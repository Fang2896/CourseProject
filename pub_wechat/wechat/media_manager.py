# -*- coding: utf-8 -*-
# filename: media.py

import urllib3
import json
import requests


class MediaManager():
    def __init__(self):
      pass

    # 上传图片
    def upload(self, accessToken, filePath, mediaType):
        with open(filePath, 'rb') as file:
            files = {'media': file}
            postUrl = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={accessToken}&type={mediaType}"
            response = requests.post(postUrl, files=files)
            print("Upload Success: \n", response.text)

            response_data = json.loads(response.text)

            if 'media_id' in response_data:
                return response_data['media_id']
            else:
                print("Error or media_id not found in response")
                return None


    # 下载用户发的资源
    def get(self, accessToken, mediaId):
        postUrl = f"https://api.weixin.qq.com/cgi-bin/media/get?access_token={accessToken}&media_id={mediaId}"
        response = requests.get(postUrl, stream=True)

        if response.headers.get('Content-Type') in ['application/json', 'text/plain']:
            jsonDict = response.json()
            print(jsonDict)
        else:
            with open("test_media.jpg", "wb") as mediaFile:
                for chunk in response.iter_content(chunk_size=128):
                    mediaFile.write(chunk)
            print("get successful")


# 测试
# if __name__ == '__main__':
#     myMedia = MediaManager()
#     accessToken = AccessTokenManager().get_access_token()
#     filePath = "/root/Grammar-Correction-Bot/pub_wechat/assets/test.JPG"
#     mediaType = "image"
#     myMedia.upload(accessToken, filePath, mediaType)



