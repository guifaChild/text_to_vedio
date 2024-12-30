# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年12月25日
描述：
"""
import os


# from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips
import pyJianYingDraft as draft
# from moviepy.video.io.VideoFileClip import VideoFileClip
import pandas as pd
from pyJianYingDraft import Intro_type, Transition_type, trange
import random
import shutil

current_file_path = os.path.abspath(__file__)

# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)

print("项目根路径:", project_root)


pdata = pd.read_csv(project_root+'\\config\\data_1.csv')

jianying_path = pdata.iloc[4, 1]




def string_duration(num):
    return str(num)+"s"




def merge_vedio(image_dir_path,audio_dir_path,parent):
    # 将文件名按照顺序排列
    image_files = os.listdir(image_dir_path)
    audio_files = os.listdir(audio_dir_path)
    print(image_files)
    new_path = image_dir_path.replace("data_image", "data_draft")+".json"
    directory = os.path.dirname(new_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("文件路径："+new_path)
    text_path = image_dir_path.replace("data_image", "data_split")+".csv"
    df_temp = pd.read_csv(text_path)

    # 创建剪映草稿
    script = draft.Script_file(1080, 1080)  # 1080x1080分辨率
    # 添加音频、视频和文本轨道
    script.add_track(draft.Track_type.audio).add_track(draft.Track_type.video).add_track(draft.Track_type.text)

    sum_length=0
    for i in range(len(audio_files)):
        image_path = os.path.join(image_dir_path, str(i) + ".png")
        audio_path = os.path.join(audio_dir_path, str(i) + ".wav")
        # 当前的文本信息     df_temp['text'].iloc[1]
        # 从本地读取音视频素材和一个gif表情包
        audio_material = draft.Audio_material(audio_path)
        video_material = draft.Video_material(image_path)
        script.add_material(audio_material).add_material(video_material)  # 随手添加素材是好习惯

        temp_item_length=audio_material.duration
        # 创建音频片段
        audio_segment = draft.Audio_segment(audio_material,
                                            trange(sum_length, temp_item_length),  # 片段将位于轨道上的0s-5s（注意5s表示持续时长而非结束时间）
                                            volume=0.6)  # 音量设置为60%(-4.4dB)
        if sum_length == 0:
            # 增加一个1s的淡入
            audio_segment.add_fade("1s", "0s")
        # audio_segment.add_fade("1s", "0s")

        # 增加一个1s的淡入

        # 创建视频片段
        video_segment = draft.Video_segment(video_material,
                                            trange(sum_length, temp_item_length))  # 片段将位于轨道上的0s-4.2s（取素材前4.2s内容，注意此处4.2s表示持续时长）

        animations_in = list(Intro_type)   #动画效果选择

        # 产生一个随机索引
        random_index = random.randint(0, len(animations_in) - 1)

        video_segment.add_animation(animations_in[random_index])  # 添加一个入场动画“斜切”

        animations_transform = list(Transition_type)  # 动画效果选择

        # 产生一个随机索引
        random_index2 = random.randint(0, len(animations_transform) - 1)
        # 为二者添加一个转场
        video_segment.add_transition(animations_transform[random_index2])  # 注意转场添加在“前一个”视频片段上

        # 将上述片段添加到轨道中
        script.add_segment(audio_segment).add_segment(video_segment)

        # 创建一行类似字幕的文本片段并添加到轨道中
        text_segment = draft.Text_segment(df_temp['text'].iloc[i], trange(sum_length, temp_item_length),
                                          # 文本将持续整个视频（注意script.duration在上方片段添加到轨道后才会自动更新）
                                          style=draft.Text_style(color=(1.0, 1.0, 0.0)),  # 设置字体颜色为黄色
                                          clip_settings=draft.Clip_settings(transform_y=-0.8))  # 模拟字幕的位置
        script.add_segment(text_segment)
        sum_length=sum_length+temp_item_length


    # 可以增加尾部内容这里可以单独处理。
    script.dump(new_path)
    return  new_path




def out_put_video(dft_path):
#     第一步先更改jianying的稿件
#      导出视频
#     草稿样本
    example_dir = jianying_path
    parent_directory = os.path.dirname(example_dir)
    video_path =dft_path.replace("data_draft","data_vedio")
    if not os.path.exists(video_path):
        os.makedirs(video_path)
    for item in os.listdir(dft_path):

        # 拷贝目录:
        target_lu=parent_directory+"\\"+item.split(".")[0]
        # 目标路径
        if os.path.exists(target_lu):
            # 删除现有的目录
            shutil.rmtree(target_lu)
            print(f"已存在的目录 {target_lu} 已删除。")

            # 拷贝新的目录
        try:
            shutil.copytree(example_dir, target_lu)
            shutil.copy(dft_path+"\\"+item, target_lu+"\\draft_content.json")
            print(f"目录 {example_dir} 已成功拷贝到 {target_lu}。")
        except Exception as e:
            print(f"拷贝目录时出错：{e}")
        ctrl = draft.Jianying_controller()
        print(os.path.basename(target_lu))
        ctrl.export_draft(os.path.basename(target_lu), video_path+"\\"+item.split(".")[0]+".mp4")

    return video_path
    # # 此前需要将剪映打开，并位于目录页
    # ctrl = draft.Jianying_controller()
    #
    # # 然后即可导出指定名称的草稿
    # ctrl.export_draft("12月26日 (1)", "D:nucai.mp4")  # 注意导出结束后视频才会被剪切至指定位置




if __name__ == '__main__':
    # print(merge_vedio("D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_image\\2024-12-26\\奴才","D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_audio\\2024-12-26\\奴才",""))
    out_put_video("D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_draft\\2024-12-26")

    # draft_names = ...
    # export_folder = ...
    # for name in draft_names:
    #     ctrl.export_draft(name, os.path.join(export_folder, name, ".mp4"))



