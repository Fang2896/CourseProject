import os
import base64
import hashlib
import requests
from requests_toolbelt import MultipartEncoder
from urllib import parse
from token_config_manager import TokenConfigManager


def upload_file(file_path, type,webHook):
    params = parse.parse_qs( parse.urlparse( webHook ).query )
    webHookKey=params['key'][0]
    upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={webHookKey}&type={type}'
    headers = {
        "Accept" : "application/json, text/plain, */*", 
        "Accept-Encoding" : "gzip, deflate",
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36"
    }

    filename = os.path.basename(file_path)
    try:
        multipart = MultipartEncoder(
            fields = {
                'filename' : filename, 
                'filelength' : '', 
                'name' : 'media', 
                'media' : (filename, open(file_path, 'rb'), 'application/octet-stream')
            },
            boundary = '-------------------------acebdf13572468'
        )

        headers['Content-Type'] = multipart.content_type
        resp = requests.post(upload_url, headers=headers, data=multipart)
        json_res = resp.json()
        if json_res.get('media_id'):
            print(f"Upload Success! file path: {file_path}")
            return json_res.get('media_id')
    except Exception as e:
        print("Upload Fail:" + str(e))
        return ""


def send_text(text_content, webHook, mentioned_list=[], mentioned_mobile_list=[]):
    url = webHook
    headers = {
        "content-type" : "application/json"
    }
    msg = {
        "msgtype" : "text",
        "text" : {
            "content" : text_content,
            "mentioned_list" : mentioned_list,
            "mentioned_mobile_list" : mentioned_mobile_list
        }
    }

    try:
        result = requests.post(url, headers=headers, json=msg)
        print("==== Text - Request post result: " + str(result) + " ====")
        return True
    except Exception as e:
        print("Text - Requset Failed: ", str(e))
        return False


def send_image(image_path, webHook):
    url = webHook

    with open(image_path,"rb") as f:
        fd=f.read()
        base64Content=str(base64.b64encode(fd),"utf-8")

    with open(image_path,"rb") as f:
        fd=f.read()
        md = hashlib.md5()
        md.update(fd)
        md5Content = md.hexdigest()

    headers = {
        "content-type" : "application/json"
    }
    
    msg = {
        "msgtype" : "image",
        "image" : {
            "base64" : base64Content,
            "md5" : md5Content
        }
    }

    try:
        result = requests.post(url, headers=headers, json=msg)
        print("==== Image - Request post result: " + str(result) + " ====")
        return True
    except Exception as e:
        print("Image - Requset Failed:", str(e))
        return False


def send_file(file_path, webHook):
    url = webHook
    headers = {
        "content-type" : "application/json"
    }

    media_id = upload_file(file_path, "file", url)
    msg={
        "msgtype" : "file",
        "file" : {
            "media_id" : media_id
        }
    }

    try:
        result = requests.post(url, headers=headers, json=msg)
        print("==== File - Request post result: " + str(result) + " ====")
        return True
    except Exception as e:
        print("File - Requset Failed:", str(e))
        return False


def send_voice(voice_path, webHook):
    url = webHook
    headers = {
        "content-type" : "application/json"
    }

    media_id = upload_file(voice_path, "voice", url)
    msg={
        "msgtype" : "voice",
        "voice" : {
            "media_id" : media_id
        }
    }

    try:
        result = requests.post(url, headers=headers, json=msg)
        print("==== Voice - Request post result: " + str(result) + " ====")
        return True
    except Exception as e:
        print("Voice - Requset Failed:", str(e))
        return False


def main():
    token_config_manager = TokenConfigManager()

    FriendWeHook = token_config_manager.get("FRIEND_WEHOOK")

    # send_text("Hello WeChat Bot!")
    # send_image("wechat/test_files/test_image_1.png", FriendWeHook)
    # send_file("wechat/test_files/test_file_1.txt", FriendWeHook)
    send_voice("wechat/test_files/test_voice_1.amr", FriendWeHook)

if __name__ == '__main__':
   main()





