from flask import Flask, request
from wechat_server import WeChatServer


def create_app():
    app = Flask(__name__)

    @app.route('/wx', methods=['GET', 'POST'])
    def wechatai():
        if request.method == 'GET':
            return WeChatServer.verify_wechat(request)
        else:
            user_message_content, from_user_name, to_user_name \
                = WeChatServer.getUserMessageContentFromXML(request.data)
            print("user message content: ", user_message_content)

            # 这里可以添加对 user_message_content 的处理逻辑
            # ...

            return WeChatServer.generate_response_xml(from_user_name, to_user_name, "你好")

    return app

