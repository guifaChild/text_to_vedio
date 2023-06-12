with open("zd.txt",'r',encoding='utf-8') as file:
    for line in file.readlines():
        name = line.split('.《')[1].split('["group1",')[0]
        url  =  line.split('.《')[1].split('["group1",')[1].split(']')[0]
        print(name,url)