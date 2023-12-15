# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：根据生成的prompt提示词来生成对应的图片
"""
import base64
import json
import os
import io
from PIL import Image
import pandas as pd
import requests




def draw_picture(path):
    df = pd.read_csv(path)
    for index,row in df.iterrows():
        novel_dict = {
          "enable_hr": "false",
          "denoising_strength": 0,
          "firstphase_width": 0,
          "firstphase_height": 0,
          "hr_scale": 2,
          "hr_upscaler": "string",
          "hr_second_pass_steps": 0,
          "hr_resize_x": 0,
          "hr_resize_y": 0,
          "prompt": "{}".format(row["prompt"]),
          "styles": [
            "string"
          ],
          "seed": -1,
          "subseed": -1,
          "subseed_strength": 0,
          "seed_resize_from_h": -1,
          "seed_resize_from_w": -1,
          "sampler_name": "DPM++ SDE Karras",
          "batch_size": 1,
          "n_iter": 1,
          "steps": 50,
          "cfg_scale": 7,
          "width": 1024,
          "height": 768,
          "restore_faces": "false",
          "tiling": "false",
          "do_not_save_samples": "false",
          "do_not_save_grid": "false",
          "negative_prompt": row["negative"],
          "eta": 0,
          "s_churn": 0,
          "s_tmax": 0,
          "s_tmin": 0,
          "s_noise": 1,
          "override_settings": {},
          "override_settings_restore_afterwards": "true",
          "script_args": [],
          "sampler_index": "DPM++ SDE Karras",
          "script_name": "",
          "send_images": "true",
          "save_images": "true",
          "alwayson_scripts": {}
        }

        sd_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
        html = requests.post(sd_url, data=json.dumps(novel_dict))
        img_response = json.loads(html.text)
        image_bytes = base64.b64decode(img_response['images'][0])
        image = Image.open(io.BytesIO(image_bytes))
        new_path = path.split(".csv")[0].replace("data_prompt","data_image")
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        image_path = os.path.join(new_path,str(index)+".png")
        # print(image_path)
        image.save(image_path)
    return new_path








def regen_video(imageprompt,imagenegitve,newpath):

    novel_dict = {
      "enable_hr": "false",
      "denoising_strength": 0,
      "firstphase_width": 0,
      "firstphase_height": 0,
      "hr_scale": 2,
      "hr_upscaler": "string",
      "hr_second_pass_steps": 0,
      "hr_resize_x": 0,
      "hr_resize_y": 0,
      "prompt": "{}".format(imageprompt),
      "styles": [
        "string"
      ],
      "seed": -1,
      "subseed": -1,
      "subseed_strength": 0,
      "seed_resize_from_h": -1,
      "seed_resize_from_w": -1,
      "sampler_name": "DPM++ SDE Karras",
      "batch_size": 1,
      "n_iter": 1,
      "steps": 50,
      "cfg_scale": 7,
      "width": 1024,
      "height": 768,
      "restore_faces": "false",
      "tiling": "false",
      "do_not_save_samples": "false",
      "do_not_save_grid": "false",
      "negative_prompt": imagenegitve,
      "eta": 0,
      "s_churn": 0,
      "s_tmax": 0,
      "s_tmin": 0,
      "s_noise": 1,
      "override_settings": {},
      "override_settings_restore_afterwards": "true",
      "script_args": [],
      "sampler_index": "DPM++ SDE Karras",
      "script_name": "",
      "send_images": "true",
      "save_images": "true",
      "alwayson_scripts": {}
    }

    sd_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    html = requests.post(sd_url, data=json.dumps(novel_dict))
    img_response = json.loads(html.text)
    image_bytes = base64.b64decode(img_response['images'][0])
    image = Image.open(io.BytesIO(image_bytes))

    # print(image_path)
    image.save(newpath)
    return newpath





























if __name__ == '__main__':
    draw_picture("data/data_prompt/侦探悬疑类/story_1.csv")




