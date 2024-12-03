contract_address = '0x59Bc853256FB0Ccb7c486302618d44911D298b27'
pk = '0x391B66930297AFdd8725Ba4Ae92Aebc28Cc22167'
sk = '0x84ee0e21c64951184d69922b9e0b79f06e0dc8cb85302cb48b3c189e8f996402'
abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"requestId","type":"uint256"},{"indexed":False,"internalType":"string","name":"result","type":"string"},{"indexed":True,"internalType":"address","name":"fulfiller","type":"address"}],"name":"DataFulfilled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"uint256","name":"requestId","type":"uint256"},{"indexed":True,"internalType":"address","name":"requester","type":"address"},{"indexed":False,"internalType":"string","name":"question","type":"string"},{"indexed":False,"internalType":"string","name":"source","type":"string"}],"name":"DataRequested","type":"event"},{"inputs":[{"internalType":"uint256","name":"requestId","type":"uint256"},{"internalType":"string","name":"result","type":"string"}],"name":"fulfillData","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"question","type":"string"},{"internalType":"string","name":"source","type":"string"}],"name":"requestData","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"requests","outputs":[{"internalType":"address","name":"requester","type":"address"},{"internalType":"string","name":"question","type":"string"},{"internalType":"string","name":"source","type":"string"},{"internalType":"bool","name":"fulfilled","type":"bool"},{"internalType":"address","name":"fulfiller","type":"address"}],"stateMutability":"view","type":"function"}]
llm_path={
        'gemini': './datas/BASE/google.json',
        'llama': './datas/BASE/llama.json',
        'chatgpt': './datas/BASE/gpt.json',
        'hunyuan': './datas/BASE/tencent.json',
        'chatglm': './datas/BASE/chatglm.json',
}
blockchain_url = 'http://127.0.0.1:7545'
node_num = 10