# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年12月08日
描述：
"""
import base64
import json
import os
import io
from PIL import Image
import pandas as pd
import requests




def draw_picture(prompt):

        novel_dict = {"mask":"",
                      "mask_blur":4,
                      "prompt":"Super realistic style,\"},(Super realistic style,\"},：1.5)northeast，%  <lora:FLUX超级玄幻:1> You want me to paint a girl wearing red clothes. \n Girl is standing under blooming cherry blossoms, with pink flowers scattered around her feet. A bright red dress and matching bow decorate the young girls appearance. She has long dark hair styled in relaxed waves, and she gently gazes at something beyond my line of sight, creating a subtle sense of curiosity and innocence","batch_size":1,"steps":10,"cfg_scale":1,"negative_prompt":"bad structure ,Low quality, text，Multiple Canvas， Black border","width":"1056","height":"594","seed":333,"sampler_name":"DPM++ 2M","enable_hr":False,"hr_upscaler":"R-ESRGAN 4x+","hr_second_pass_steps":6,"denoising_strength":0.5,"hr_scale":2.0,"override_settings_restore_afterwards":True,"scheduler":"SGM Uniform"}

        sd_url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
        html = requests.post(sd_url, data=json.dumps(novel_dict))
        img_response = json.loads(html.text)
        image_bytes = base64.b64decode(img_response['images'][0])
        image = Image.open(io.BytesIO(image_bytes))

        # print(image_path)
        image.save("test.png")

if __name__ == '__main__':
    draw_picture("a chinese girl ")
