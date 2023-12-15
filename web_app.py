# -*- coding:utf-8 -*-
"""
作者：张贵发
日期：2023年07月12日
描述：对应的是web版本
"""
from batch_gen.batch_controller import bach_gen_video
from single_gen.controller import gen_video, remerge_video
from single_gen.single_to_image import regen_video

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
import shutil
from data_split import split_data_process


current_file_path = os.path.abspath(__file__)
# 逐级向上获取上级目录，直到达到项目根目录
project_root = os.path.dirname(current_file_path)
while not os.path.isfile(os.path.join(project_root, 'README.md')):
    project_root = os.path.dirname(project_root)
app = Flask(__name__,static_folder=project_root+"\\static", template_folder=project_root+"\\templates")

"""项目的首页"""
@app.route('/')
def index():
    """首页的路由"""
    return render_template('index_new.html')


"""项目的路由"""
@app.route('/route')
def route():
    """路由设置，所有请求走这里"""
    route_index = request.args.get('route')
    if route_index =='config' :
        data = pd.read_csv(project_root + '\\config\\data_1.csv')
        table = data.to_html(index=False, table_id="my-table",classes='table dt-responsive nowrap')
        return render_template('config.html', table=table)
    if route_index =='file' :
        data = pd.read_csv(project_root + "\\static\\data\\data_source\\data_list\\data_list.csv")
        list = []
        for _, row in data.iterrows():
            list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
        return render_template('file.html', table=list)
    if route_index == 'videoList':
        lists = []
        items = os.listdir(project_root + '\\static\\data\\data_vedio\\')
        for item in items:
            if '2023-' not in item and '2024' not in item:
                content_data = pd.read_csv(project_root + '\\static\\data\\data_split\\' + item + '\\' + item + '.csv')
                content = ','.join(content_data['text'])
                lists.append({'title': item,
                         'content': content,
                         'video_path': project_root + '\\static\\data\\data_vedio\\' + item + '\\' + item + '.mp4',
'video_html_path': 'static/data/data_vedio/' + item + '/' + item + '.mp4'})

        return render_template('videoList.html', table=lists)
    return render_template(route_index+'.html')




"""项目的路由"""
@app.route('/routeHeader')
def routeHeader():
    """路由设置，所有请求走这里"""
    route_Header = request.args.get('routeHeader')

    return render_template(route_Header+'_header.html')





@app.route('/pagetest')
def pagetest():
    """路由设置，所有请求走这里"""
    # route_Header = request.args.get('routeHeader')

    return render_template('index_new_2.html')



@app.route('/save', methods=['POST'])
def save_data():
    table_data = request.json
    df = pd.DataFrame(table_data, columns=['Column1', 'Column2'])  # 替换为实际的列名
    df.to_csv(project_root+'\\config\\data_1.csv', index=False,header=False)  # 将 DataFrame 保存为 CSV 文件

    return '数据保存成功！'


"""浏览器默认打开工程"""
def open_browser():
    print("打开浏览器")
    webbrowser.open('http://localhost:5000')


"""文件上传，可以直接批量生成视频"""
@app.route('/upload', methods=['POST'])
def upload():

    current_date = datetime.now().date()
    print(current_date)
    file = request.files['file']
    wb = load_workbook(file)
    sheet = wb.active
    df = pd.DataFrame(sheet.values)
    filepath = project_root+'\\static\\data\\data_source\\data\\'+str(current_date)+'.csv'
    df.to_csv(filepath, index=False,header=False)

    data = pd.read_csv(project_root+"\\static\\data\\data_source\\data_list\\data_list.csv")
    new_row = {'filename': str(current_date)+'.csv', 'gen_status': '未生成', 'video_path': '无'}
    data = data.append(new_row, ignore_index=True)
    data.to_csv(project_root+"\\static\\data\\data_source\\data_list\\data_list.csv",  index=False)

    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)

    # return '文件上传成功！'



"""根据id删除指定的数据"""
@app.route('/delete', methods=['POST'])
def delete_row():
    data = pd.read_csv(project_root+'\\static\\data\\data_source\\data_list\\data_list.csv')
    row_index = int(request.form['index'])  # 获取要删除的行索引
    data.drop(row_index, inplace=True)  # 从 Pandas 数据中删除行
    data.reset_index(drop=True, inplace=True)  # 重新设置索引
    data.to_csv(project_root+'\\static\\data\\data_source\\data_list\\data_list.csv', index=False)  # 保存更新后的数据到文件
    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)


