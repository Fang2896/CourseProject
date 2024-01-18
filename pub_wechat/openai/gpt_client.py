import requests
import json
# from openai import OpenAI
from openai.dialogue_history import DialogueHistory


class GPTClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def submit_message(self, whole_text):
        payload = {
            'model': 'gpt-4-1106-preview',  # gpt-4-turbo
            'messages': whole_text
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']
        else:
            # error handler
            print(f"Error from OpenAI: {response.status_code} - {response.text}")
            return None

    # async def submit_message(self, whole_text):
    #     async with aiohttp.ClientSession() as session:
    #         payload = {
    #             'model': 'gpt-4-1106-preview',  # gpt-4-turbo
    #             'messages': whole_text
    #         }
    #         async with session.post(self.api_url, headers=self.headers, json=payload) as response:
    #             if response.status == 200:
    #                 data = await response.json()
    #                 return data['choices'][0]['message']
    #             else:
    #                 # error handler
    #                 response_text = await response.text()
    #                 print(f"Error from OpenAI: {response.status} - {response_text}")
    #                 return None

