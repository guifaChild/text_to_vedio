# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：调用微软官网的api，生成的文本合成语音
"""
import os, requests, time
from xml.etree import ElementTree
import pandas as pd
# 你注册申请的微软tts的api——key
subscription_key = ""


class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.tts = "你是最棒的哦，哇哈哈哈"
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)

    def save_audio(self,data,child_path):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'TTSForPython'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        voice.set('name', 'zh-CN-YunxiNeural')
        voice.set(' rate ', '1.4')
        voice.text = data
        body = ElementTree.tostring(xml_body)
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(child_path+'.wav', 'wb') as audio:
                audio.write(response.content)
                # print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
            print("Reason: " + str(response.reason) + "\n")




    def get_voices_list(self):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/voices/list'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
        }
        response = requests.get(constructed_url, headers=headers)
        if response.status_code == 200:
            print("\nAvailable voices: \n" + response.text)
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")



def load_source_data_text(path):
    app = TextToSpeech(subscription_key)
    app.get_token()
    df_temp = pd.read_csv(path)
    for index, row in df_temp.iterrows():
        new_path = path.split(".csv")[0].replace("data_split","data_audio")
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        path_child =os.path.join(new_path,str(index))
        app.save_audio(row['text'],path_child)
    return new_path


if __name__ == "__main__":
    load_source_data_text("data/data_split/测试_2/测试_2.csv")