"""查看数据"""
@app.route('/view', methods=['GET'])
def viewRow():
    data = pd.read_csv(project_root+'\\static\\data\\data_source\\data_list\\data_list.csv')
    new_index = int(request.args.get('index'))
    # 根据索引获取指定行数据
    row = data.iloc[new_index][0]
    # 返回 JSON 格式的数据y
    file_path=project_root+'\\static\\data\\data_source\\data\\'+row
    pdata = pd.read_csv(file_path)
    pdata.fillna("", inplace=True)
    # pdata=pdata.to_dict(orient='records')
    file_title = row.split('.csv')[0]
    lists = []
    pdata['video_html_path'] = 'static/data/data_vedio/' + file_title + '/' + pdata['title'].astype(str) + '.mp4'
    for _, row in pdata.iterrows():
        lists.append({'title': row['title'], 'content': row['content'], 'video_html_path': row['video_html_path']})

    return render_template('fileList.html', table=lists)



"""单个视频的生成"""
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

@app.route('/show_detail', methods=['GET'])
def show_detail():
    title = request.args.get('title')
    data = pd.read_csv(project_root + '\\static\\data\\data_prompt\\'+title+'\\'+title+'.csv')
    data['image_path'] = 'static/data/data_image/'+title+'/'+title+'/' + data['index'].astype(str)+'.png'
    data['tts_path'] = 'static/data/data_audio/'+title+'/'+title+'/' + data['index'].astype(str)+'.wav'
    data.fillna("", inplace=True)
    list = []
    for _, row in data.iterrows():
        list.append({'text': row['text'], 'index': row['index'], 'prompt': row['prompt'], 'negative': row['negative'],  'image_path': row['image_path'], 'tts_path': row['tts_path']})
    vedio_path = project_root + '\\static\\data\\data_vedio\\'+title+'\\'+title+'.mp4'
    vedio_html_path = 'static/data/data_vedio/' + title + '/' + title + '.mp4'
    return render_template('detail.html', table=list,vedio_path=vedio_path,vedio_html_path=vedio_html_path)

@app.route('/deleteDetail', methods=['GET'])
def deleteDetail():
    title = request.args.get('title')
    try:
        shutil.rmtree(project_root + '\\static\\data\\data_vedio\\'+title)
        shutil.rmtree(project_root + '\\static\\data\\data_audio\\' + title)
        shutil.rmtree(project_root + '\\static\\data\\data_image\\' + title)
        shutil.rmtree(project_root + '\\static\\data\\data_prompt\\' + title)
        shutil.rmtree(project_root + '\\static\\data\\data_split\\' + title)
        shutil.rmtree(project_root + '\\static\\data\\source_data\\' + title)
    except:
        lists = []
        items = os.listdir(project_root + '\\static\\data\\data_vedio\\')
        for item in items:
            if '2023-' not in item and '2024' not in item:
                content_data = pd.read_csv(project_root + '\\static\\data\\data_split\\' + item + '\\' + item + '.csv')
                content = ','.join(content_data['text'])
                lists.append({'title': item,
                              'content': content,
                              'video_path': project_root + '\\static\\data\\data_vedio\\' + item + '\\' + item + '.mp4',
                              'video_html_path': 'static/data/data_vedio/' + item + '/' + item + '.mp4'})
        return render_template('videoList.html', table=lists)
    lists = []
    items = os.listdir(project_root + '\\static\\data\\data_vedio\\')
    for item in items:
        if '2023-' not in item and '2024' not in item:
            content_data = pd.read_csv(project_root + '\\static\\data\\data_split\\' + item + '\\' + item + '.csv')
            content = ','.join(content_data['text'])
            lists.append({'title': item,
                          'content': content,
                          'video_path': project_root + '\\static\\data\\data_vedio\\' + item + '\\' + item + '.mp4',
                          'video_html_path': 'static/data/data_vedio/' + item + '/' + item + '.mp4'})

    return render_template('videoList.html', table=lists)

