with open("南关园区勘界图.txt",'r',encoding='utf-8')  as file:
    lines = file.readlines()
    for line in lines :
        wei,jing= line.split(' ')[1],line.split(' ')[2]

        print('['+wei+','+jing+'],')

