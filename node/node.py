from web3 import Web3
import time
import json
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from utils.aggre import find_most_similar_sentence, find_most_similar_sentence_bert
from utils.llm_api import get_gpt_answer
from constantModule import (
    contract_address,
    pk,
    sk,
    llm_path,
    abi,
    blockchain_url,
    node_num,
)


def fetch_data_from_datasource(source, question, id):
    path_map = llm_path
    # 如果数据集中没有就去调用 LLM API
    if source in path_map.keys():
        path = path_map[source]
        # 打开JSON文件
        with open(path, "r", encoding="utf-8") as file:
            # 加载JSON数据
            data = json.load(file)
        # 遍历JSON数据
        for item in data:
            # 如果找到匹配的问题
            if item["question"] == question:
                # 检查索引是否有效
                if id < len(item["answers"]):
                    return item["answers"][id]
                else:
                    return "索引超出答案范围"
        return get_gpt_answer(question)


class Node:
    def __init__(self, id, is_malicious, pk, sk, web3):
        self.id = id
        self.is_malicious = is_malicious
        self.pk = pk
        self.sk = sk
        self.web3 = web3

    def get_data(self, question, source):
        # 根据不同的任务source和question返回不同的数据，从data中
        return fetch_data_from_datasource(source, question, self.id)

    def callback_data(self, task_id, data, web3, contract):
        nonce = web3.eth.get_transaction_count(self.pk)
        tx = contract.functions.fulfillData(task_id, data).build_transaction(
            {
                "from": self.pk,
                "nonce": nonce,
                "gas": 2000000,
                "gasPrice": web3.to_wei("50", "gwei"),
            }
        )

        signed_tx = web3.eth.account.sign_transaction(tx, self.sk)

        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Tx successful with hash: {tx_receipt.transactionHash.hex()}")

    def handle_event(self, event):
        # 处理事件
        task_id = event.args.requestId
        question = event.args.question
        source = event.args.source

        data = self.get_data(question, source)
        return task_id, data


def oracle_network():
    web3 = Web3(Web3.HTTPProvider(blockchain_url))
    contract = web3.eth.contract(address=contract_address, abi=abi)

    # 先假定所有人的pk sk 一样
    nodes = [
        Node(id=i, is_malicious=False, pk=pk, sk=sk, web3=web3) for i in range(node_num)
    ]
    node_weight = np.array([0.5 for _ in range(node_num)])

    event_filter = contract.events.DataRequested().create_filter(from_block="0x0")
    while True:
        # 事件监听
        logs = event_filter.get_new_entries()
        for log in logs:
            res = []
            # 请求数据
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(node.handle_event, log) for node in nodes]
                for future in futures:
                    res.append(future.result())
            # 数据聚合
            task_id, final_data, score, node_weight = find_most_similar_sentence_bert(res, node_weight)
            print(task_id, final_data, score)
            print(node_weight)

            # 回传数据
            nodes[0].callback_data(task_id, final_data, web3, contract)
        time.sleep(1)


if __name__ == "__main__":
    oracle_network()