@app.route('/show_filedetail', methods=['GET'])
def show_batch_detail():
    title = request.args.get('title')
    filename = request.args.get('filename')
    data = pd.read_csv(project_root + '\\static\\data\\data_prompt\\'+filename+'\\'+title+'.csv')
    data['image_path'] = 'static/data/data_image/'+filename+'/'+title+'/' + data['index'].astype(str)+'.png'
    data['tts_path'] = 'static/data/data_audio/'+filename+'/'+title+'/' + data['index'].astype(str)+'.wav'
    data.fillna("", inplace=True)
    list = []
    for _, row in data.iterrows():
        list.append({'text': row['text'], 'index': row['index'], 'prompt': row['prompt'], 'negative': row['negative'],  'image_path': row['image_path'], 'tts_path': row['tts_path']})
    vedio_path = project_root + '\\static\\data\\data_vedio\\'+filename+'\\'+title+'.mp4'
    vedio_html_path = 'static/data/data_vedio/' + filename + '/' + title + '.mp4'
    return render_template('filedetail.html', table=list,vedio_path=vedio_path,vedio_html_path=vedio_html_path)









"""批量视频的生成"""
@app.route('/batch', methods=['GET'])
def batch_gen_video():
    data = pd.read_csv(project_root+'\\static\\data\\data_source\\data_list\\data_list.csv')
    new_index = int(request.args.get('index'))
    # 根据索引获取指定行数据
    row = data.iloc[new_index][0]
    # 返回 JSON 格式的数据
    file_path = project_root+'\\static\\data\\data_source\\data\\' + row
    video_path = bach_gen_video(file_path,row)

    data.iloc[new_index, 1]='已生成'
    data.iloc[new_index, 2] = video_path
    data.to_csv(project_root+"\\static\\data\\data_source\\data_list\\data_list.csv",  index=False)
    list = []
    for _, row in data.iterrows():
        list.append({'filename': row['filename'], 'gen_status': row['gen_status'], 'video_path': row['video_path']})
    return render_template('file.html', table=list)


"""单个视频的生成"""
@app.route('/regenerate', methods=['POST'])
def regenerate():
    data = request.get_json()
    imageprompt = data.get('imageprompt')
    imagenegitve = data.get('imagenegitve')
    index = data.get('index')
    title = data.get('title')
    # 根据索引获取指定行数据
    # 返回 JSON 格式的数据
    newpath = project_root + '\\static\\data\\data_image\\' + title + '\\' + title + "\\"+str(index)+'.png'
    video_path = regen_video(imageprompt,imagenegitve,newpath)

    return jsonify(video_path)




@app.route('/rebatchgenerate', methods=['POST'])
def rebatchgenerate():
    data = request.get_json()
    imageprompt = data.get('imageprompt')
    imagenegitve = data.get('imagenegitve')
    index = data.get('index')
    title = data.get('title')
    filename = data.get('filename')
    # 根据索引获取指定行数据
    # 返回 JSON 格式的数据
    newpath = project_root + '\\static\\data\\data_image\\' + filename + '\\' + title + "\\"+str(index)+'.png'
    video_path = regen_video(imageprompt,imagenegitve,newpath)

    return jsonify(video_path)

@app.route('/remerge', methods=['POST'])
def remerge():
    data = request.get_json()
    video_html_path = data.get('image_path')
    path = str(video_html_path).split('.mp4')[0]
    path_item = path.split("/")
    audeo_path = ""
    image_path = ""
    vedio_path = ""
    title =""
    filename =""
    if path_item[-1] == path_item[-2]:
        title=path_item[-1]
        audeo_path = project_root + '\\static\\data\\data_audio\\' + title + '\\' + title
        image_path =  project_root + '\\static\\data\\data_image\\' + title + '\\' + title
        vedio_path =  project_root + '\\static\\data\\data_vedio\\' + title + '\\' + title
    else :
        title = path_item[-1]
        filename = path_item[-2]
        audeo_path = project_root + '\\static\\data\\data_audio\\' + filename + '\\' + title
        image_path = project_root + '\\static\\data\\data_image\\' + filename + '\\' + title
        vedio_path = project_root + '\\static\\data\\data_vedio\\' + filename + '\\' + title
    return remerge_video(image_path,audeo_path,vedio_path)






if __name__ == '__main__':
    # 创建一个新线程来打开浏览器
    thread = threading.Timer(1,open_browser)
    thread.start()
    app.run()
    # load_data()