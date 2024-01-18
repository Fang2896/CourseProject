import xml.etree.ElementTree as ET   
from flask import Flask, request, make_response
import hashlib
import time


class WeChatServer:
    def __init__(self, token):
        self.token = token


    def verify_wechat(self, request):
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


    def printXML(self, xml_content):
        # 创建XML元素
        element = ET.XML(xml_content)

        # 使用indent()函数进行格式化打印
        ET.indent(element)
        print(ET.tostring(element, encoding='unicode'))


    def getUserMessageContentFromXML(self, xml_content):
        # 解析XML字符串
        root = ET.fromstring(xml_content)

        # 提取数据，分三种情况：文本，图片，语音
        msg_type = root.find('MsgType').text
        msg_data = {
            "ToUserName" : "",
            "FromUserName" : "",
            "MsgType" : "",
            "Content" : "",
            "PicUrl" : "",
            "MediaId" : "",
            "Format" : ""
        }
        msg_data["MsgType"] = msg_type
        msg_data["ToUserName"] = root.find('ToUserName').text
        msg_data["FromUserName"] = root.find('FromUserName').text

        if(msg_type == 'text'):
            msg_data["Content"] = root.find('Content').text
        elif(msg_type == 'image'):
            msg_data["PicUrl"] = root.find('PicUrl').text
            msg_data["MediaId"] = root.find('MediaId').text
        elif(msg_type == 'voice'):
            msg_data["MediaId"] = root.find('MediaId').text
            msg_data["Format"] = root.find('Format').text

        return msg_data


    def generate_text_response_xml(self, from_user_name, to_user_name, output_content):
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
    

    def generate_image_response_xml(self, from_user_name, to_user_name, output_media_id):
        output_xml = '''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[image]]></MsgType>
            <Image>
              <MediaId><![CDATA[%s]]></MediaId>
            </Image>
        </xml>'''
        
        # 2. 通过 make_response 函数封装网络返回结构体
        response = make_response(
            output_xml % (from_user_name, to_user_name, 
                          str(int(time.time())), output_media_id))
        response.content_type = 'application/xml'
        return response
    

    def generate_voice_response_xml(self, from_user_name, to_user_name, output_media_id):
        output_xml = '''
        <xml>
            <ToUserName><![CDATA[%s]]></ToUserName>
            <FromUserName><![CDATA[%s]]></FromUserName>
            <CreateTime>%s</CreateTime>
            <MsgType><![CDATA[voice]]></MsgType>
            <Voice>
              <MediaId><![CDATA[%s]]></MediaId>
            </Voice>
        </xml>'''
        
        # 2. 通过 make_response 函数封装网络返回结构体
        response = make_response(
            output_xml % (from_user_name, to_user_name, 
                          str(int(time.time())), output_media_id))
        response.content_type = 'application/xml'
        return response

    

