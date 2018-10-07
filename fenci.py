import jieba
id=0
for id in range(3000):
    dic={}
    fen_title=[]
    fen_text=[]
    f=open('爬虫/'+str(id),'r',encoding='UTF-8')
    title=f.readline()
    temp_title=(jieba.cut_for_search(title))
    f.readline()
    text=f.read()
    temp_text=jieba.cut_for_search(text)
    for i in temp_title:
        if(i!=' ' and i!='\n'):
            fen_title+=[i]
    for i in temp_text:
        if(i!=' ' and i!='\n'and i!= '\u3000'):
            fen_text+=[i]
    for string in fen_title:
        if(string in dic.keys()):
            dic[string]+=1
        else:
            dic[string]=1
    for string in fen_text:
        if(string in dic.keys()):
            dic[string]+=1
        else:
            dic[string]=1
    f2=open('fenci/fenci_'+str(id),'w',encoding='UTF-8')
    for key in dic.keys():
        f2.write(key)
        f2.write('\n')
        f2.write(str(dic[key]))
        f2.write('\n')
    print(id)