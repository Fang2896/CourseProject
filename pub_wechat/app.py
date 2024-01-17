from flask import Flask, request
from pydantic import Json
from token_config_manager import TokenConfigManager

from token_config_manager import TokenConfigManager
from wechat_server import WeChatServer
from json_config_manager import JsonConfigManager
from dialogue_history import DialogueHistory
from gpt_client import GPTClient


def create_app():
    token_config_manager = TokenConfigManager()
    json_config_manager = JsonConfigManager('config.json')

    openai_api_key = token_config_manager.get("OPENAI_API_KEY")
    gpt_client = GPTClient(openai_api_key)

    history = DialogueHistory(json_config_manager)

    app = Flask(__name__)
    wechat_server = WeChatServer(token_config_manager.get("WECHAT_TOKEN"))

    @app.route('/wx', methods=['GET', 'POST'])
    def wechatai():
        if request.method == 'GET':
            return wechat_server.verify_wechat(request)
        else:
            user_message_content, from_user_name, to_user_name \
                = wechat_server.getUserMessageContentFromXML(request.data)
            print("user message content: ", user_message_content)

            #================ Start GPT Processing =============#
            history.add_message("user", user_message_content)
            response = gpt_client.submit_message(history.get_full_history())
            reply_content = response["content"]
            history.add_message("assistant", reply_content)
            #================ End GPT Processing =============#

            return wechat_server.generate_response_xml(from_user_name, to_user_name, reply_content)

    return app

