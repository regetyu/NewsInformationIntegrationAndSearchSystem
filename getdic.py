dic={}
dic_simple={}
for id in range(3000):
    f=open('fenci/fenci_'+str(id),'r',encoding='UTF-8')
    flag=True
    single_list=[]
    str_num=[]
    for line in f.readlines():
        if(flag):
            str_num+=[line[:-1]]
            flag=False
        else:
            str_num+=[int(line[:-1])]
            single_list+=[str_num]
            str_num=[]
            flag=True
    for string_num in single_list:
        if(string_num[0] in dic.keys()):
            dic[string_num[0]]+=([id,string_num[1]])
            dic_simple[string_num[0]]+=[id]
        else:
            dic[string_num[0]]=[id,string_num[1]]
            dic_simple[string_num[0]] = [id]
    print(id)
print(dic_simple)
f2=open('dic/dic_simple','w',encoding='UTF-8')
for i in dic_simple.keys():
    f2.write(i)
    f2.write('\n')
    for num in dic_simple[i]:
        f2.write(str(num))
        f2.write(' ')
    f2.write('\n')