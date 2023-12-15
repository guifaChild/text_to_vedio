# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：将语料进行切割，按照中文的句号进行切割，并保存到指定位置
"""

import pandas as pd
import os

def split_data_process(path):
    data_csv_path = ""
    df = pd.read_csv(path)
    for i in range(len(df)):
        type_path = df["type"][i]
        # 读取整段文本 并且按照中文的句号进行切分
        content = df["content"][i].split('。')
        content = [x.strip().replace("\n","") for x in content if len(x.strip()) > 0]
        # 创建新的文件保存切割后的文件
        each_df = pd.DataFrame(content,columns=["text"])
        data_csv_path = os.path.join("data/data_split", type_path)
        if not os.path.exists(data_csv_path):
            os.mkdir(data_csv_path)
        csv_save_path = os.path.join(data_csv_path,df["en_name"][i] + ".csv")
        each_df.to_csv(csv_save_path,index=False)
    return "data/data_split"



if __name__ == '__main__':
    # split_data_process("data/source_data/example.csv")
    print(pd.__version__)
