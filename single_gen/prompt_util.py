# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2024年07月30日
描述：
"""
# 风格处理、提示词处理、年代处理、

import json
import os
# 假设您有一个名为 'data.json' 的JSON文件
current_file_path = os.path.abspath(__file__)

# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)

file_path = project_root+'\\config\\prompt_json.json'

# 使用with语句确保文件会被正确关闭
with open(file_path, 'r', encoding='utf-8') as file:
    # 使用json.load()函数加载JSON数据
    dict_data = json.load(file)


# 文本翻译
def translate(text):
    for key in sorted(dict_data.keys(), key=lambda k: len(k), reverse=True):
        if key in text:
            text = text.replace(key, ' ' + dict_data[key] + ' ')
    return text


def char_convert(text):
    if "5830" in text and "" in text and "【" in text:
        return False
    else:
        return True



def style_component(text):
    pass

def append_all_items():
    pass



