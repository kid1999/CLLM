import requests
import time

# set to your key.
API_KEY = "sb-xxxxx"


# 封装函数：发送请求获取答案
def get_gpt_answer(question):
    # 设置 API URL 和 Header
    url = "https://api.openai-sb.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",  # 确保 GROQ_API_KEY 被正确设置
    }

    # 设置请求数据
    payload = {
        "model": "gpt-4o-mini",
        # "temperature": 0,
        # "top_p": 0,
        # "seed": 42,      # 固定种子，确保一致性
        # "system_fingerprint": "fp_44709d6fcb",
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    while True:
        # Make the POST request with the proxy
        response = requests.post(url, headers=headers, json=payload)
        # Check if the request was successful
        if response.status_code == 200:
            text = response.json()["choices"][0]["message"]["content"]
            print(response.json()["system_fingerprint"])
            return text
        else:
            print(f"Error: {response.status_code}, {response.text}")
            time.sleep(1)
