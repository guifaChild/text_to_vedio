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

import auto_upload
from .batch_to_image import draw_picture
# from .batch_to_vedio import merge_vedio
from .batch_tts import load_source_data_text
from util.llm import llm_promt
from util.jianying import merge_vedio,out_put_video
import asyncio
from datetime import datetime
negative ="NSFW,sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy,(long hair:1.4),DeepNegative,(fat:1.2),facing away, looking away,tilted head, {Multiple people}, lowres,bad anatomy,bad hands, text, error, missing fingers,extra digit, fewer digits, cropped, worstquality, low quality, normal quality,jpegartifacts,signature, watermark, username,blurry,bad feet,cropped,poorly drawn hands,poorly drawn face,mutation,deformed,worst quality,low quality,normal quality,jpeg artifacts,signature,watermark,extra fingers,fewer digits,extra limbs,extra arms,extra legs,malformed limbs,fused fingers,too many fingers,long neck,cross-eyed,mutated hands,polar lowres,bad body,bad proportions,gross proportions,text,error,missing fingers,missing arms,missing legs,extra digit, extra arms, extra leg, extra foot,"
prompt = "best quality,masterpiece,illustration, an extremely delicate and beautiful,extremely detailed,CG,unity,8k wallpaper, "


# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)

print("项目根路径:", project_root)

def load_data_text(path):
    # 读取指定的文件进行加载处理
    #sum_content = df_temp['text'].str.cat(sep=" ")
    if path =="" :
        path="data/data_split/侦探悬疑类/story_1.csv"




    df = pd.DataFrame(columns=['text', 'index', 'prompt', 'negative'])
    df_temp = pd.read_csv(path)
    # 获取全文，这里第一次调用分析故事背景
    # 风格可以进行自定义：人物可以进行提取。
    # sum_content = df_temp['text'].str.cat(sep=" ")
    # sum_role_messages=[
    #     {"role": "system", "content": "你是一个文本编辑"},
    #     {"role": "system","content": sum_content+"查看上面的文本，然后扮演一个文本编辑来回答问题。"},
    #     {"role":"user", "content": "这个文本里的故事类型是啥，时代背景是啥， 主角有哪几个， 每个角色的性别年龄穿着是啥？没外观描述的直接猜测，尽量精简 格式按照：故事类型：（故事类型）\n时代背景：（时代背景）\n主角1：（名字，编号AA，性别，年龄，发型和颜色，衣服类型和颜色 ）\n主角2：（名字，编号BB，性别，年龄，发型和颜色，衣服类型和颜色  ）\n主角3........ ，不知道的直接猜测设定，有头发的都设置为黑色，例如：（拉拉，AA，男，白色短发，黑色西装，20岁）或者（我，BB，女，黄色短发，紫色连衣裙，25岁）等.注意这里是例子实际细节要符合剧本.每个角色的衣服颜色要不同，衣服类型要不同，年龄要不同，外观细节要不同，必须包含AA BB等编号，不能出不详 未知等字 中文回答。"}
    #     ]
    # role_charactor = openai_llm(sum_role_messages)


    for  index, row in df_temp.iterrows():
        prompt_param ='根据下面的内容描述，生成一副画面并用英文单词表示：'+row['text']
        # result_json = prompt_generation(prompt_param)
        # 每一部分分析，来处理成为完整的prompt
        result_json =  llm_promt(content=prompt_param)
        new_row = {'text': row['text'], 'index': index, 'prompt': prompt + result_json, 'negative': negative}
        new_df = pd.DataFrame([new_row])  # Create a DataFrame from the new row dictionary
        df = pd.concat([df, new_df], ignore_index=True)  # Concatenate the old DataFrame with the new DataFrame
    new_path = path.replace("data_split","data_prompt")

    # parent_path = new_path.split('\\', 1)[0]
    parent_path = os.path.dirname(new_path)
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    df.to_csv(new_path,index=False,encoding='utf-8')
    return new_path
def split_data_process(path,parent):
    df = pd.read_csv(path)
    wor_info_dir = os.path.dirname(os.path.dirname(path).replace("data_source","data_vedio"))
    if not os.path.exists(wor_info_dir):
        os.makedirs(wor_info_dir)
    accounts={}
    current_date = datetime.now().date()
    print(current_date)
    for i in range(len(df)):
        # 读取整段文本 并且按照中文的句号进行切分
        # 生成两个内容   一个是text上传信息的内容，一个是账号信息

        title = df["title"][i]
        account = df["account"][i]
        work_info = df["work_information"][i]
        with open(os.path.join(wor_info_dir,str(current_date)+"\\"+title+".txt"), "w") as file:
            file.write(str(work_info))

        accounts[title]=account

        # 验证一下有无本地的cookie
        account_file = project_root+"\\cookies\\douyin\\"+account+".json"
        if not os.path.exists(account_file):
            print("文件存在。")
        asyncio.run(auto_upload.main(platform="douyin", account_name=account, action="login", publish_type=0))
        content = df["content"][i].split('。')
        content = [x.strip().replace("\n","") for x in content if len(x.strip()) > 0]
        # 创建新的文件保存切割后的文件
        each_df = pd.DataFrame(content,columns=["text"])
        data_csv_path = project_root+"\\static\\data\\data_split\\"+ parent
        if not os.path.exists(data_csv_path):
            os.mkdir(data_csv_path)
        csv_save_path =data_csv_path +'\\'+ df["title"][i] + ".csv"
        each_df.to_csv(csv_save_path,index=False)
    with open(path.replace("csv","json"), 'w') as f:
        json.dump(accounts, f, indent=4)

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
    # 合成视频
    for i in range(len(image_file)):
        # result = merge_vedio(image_file[i],audio_file[i],parent_name)
        result = merge_vedio(image_file[i], audio_file[i], parent_name)

    video_path = out_put_video(os.path.dirname(result))
    # 自动上传视频
    video_items = [os.path.join(video_path,item) for item in os.listdir(video_path) if item.endswith(".mp4")]
    for video_item in video_items:
        asyncio.run(auto_upload.main(platform="douyin", account_name="woai1234A", action="upload", video_file=video_item, publish_type=0))

    return video_path

    # 保存为csv格式







if __name__ == '__main__':
    bach_gen_video("sddf","2023-3-15.csv")
