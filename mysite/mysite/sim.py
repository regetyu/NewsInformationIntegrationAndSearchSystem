f=open('mysite/data/similarity/sim','r',encoding='UTF-8')
dic_sim={}
i=0
for line in f.readlines():
    dic_sim[i]=(line.split())
    i+=1
