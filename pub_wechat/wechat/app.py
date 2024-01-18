import threading
from flask import Flask, request
from pydantic import Json
from utils.token_config_manager import TokenConfigManager

from utils.token_config_manager import TokenConfigManager
from wechat.wechat_server import WeChatServer
from utils.json_config_manager import JsonConfigManager
from openai.dialogue_history import DialogueHistory
from openai.gpt_client import GPTClient
from wechat.media_manager import MediaManager
from wechat.access_token import AccessTokenManager


class WeChatApp:
    def __init__(self):
        # 一些参数管理
        self.token_config_manager = TokenConfigManager()
        self.json_config_manager = JsonConfigManager('config.json')
        
        # openai侧管理
        self.gpt_client = GPTClient(self.token_config_manager.get("OPENAI_API_KEY"))
        self.history = DialogueHistory(self.json_config_manager)
        
        # 微信端管理
        self.wechat_server = WeChatServer(self.token_config_manager.get("WECHAT_TOKEN"))
        self.media_manager = MediaManager()
        self.access_token_manager = AccessTokenManager(self.token_config_manager.get("WECHAT_APP_ID"),
                                                       self.token_config_manager.get("WECHAT_APP_SECRET"))

        # 这个线程用来管理token
        self.token_thread = threading.Thread(target=self.access_token_manager.run)
        self.token_thread.daemon = True  # 将线程设置为守护线程
        self.token_thread.start()

    def wechatai(self, request):
        if request.method == 'GET':
            return self.wechat_server.verify_wechat(request)
        elif request.method == 'POST':
            use_msg_data = self.wechat_server.getUserMessageContentFromXML(request.data)
            print("=======\n User Message Data: \n", use_msg_data, "\n=======")

            if use_msg_data["MsgType"] == "text":
                return self.handle_text_msg(use_msg_data)
            elif use_msg_data["MsgType"] == "image":
                return self.handle_image_msg(use_msg_data)
            elif use_msg_data["MsgType"] == "voice":
                return self.handle_voice_msg(use_msg_data)

            # 根据消息类型生成响应XML
            

    def handle_text_msg(self, use_msg_data):
        from_user_name = use_msg_data["FromUserName"]
        to_user_name = use_msg_data["ToUserName"]

        self.history.add_message("user", use_msg_data["Content"])
        response = self.gpt_client.submit_message(self.history.get_full_history())
        reply_content = response["content"]
        print("GPT says: " + reply_content)
        self.history.add_message("assistant", reply_content)

        return self.wechat_server.generate_text_response_xml(from_user_name, to_user_name, reply_content)

    def handle_image_msg(self, use_msg_data):
        from_user_name = use_msg_data["FromUserName"]
        to_user_name = use_msg_data["ToUserName"]

        accessToken = self.access_token_manager.get_access_token()

        # 测试用的
        filePath = "/root/Grammar-Correction-Bot/pub_wechat/assets/test_image.JPG"
        mediaType = "image"
        media_id = self.media_manager.upload(accessToken, filePath, mediaType)

        return self.wechat_server.generate_image_response_xml(from_user_name, to_user_name, media_id)


    def handle_voice_msg(self, use_msg_data):
        from_user_name = use_msg_data["FromUserName"]
        to_user_name = use_msg_data["ToUserName"]

        accessToken = self.access_token_manager.get_access_token()

        # 测试用的
        filePath = "/root/Grammar-Correction-Bot/pub_wechat/assets/test_voice.mp3"
        mediaType = "voice"
        media_id = self.media_manager.upload(accessToken, filePath, mediaType)

        return self.wechat_server.generate_voice_response_xml(from_user_name, to_user_name, media_id)


# Flask 应用部分
app = Flask(__name__)
wechat_app = WeChatApp()

@app.route('/wx', methods=['GET', 'POST'])
def wechatai():
    return wechat_app.wechatai(request)

