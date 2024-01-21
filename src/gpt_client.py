import os
import aiohttp
import aiofiles
from datetime import datetime


class GPTClient:
    def __init__(self, api_key, model="gpt-4-1106-preview"):
        self.api_key = api_key
        self.model = model
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.api_url = "https://api.openai.com/v1/chat/completions"


    async def submit_message(self, whole_text):
        async with aiohttp.ClientSession() as session:
            payload = {
                'model': self.model,  # gpt-4-turbo
                'messages': whole_text
            }

            async with session.post(self.api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['choices'][0]['message']
                else:
                    # error handler
                    response_text = await response.text()
                    print(f"Error from OpenAI: {response.status} - {response_text}")
                    return None
    
    async def get_image(self, prompt):
        image_api_url = "https://api.openai.com/v1/images/generations"
        payload = {
            'model': 'dall-e-3',
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024'
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(image_api_url, headers=self.headers, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data['data'][0]['url']
                    return await self._download_image(image_url)
                else:
                    print(f"Error from OpenAI: {response.status}")
                    return None


    async def _download_image(self, url):
        image_folder = 'images'
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(image_folder, f"{timestamp}.png")

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(file_path, mode='wb') as file:
                        await file.write(await response.read())
                    return file_path
                else:
                    print(f"Error downloading image: {response.status}")
                    return None


    

