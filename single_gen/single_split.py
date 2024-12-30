# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：将语料进行切割，按照中文的句号进行切割，并保存到指定位置
"""

import pandas as pd
import os
import re
def split_data_process_old(path):

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


def split_data_process(path):
    # 读取CSV文件，去除空白行
    df = pd.read_csv(path)
    df.dropna(inplace=True)  # 去除空白行

    results = []  # 用于存储最终结果

    for _, row in df.iterrows():
        # 按照中英文句号保留分隔符进行分割
        segments = [seg + '.' for seg in re.split('(?<=[。.])', row['content']) if len(seg.strip()) > 0]

        for segment in segments:
            # 检查长度并按需进一步分割
            if len(segment) > 30:
                sub_segments = [sub_seg + ',' for sub_seg in re.split('(?<=[,，])', segment) if len(sub_seg.strip()) > 0]
                # 处理逗号分割后仍过长的情况
                for sub in sub_segments:
                    if len(sub) > 30:
                        chunk_size = 10
                        chunks = [sub[i:i + chunk_size] for i in range(0, len(sub), chunk_size)]
                        results.extend(chunks)
                    else:
                        results.append(sub)
            else:
                results.append(segment)

    # 处理长度小于5的情况，将其合并到前一条内容
    final_results = []
    for text in results:
        if len(text) < 5 and final_results:
            final_results[-1] += text
        else:
            final_results.append(text)

    # 写入新的CSV文件
    final_df = pd.DataFrame(final_results, columns=["text"])
    final_df.to_csv("split_contents.csv", index=False)
#
#
# return "data/data_split"



if __name__ == '__main__':
    split_data_process_old("../static/data/source_data/zuizhong.csv")
    print(pd.__version__)
