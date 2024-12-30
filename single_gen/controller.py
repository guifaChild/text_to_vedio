# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月15日
描述：单个视频的生成
"""
import pandas as pd
import os
import re
import requests

from .single_to_image import draw_picture
from .single_to_vedio import merge_vedio
from .single_tts import load_source_data_text
from .single_to_vedio import remerge_vedio
from .prompt_util import translate
from util.llm import llm_promt
current_file_path = os.path.abspath(__file__)

# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)
negative ="NSFW,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.4),DeepNegative,(fat:1.2),facing away, looking away,tilted head, {Multiple people}, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra leg, extra foot,"
prompt = "best quality,masterpiece,illustration, an extremely delicate and beautiful,extremely detailed,CG,unity,8k wallpaper, "


def prompt_api_generation(param):
    pdata = pd.read_csv(project_root + '\\config\\data_1.csv')

    api_url = pdata.iloc[4, 1]
    api_key = pdata.iloc[5, 1]
    # 发送HTTP POST请求
    url = api_url
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    data = {
        "model": "yi-large",
        "messages": [{"role": "user", "content": param}],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    cotent =response_data['choices'][0]['message']['content']
    # 输出结果
    return  cotent




def load_data_text(path,title):
    df = pd.DataFrame(columns=['text', 'index', 'prompt', 'negative'])
    df_temp = pd.read_csv(path)
    for  index, row in df_temp.iterrows():
        prompt_param ='根据下面的内容描述，生成一副画面并用英文单词表示：'+row['text']
        # result_json = prompt_generation(prompt_param)

        result_json = llm_promt(content=prompt_param)
        new_row = {'text': row['text'], 'index': index, 'prompt': prompt + result_json, 'negative': negative}
        df = df.append(new_row, ignore_index=True)
    new_path = path.replace("data_split","data_prompt")

    parent_path = new_path.split('\\'+title+'.csv')[0]

    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    df.to_csv(new_path,index=False,encoding='utf-8')
    return new_path


def load_api_data_text(path,title):
    df = pd.DataFrame(columns=['text', 'index', 'prompt', 'negative'])
    df_temp = pd.read_csv(path)
    for  index, row in df_temp.iterrows():
        prompt_param ='根据下面的内容描述，生成一副画面并用英文单词表示：'+row['text']
        result_json = prompt_api_generation(prompt_param)
        new_row = {'text': row['text'], 'index': index, 'prompt': prompt + result_json, 'negative': negative}
        df = df.append(new_row, ignore_index=True)
    new_path = path.replace("data_split","data_prompt")

    parent_path = new_path.split('\\'+title+'.csv')[0]

    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    df.to_csv(new_path,index=False,encoding='utf-8')
    return new_path



def load_local_translate(path,title):
    df = pd.DataFrame(columns=['text', 'index', 'prompt', 'negative'])
    df_temp = pd.read_csv(path)
    for  index, row in df_temp.iterrows():

        result_json = translate(row['text'])
        print("本地翻译不需要跑大模型")
        new_row = [{'text': row['text'], 'index': index, 'prompt': prompt + result_json, 'negative': negative}]

        df = pd.concat([df,pd.DataFrame(new_row)], ignore_index=True)
    new_path = path.replace("data_split","data_prompt")
    parent_path = new_path.split('\\'+title+'.csv')[0]
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    df.to_csv(new_path,index=False,encoding='utf-8')
    return new_path








def split_data_process(path,title):
    df = pd.read_csv(path)
    for i in range(len(df)):
        # 读取整段文本 并且按照中文的句号进行切分
        content = df["content"][i].split('。')
        content = [x.strip().replace("\n","") for x in content if len(x.strip()) > 0]
        # 创建新的文件保存切割后的文件
        each_df = pd.DataFrame(content,columns=["text"])
        data_csv_path = os.path.join(project_root+"\\static\\data\\data_split", title)
        if not os.path.exists(data_csv_path):
            os.mkdir(data_csv_path)
        csv_save_path = data_csv_path+'\\'+title + ".csv"
        each_df.to_csv(csv_save_path,index=False)
    return csv_save_path




"""真正的生成视频"""
def gen_video(title,content):
    df = pd.DataFrame(columns=['title',  'content'])
    new_row = {'title': title, 'content': content}
    rows_to_add = [
        {'title': title, 'content': content}
    ]
    # 将所有新行转换为 DataFrame 并合并
    df = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)

    df.to_csv(project_root+'\\static\\data\\source_data\\'+title+'.csv', index=False, encoding='utf-8')
    # 分割数据
    split_path = split_data_process(project_root+'\\static\\data\\source_data\\'+title+'.csv',title)
    # 本地大模型生成生成提示词
    # prompp_path = load_data_text(split_path,title)
    # 本地直译
    prompp_path = load_local_translate(split_path, title)
    # 生成语音
    audio_path = load_source_data_text(split_path)
    #生成图片
    image_path = draw_picture(prompp_path)
    #合成视频
    video_path= merge_vedio(image_path,audio_path)

    return video_path


"""真正api的生成视频"""
def gen_api_video(title,content):
    df = pd.DataFrame(columns=['title',  'content'])
    new_row = {'title': title, 'content': content}
    df = df.append(new_row, ignore_index=True)
    df.to_csv(project_root+'\\static\\data\\source_data\\'+title+'.csv', index=False, encoding='utf-8')
    # 分割数据
    split_path = split_data_process(project_root+'\\static\\data\\source_data\\'+title+'.csv',title)
    # 生成提示词
    prompp_path = load_api_data_text(split_path,title)
    # 生成语音
    audio_path = load_source_data_text(split_path)
    #生成图片
    image_path = draw_picture(prompp_path)
    #合成视频
    video_path= merge_vedio(image_path,audio_path)

    return video_path

















def remerge_video(imagpath,audio_path,vediopath):
    return remerge_vedio(imagpath,audio_path,vediopath)


















    # 保存为csv格式




if __name__ == '__main__':
    pass