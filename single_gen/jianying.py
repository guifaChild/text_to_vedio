# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年01月26日
描述：
"""
import json
import os
import uuid
import pandas as pd

from moviepy.audio.io.AudioFileClip import AudioFileClip

current_file_path = os.path.abspath(__file__)

# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)



pdata = project_root+'\\config\\draft_content.json'
def generate_id():
    return str(uuid.uuid4()).upper()


def load_template(image_dir_path,audio_dir_path):
    false = False
    true =True
    null = None
    with open(pdata,encoding="utf-8") as f:
        data = json.loads(f.read())
    # 为文件id附上值
    image_files = os.listdir(image_dir_path)
    audio_files = os.listdir(audio_dir_path)

    new_parent = image_dir_path.replace("data_image", "data_vedio")
    df = pd.DataFrame(columns=['id', 'image_path', 'audio_path', 'duration', 'image_id', 'audio_id', 'canvas_id', 'speed_1_id', 'speed_2_id', 'animation_id','beat_id'])
    for i in range(len(audio_files)):
        image_path = os.path.join(image_dir_path, str(i) + ".png")
        audio_path = os.path.join(audio_dir_path, str(i) + ".wav")
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration
        new_row = {'id': 1, 'image_path': image_path, 'audio_path': audio_path, 'duration': duration * 1000000, 'image_id': generate_id(),
                   'audio_id': generate_id(), 'canvas_id': generate_id(), 'speed_1_id': generate_id(), 'speed_2_id': generate_id(),
                   'animation_id':generate_id(), 'beat_id':generate_id()
                   }
        df=df.append(new_row,ignore_index=True)


    # 设置id属性
    # print(df['duration'].head(10))
    data["id"] =generate_id()

    # n = df.index.max() +1
    #
    data["duration"] = int(df["duration"].sum())
    # # 生成画布
    convases = []
    # 里面的id设置  extra_material_refs中有用到
    for i in range(len(audio_files)):
        convase= {
        "album_image": "",
        "blur": 0.0,
        "color": "",
        "id": df['canvas_id'].iloc[i],
        "image": "",
        "image_id": "",
        "image_name": "",
        "source_platform": 0,
        "team_id": "",
        "type": "canvas_color"
      }
        convases.append(convase)
    data["materials"]["canvases"]=convases
    # # 生成画布动画
    material_animations =[]
    for i in range(len(audio_files)):
        animation= {
        "animations": [],
        "id": df['animation_id'].iloc[i],
        "type": "sticker_animation"
      }
        material_animations.append(animation)
    data["materials"]["material_animations"]=material_animations
    #
    # # 生成速度配置
    speeds =[]
    for i in range(len(audio_files)):
        speed= {
        "curve_speed": null,
        "id": df['speed_1_id'].iloc[i],
        "mode": 0,
        "speed": 1.0,
        "type": "speed"
      }
        speeds.append(speed)
        speed = {
            "curve_speed": null,
            "id": df['speed_2_id'].iloc[i],
            "mode": 0,
            "speed": 1.0,
            "type": "speed"
        }
        speeds.append(speed)
    data["materials"]["speeds"]=speeds
    #
    # # 生成文本
    texts =[]
    # for i in range(1):
    #     pass
    data["materials"]["texts"]=texts
    #
    # # 视频轨道
    video_trackings =[]
    # for i in range(n):
    #     pass
    data["materials"]["video_trackings"]=video_trackings
    #
    # # 视频轨道
    videos =[]
    for i in range(len(audio_files)):
        video=  {
        "audio_fade": null,
        "cartoon_path": "",
        "category_id": "",
        "category_name": "local",
        "check_flag": 63487,
        "crop": {
          "lower_left_x": 0.0,
          "lower_left_y": 1.0,
          "lower_right_x": 1.0,
          "lower_right_y": 1.0,
          "upper_left_x": 0.0,
          "upper_left_y": 0.0,
          "upper_right_x": 1.0,
          "upper_right_y": 0.0
        },
        "crop_ratio": "free",
        "crop_scale": 1.0,
        "duration": int(df['duration'].iloc[i]),
        "extra_type_option": 0,
        "formula_id": "",
        "freeze": null,
        "gameplay": null,
        "has_audio": false,
        "height": 768,
        "id": df['image_id'].iloc[i],
        "intensifies_audio_path": "",
        "intensifies_path": "",
        "is_unified_beauty_mode": false,
        "local_id": "",
        "local_material_id": "",
        "material_id": "",
        "material_name": str(i)+".png",
        "material_url": "",
        "matting": {
          "flag": 0,
          "has_use_quick_brush": false,
          "has_use_quick_eraser": false,
          "interactiveTime": [],
          "path": "",
          "strokes": []
        },
        "media_path": "",
        "object_locked": null,
        "path": df['image_path'].iloc[i],
        "picture_from": "none",
        "picture_set_category_id": "",
        "picture_set_category_name": "",
        "reverse_intensifies_path": "",
        "reverse_path": "",
        "source_platform": 0,
        "stable": null,
        "team_id": "",
        "type": "photo",
        "video_algorithm": {
          "algorithms": [],
          "deflicker": null,
          "motion_blur_config": null,
          "noise_reduction": null,
          "path": "",
          "time_range": null
        },
        "width": 1024
      }
        videos.append(video)
    data["materials"]["videos"]=videos
    #

    audios = []
    for i in range(len(audio_files)):
        audio =  {
        "app_id": 0,
        "category_id": "",
        "category_name": "local",
        "check_flag": 1,
        "duration": int(df['duration'].iloc[i]),
        "effect_id": "",
        "formula_id": "",
        "id": df['audio_id'].iloc[i],
        "intensifies_path": "",
        "local_material_id": generate_id(),
        "music_id": generate_id(),
        "name": str(i)+".wav",
        "path": df['audio_path'].iloc[i],
        "resource_id": "",
        "source_platform": 0,
        "team_id": "",
        "text_id": "",
        "tone_category_id": "",
        "tone_category_name": "",
        "tone_effect_id": "",
        "tone_effect_name": "",
        "tone_speaker": "",
        "tone_type": "",
        "type": "extract_music",
        "video_id": "",
        "wave_points": []
      }
        audios.append(audio)
    data["materials"]["audios"] = audios


    #
    # # tracks 轨道主线
    #

    tracks = [
            {
              "attribute": 0,
              "flag": 0,
              "id": generate_id(),
              "segments": [],
              "type": "video"
            },
            {
              "attribute": 0,
              "flag": 0,
              "id": generate_id(),
              "segments": [],
              "type": "audio"
            }
        ]
    data["tracks"] = tracks
    segment1=[]
    duration_length_image = 0
    for i in range(len(audio_files)):
        segment =  {
          "cartoon": false,
          "clip": {
            "alpha": 1.0,
            "flip": {
              "horizontal": false,
              "vertical": false
            },
            "rotation": 0.0,
            "scale": {
              "x": 1.0,
              "y": 1.0
            },
            "transform": {
              "x": 0.0,
              "y": 0.0
            }
          },
          "enable_adjust": true,
          "enable_color_curves": true,
          "enable_color_wheels": true,
          "enable_lut": true,
          "enable_smart_color_adjust": false,
          "extra_material_refs": [
            df['speed_1_id'].iloc[i],
            df['canvas_id'].iloc[i],
            df['animation_id'].iloc[i],
            df['animation_id'].iloc[i],
          ],
          "group_id": "",
          "hdr_settings": {
            "intensity": 1.0,
            "mode": 1,
            "nits": 1000
          },
          "id": generate_id(),
          "intensifies_audio": false,
          "is_placeholder": false,
          "is_tone_modify": false,
          "keyframe_refs": [],
          "last_nonzero_volume": 1.0,
          "material_id": df['image_id'].iloc[i],
          "render_index": 0,
          "reverse": false,
          "source_timerange": {
            "duration": df['duration'].iloc[i],
            "start": 0
          },
          "speed": 1.0,
          "target_timerange": {
            "duration": df['duration'].iloc[i],
            "start": duration_length_image
          },
          "template_id": "",
          "template_scene": "default",
          "track_attribute": 0,
          "track_render_index": 0,
          "visible": true,
          "volume": 1.0
        }


        segment1.append(segment)
        duration_length_image=duration_length_image+df['duration'].iloc[i]
    data["tracks"][0]["segments"]=segment1
    segment2=[]
    duration_length = 0
    for i in range(len(audio_files)):

        segment={
          "cartoon": false,
          "clip": null,
          "enable_adjust": false,
          "enable_color_curves": true,
          "enable_color_wheels": true,
          "enable_lut": false,
          "enable_smart_color_adjust": false,
          "extra_material_refs": [
            df['speed_2_id'].iloc[i],
            df['speed_2_id'].iloc[i],
            df['speed_2_id'].iloc[i],
          ],
          "group_id": "",
          "hdr_settings": null,
          "id": generate_id(),
          "intensifies_audio": false,
          "is_placeholder": false,
          "is_tone_modify": false,
          "keyframe_refs": [],
          "last_nonzero_volume": 1.0,
          "material_id":df['audio_id'].iloc[i],
          "render_index": 0,
          "reverse": false,
          "source_timerange": {
            "duration":  df['duration'].iloc[i],
            "start":  0
          },
          "speed": 1.0,
          "target_timerange": {
            "duration":  df['duration'].iloc[i],
            "start": duration_length
          },
          "template_id": "",
          "template_scene": "default",
          "track_attribute": 0,
          "track_render_index": 0,
          "visible": true,
          "volume": 1.0
        }

        segment2.append(segment)
        duration_length = duration_length + df['duration'].iloc[i]
    data["tracks"][1]["segments"]=segment2
    # print(data)
    result_txt = json.dumps(data)
    # print(result_txt)
    return result_txt


def draft_content(imagepath, audio_path,new_parent_path):
    result_txt = load_template(imagepath, audio_path)
    with open(new_parent_path+"\\"+"draft_content.json","w+",encoding="utf-8") as file:
        file.write(result_txt)

def save_data_json(result_txt):
    with open("zuixin/draft_content.json","w+",encoding="utf-8") as file:
        file.write(result_txt)

def name_make_dir(name):
    os.makedirs(name)

if __name__ == '__main__':
    # name_make_dir("zuixin")
    # result_txt =load_template("D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_image\\最新的例子测试\\最新的例子测试","D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_audio\\最新的例子测试\\最新的例子测试")
    # result_txt = load_template(
    #     "D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_image\\move\\move",
    #     "D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_audio\\move\\move")
    #
    # save_data_json(result_txt)
    draft_content()
