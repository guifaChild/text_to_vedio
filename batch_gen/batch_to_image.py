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
          "mask":"",
          "mask_blur":4,
          "prompt": "{}".format(row["prompt"]),
          "batch_size": 1,
          "steps": 10,
          "cfg_scale": 1,
          "negative_prompt": row["negative"],
          "width": 1056,
          "height": 594,
          "seed": -1,
          "sampler_name": "DPM++ 2M",
          "enable_hr": "false",
          "hr_upscaler": "R-ESRGAN 4x+",
          "hr_second_pass_steps":6,
          "denoising_strength":0.5,
          "override_settings_restore_afterwards": "true",
          "hr_scale": 2,
          "scheduler":"SGM Uniform"


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



if __name__ == '__main__':
    draw_picture("data/data_prompt/侦探悬疑类/story_1.csv")




