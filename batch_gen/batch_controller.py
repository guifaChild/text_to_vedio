# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月15日
描述：批次生成视频
"""

import pandas as pd
import os
import json
import requests

from batch_gen.batch_to_image import draw_picture
from batch_gen.batch_to_vedio import merge_vedio
from batch_gen.batch_tts import load_source_data_text

negative ="NSFW,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.4),DeepNegative,(fat:1.2),facing away, looking away,tilted head, {Multiple people}, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra leg, extra foot,"
prompt = "best quality,masterpiece,illustration, an extremely delicate and beautiful,extremely detailed,CG,unity,8k wallpaper, "


# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)

print("项目根路径:", project_root)
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

    parent_path = new_path.rsplit('\\', 1)[0]

    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    df.to_csv(new_path,index=False,encoding='utf-8')
    return new_path
def split_data_process(path,parent):
    df = pd.read_csv(path)
    for i in range(len(df)):
        # 读取整段文本 并且按照中文的句号进行切分
        title=df["title"][i]
        content = df["content"][i].split('。')
        content = [x.strip().replace("\n","") for x in content if len(x.strip()) > 0]
        # 创建新的文件保存切割后的文件
        each_df = pd.DataFrame(content,columns=["text"])
        data_csv_path = project_root+"\\data\\data_split\\"+ parent
        if not os.path.exists(data_csv_path):
            os.mkdir(data_csv_path)
        csv_save_path =data_csv_path +'\\'+ df["title"][i] + ".csv"
        each_df.to_csv(csv_save_path,index=False)
    return data_csv_path


def bach_gen_video(filepath,parent_name):
    parent_name = parent_name.split('.csv')[0]
    sourcepath = split_data_process(filepath,parent_name)
    file_path = [sourcepath+'\\'+item for item in os.listdir(sourcepath)]
    # 生成提示词
    for item in file_path :
        load_data_text(item)
    #
    # 生成语音
    for item in file_path :
        load_source_data_text(item)

    #生成图片
    prompt_file =[item.replace('data_split','data_prompt') for item in file_path]
    for item in prompt_file:
        draw_picture(item)

    image_file =[item.split('.csv')[0].replace('data_prompt','data_image') for item in prompt_file]
    audio_file = [item.replace('data_image','data_audio')for item in image_file]
    result='\\'
    for i in range(len(image_file)):
        result = merge_vedio(image_file[i],audio_file[i],parent_name)

    return result.rsplit('\\', 1)[0]







    # 保存为csv格式




if __name__ == '__main__':
    bach_gen_video("sddf","2023-3-15.csv")
