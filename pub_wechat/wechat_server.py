import xml.etree.ElementTree as ET   
from flask import Flask, request, make_response
import hashlib
import time


class WeChatServer:
    def __init__(self, token):
        self.token = token

    def printXML(xml_content):
        # 创建XML元素
        element = ET.XML(xml_content)

        # 使用indent()函数进行格式化打印
        ET.indent(element)
        print(ET.tostring(element, encoding='unicode'))

    def getUserMessageContentFromXML(xml_content):
        # 解析XML字符串
        root = ET.fromstring(xml_content)

        # 提取数据
        content = root.find('Content').text
        from_user_name = root.find('FromUserName').text
        to_user_name = root.find('ToUserName').text
        return content, from_user_name, to_user_name

    def generate_response_xml(from_user_name, to_user_name, output_content):
        output_xml = '''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[%s]]></Content>
        </xml>'''
        
        # 2. 通过 make_response 函数封装网络返回结构体
        response = make_response(output_xml % (from_user_name, to_user_name, str(int(time.time())), output_content))
        response.content_type = 'application/xml'
        return response

    def verify_wechat(request):
        token = 'Orangestar'

        data = request.args
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')

        temp = [timestamp, nonce, token]
        temp.sort()
        temp = ''.join(temp)

        if (hashlib.sha1(temp.encode('utf8')).hexdigest() == signature):
            return echostr
        else:
            return 'error', 403

