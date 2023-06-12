# -*- coding: utf-8 -*-
"""
作者：张贵发
日期：2023年06月12日
描述：批量生成视频
"""
from data_split import *
from data_promt_words import *
from data_tts import *
from data_to_image import *
from data_to_vedio import *
# 0、准备语料。
# 1、切割源文件，句号分割语料，形成新的文件。
# 2、利用chatglm生成提示词，prompt negative。
# 3、利用第1步的语料，调用tts的api生成语音。
# 4、利用第2步生成提示词，调用stable diffusion的api生成图片。
# 5、将第3步的语音和第4步的图片合成视频。


def xunhuan_list(path):
    filename = [ os.path.join(path, item) for item in os.listdir(path)]
    result =[]
    for item in filename :
        item_list =os.listdir(item)
        for line in item_list :
            result.append(os.path.join(item,line))

    return result


def batch_merge(ource_file_path):
    #切割源文件，句号分割语料，形成新的文件。
    csv_save_path = split_data_process(ource_file_path)
    print("数据切割完成")
    name_list = xunhuan_list(csv_save_path)
    for item in name_list:
        #利用chatglm生成提示词，prompt negative。
        data_promt_path = load_data_text(item)
        print("提示词生成完成")
        #利用第1步的语料，调用tts的api生成语音。
        tts_path = load_source_data_text(item)
        print("语音生成完成")
        #利用第2步生成提示词，调用stable diffusion的api生成图片。
        image_dir =draw_picture(data_promt_path)
        print("图片生成完成")
        #将第3步的语音和第4步的图片合成视频。
        vedio_path = merge_vedio(image_dir,tts_path)
        print("--------视频生成成功，路径是{}-------------".format(vedio_path))




if __name__ == '__main__':
    # 定义源文件的路径
    vedio_path = batch_merge('data/source_data/example1.csv')



