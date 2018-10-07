f=open('mysite/data/dic/dic_simple','r',encoding='UTF-8')
flag=True
temp=''
dic={}
for line in f.readlines():
    if(flag):
        temp=line[:-1]
        flag=False
    else:
        list=line[:-1].split(" ")[:-1]
        _list=[]
        for string in list:
            _list+=[int(string)]
        dic[temp]=_list
        flag=True