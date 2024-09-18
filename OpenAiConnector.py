import openai
from openai import OpenAI
import requests

openai.api_key = '*******************************************************************'
client = OpenAI(api_key=openai.api_key)

def connect_open_ai(encoded_image) :
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "CPATCHA에서 요구하는 글자만을 반환한다."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    # 결과 출력
    content = response.json()['choices'][0]['message']['content']
    print(content)
    return content
