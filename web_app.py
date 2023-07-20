# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月12日
描述：对应的是web版本
"""
from batch_gen.batch_controller import bach_gen_video
from single_gen.controller import gen_video

# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月7日
描述：项目启动项

"""
from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import os
from data_split import split_data_process


current_file_path = os.path.abspath(__file__)
# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)

app = Flask(__name__,static_folder=project_root+"\\static", template_folder=project_root+"\\templates")


@app.route('/')
def index():
    data = pd.read_csv(project_root+'\\config\\data_1.csv')
    table = data.to_html(index=False, table_id="my-table")
    return render_template('index.html',table=table)


@app.route('/config')
def config():
    data = pd.read_csv(project_root+'\\config\\data_1.csv')
    table = data.to_html(index=False, table_id="my-table")
    return render_template('config.html',table=table)



@app.route('/optimization')
def optimization():
    return render_template('optimization.html')
@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/file')
def file():
    data = pd.read_csv(project_root+"\\data\\data_source\\data_list\\data_list.csv")
    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)


@app.route('/save', methods=['POST'])
def save_data():
    table_data = request.json
    df = pd.DataFrame(table_data, columns=['Column1', 'Column2'])  # 替换为实际的列名
    df.to_csv(project_root+'\\config\\data_1.csv', index=False,header=False)  # 将 DataFrame 保存为 CSV 文件

    return '数据保存成功！'




def load_data():
    data = pd.read_csv(project_root+"\\config\\data_1.csv")
    return data

def open_browser():
    print("打开浏览器")
    webbrowser.open('http://localhost:5000')



@app.route('/upload', methods=['POST'])
def upload():


    current_date = datetime.now().date()
    print(current_date)
    file = request.files['file']
    wb = load_workbook(file)
    sheet = wb.active
    df = pd.DataFrame(sheet.values)
    filepath = project_root+'\\data\\data_source\\data\\'+str(current_date)+'.csv'
    df.to_csv(filepath, index=False,header=False)

    data = pd.read_csv(project_root+"\\data\\data_source\\data_list\\data_list.csv")
    new_row = {'filename': str(current_date)+'.csv', 'gen_status': '未生成', 'video_path': '无'}
    data = data.append(new_row, ignore_index=True)
    data.to_csv(project_root+"\\data\\data_source\\data_list\\data_list.csv",  index=False)

    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)

    # return '文件上传成功！'




@app.route('/delete', methods=['POST'])
def delete_row():
    data = pd.read_csv(project_root+'\\data\\data_source\\data_list\\data_list.csv')
    row_index = int(request.form['index'])  # 获取要删除的行索引
    data.drop(row_index, inplace=True)  # 从 Pandas 数据中删除行
    data.reset_index(drop=True, inplace=True)  # 重新设置索引
    data.to_csv(project_root+'\\data\\data_source\\data_list\\data_list.csv', index=False)  # 保存更新后的数据到文件
    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)

@app.route('/view', methods=['GET'])
def viewRow():
    data = pd.read_csv(project_root+'\\data\\data_source\\data_list\\data_list.csv')
    new_index = int(request.args.get('index'))
    # 根据索引获取指定行数据
    row = data.iloc[new_index][0]
    # 返回 JSON 格式的数据y
    file_path=project_root+'\\data\\data_source\\data\\'+row

    pdata = pd.read_csv(file_path)
    pdata.fillna("", inplace=True)
    pdata=pdata.to_dict(orient='records')
    return jsonify(pdata)


@app.route('/single', methods=['POST'])
def single_gen_video():
    data = request.get_json()
    title = data.get('title')
    title = title.replace(" ", "").replace(" ", "")
    content = data.get('content')
    content = content.replace(" ", "").replace(" ", "")
    # 根据索引获取指定行数据

    # 返回 JSON 格式的数据
    video_path = gen_video(title,content)
    return jsonify(video_path)



@app.route('/batch', methods=['GET'])
def batch_gen_video():
    data = pd.read_csv(project_root+'\\data\\data_source\\data_list\\data_list.csv')
    new_index = int(request.args.get('index'))
    # 根据索引获取指定行数据
    row = data.iloc[new_index][0]
    # 返回 JSON 格式的数据
    file_path = project_root+'\\data\\data_source\\data\\' + row
    video_path = bach_gen_video(file_path,row)

    data.iloc[new_index, 1]='已生成'
    data.iloc[new_index, 2] = video_path
    data.to_csv(project_root+"\\data\\data_source\\data_list\\data_list.csv",  index=False)
    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)







if __name__ == '__main__':
    # 创建一个新线程来打开浏览器
    thread = threading.Timer(1,open_browser)
    thread.start()
    app.run()
    # load_data()