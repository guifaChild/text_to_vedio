# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：将生成的语音、图像合成视频
"""

import os
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips


from moviepy.video.io.VideoFileClip import VideoFileClip

from single_gen.jianying import draft_content

speed = 10
size = 700

def fl(gf, t):
    image = gf(t)
    start_index = int(speed * t)
    end_index = int(speed * t) + size
    if end_index > 768 :
        end_index = 768
        start_index = 768 - 700
    cropped_image = image[start_index:end_index, :]
    return cropped_image



def merge_vedio(image_dir_path, audio_dir_path):
    # image_files = os.listdir(image_dir_path)
    audio_files = os.listdir(audio_dir_path)
    # clips = []
    new_path = image_dir_path.replace("data_image", "data_vedio")
    new_parent = image_dir_path.replace("data_image", "data_vedio").split("story")[0]
    if not os.path.exists(new_parent):
        os.makedirs(new_parent)
    for i in range(len(audio_files)):
        image_path = os.path.join(image_dir_path, str(i) + ".png")
        audio_path = os.path.join(audio_dir_path, str(i) + ".wav")
        audio_clip = AudioFileClip(audio_path)
        img_clip = ImageSequenceClip([image_path], audio_clip.duration)
        img_clip = img_clip.set_position(('center', 'center')).fl(fl, apply_to=['mask']).set_duration(
            audio_clip.duration)
        clip = img_clip.set_audio(audio_clip)
        clip.write_videofile(new_path + "\\" + str(i) + ".mp4", fps=24, audio_codec="aac")
    items = os.listdir(new_parent)
    lips = []
    for i in range(len(items)):
        clip = VideoFileClip(new_parent + "\\" + str(i) + ".mp4")
        lips.append(clip)
    final_clip = concatenate_videoclips(lips)
    final_clip.write_videofile(new_parent + ".mp4", fps=24, audio_codec="aac")
    for item in lips:
        item.close()
    for i in range(len(items)):
        os.remove(new_parent + "\\" + str(i) + ".mp4")
    draft_content(image_dir_path, audio_dir_path,new_parent)
    return new_path+".mp4"




def remerge_vedio(image_dir_path, audio_dir_path,new_parent):
    # image_files = os.listdir(image_dir_path)
    audio_files = os.listdir(audio_dir_path)
    # clips = []

    if not os.path.exists(new_parent):
        os.makedirs(new_parent)
    for i in range(len(audio_files)):
        image_path = os.path.join(image_dir_path, str(i) + ".png")
        audio_path = os.path.join(audio_dir_path, str(i) + ".wav")
        audio_clip = AudioFileClip(audio_path)
        img_clip = ImageSequenceClip([image_path], audio_clip.duration)
        img_clip = img_clip.set_position(('center', 'center')).fl(fl, apply_to=['mask']).set_duration(
            audio_clip.duration)
        clip = img_clip.set_audio(audio_clip)
        clip.write_videofile(new_parent + "\\" + str(i) + ".mp4", fps=24, audio_codec="aac")
    items = os.listdir(new_parent)
    lips = []
    for i in range(len(items)):
        clip = VideoFileClip(new_parent + "\\" + str(i) + ".mp4")
        lips.append(clip)
    final_clip = concatenate_videoclips(lips)
    final_clip.write_videofile(new_parent + ".mp4", fps=24, audio_codec="aac")
    for item in lips:
        item.close()
    for i in range(len(items)):
        os.remove(new_parent + "\\" + str(i) + ".mp4")
    draft_content(image_dir_path, audio_dir_path, new_parent)
    return new_parent+".mp4"












if __name__ == '__main__':
    # lists =os.listdir('../data/data_image/少年歌行第一章/少年歌行第一章')
    # print(lists)

    merge_vedio("../data/data_image/少年歌行第一章/少年歌行第一章","../data/data_audio/少年歌行第一章/少年歌行第一章")


