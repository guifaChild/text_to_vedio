# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：根据上一步切割完成的语料生成英文提示词，为生成图片做准备
"""

import pandas as pd
import os
import requests
import json




negative ="NSFW,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.4),DeepNegative,(fat:1.2),facing away, looking away,tilted head, {Multiple people}, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra leg, extra foot,"
prompt = "best quality,masterpiece,illustration, an extremely delicate and beautiful,extremely detailed,CG,unity,8k wallpaper, "
def prompt_generation(param):
    # 发送HTTP POST请求
    url = 'http://127.0.0.1:8000'
    data = {'prompt': param}
    json_data = json.dumps(data)
    # 发送HTTP POST请求
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    result_json = json.loads(response.text)
    # 输出结果
    return  result_json['response']

def load_data_text(path):
    # 读取指定的文件进行加载处理
    if path =="" :
        path="data/data_split/侦探悬疑类/story_1.csv"
    df = pd.DataFrame(columns=['text', 'index', 'prompt', 'negative'])
    df_temp = pd.read_csv(path)
    for  index, row in df_temp.iterrows():
        prompt_param ='根据下面的内容描述，生成一副画面并用英文单词表示：'+row['text']
        result_json = prompt_generation(prompt_param)
        new_row = {'text': row['text'], 'index': index, 'prompt': prompt + result_json, 'negative': negative}
        df = df.append(new_row, ignore_index=True)
    new_path = path.replace("data_split","data_prompt")

    parent_path = new_path.split('story')[0]

    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    df.to_csv(new_path,index=False,encoding='utf-8')
    return new_path


if __name__ == '__main__':
    load_data_text("")


