# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年12月08日
描述：
"""

import asyncio
import os
from auto_upload import main
import datetime
import json


def count_get(video_path):
    acount_path = video_path.replace("data_vedio","data_source\\data")
    current_date = datetime.now().date()
    print(current_date)
    with open(os.path.join(acount_path,str(current_date)+".json"), 'r') as f:
        data = json.load(f)
    return data
def auto_upload(video_path):
    video_items = [os.path.join(video_path, item) for item in os.listdir(video_path) if item.endswith(".mp4")]
    acount_data= count_get(video_path)

    for video_item in video_items:
        base_name = os.path.basename(video_item)
        file_name_without_extension = os.path.splitext(base_name)[0]
        asyncio.run(main(platform="douyin", account_name=acount_data[file_name_without_extension], action="upload", video_file=video_item,
                                     publish_type=0))

    print("上传成功")




if __name__ == '__main__':
    auto_upload("D:\\workspace\\sft\\text_to_video\\text_to_vedio\\static\\data\\data_vedio\\2024-12-26")
