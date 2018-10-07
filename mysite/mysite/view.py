# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render
import jieba
from mysite import data
from django.http import HttpResponse
from mysite import  sim
import time

class Text:
    def __init__(self,title,time,content,id,link):
        self.title=title
        self.time=time
        self.content=content
        self.id=id
        self.link=link


def search_form(request):
    context = {}
    context['title'] = '新浪新闻检索'
    context['search_title'] = '新浪新闻检索'
    return render(request, 'search_form.html', context)

def search(request):
    if(request.POST):
        time1 = time.time()
        context={}
        context['title'] ='搜索结果'
        string=request.POST['content']
        context['keywords']=string
        if request.POST['content'] not in data.dic.keys():
            temp = {}
            temp['title'] = "找不到搜索结果"
            temp['text'] = r'没有找到"' + string + r'"的结果'
            return render(request, 'search_error.html', temp)
        else:
            list=data.dic[request.POST['content']]
            Textlist=[]
            if(len(list)<=10):
                for num in list:
                    f=open('mysite/data/content/'+str(num),'r',encoding='UTF-8')
                    content = []
                    title = f.readline()
                    _time = f.readline()
                    for line in f.readlines():
                        content+=[line]
                    link='/page/'+str(num)
                    Textlist +=[Text(title,_time,content,num,link)]
            else:
                for i in range(10):
                    f = open('mysite/data/content/' + str(list[i]), 'r', encoding='UTF-8')
                    content = []
                    title = f.readline()
                    _time = f.readline()
                    for line in f.readlines():
                        content += [line]
                    link = '/page/' + str(list[i])
                    Textlist += [Text(title, _time, content, list[i], link)]
            time2=time.time()
            search_time=time2-time1
            context['Textlist']=Textlist
            context['search_title']=r'"'+string+r'"的搜索结果'
            context['search_time']='本次搜索耗时'+str(search_time)+'秒'
            context['search_num']='共找到'+str(len(list))+'条结果'
            context['front_page_link']='search/'+string+'/1'
            context['last_page_link']='search/'+string+'/1'
            context['next_page_link']='search/'+string+'/2'
            context['end_page_link']='search/'+string+'/'+str((len(list)-1)//10+1)
            context['page']='1'
            context['total_page']=str((len(list)-1)//10+1)
            return render(request, 'search.html',context)

def page(request,id):
    context={}
    f=open('mysite/data/content/'+id,'r',encoding='UTF-8')
    content = []
    title = f.readline()
    time = f.readline()
    for line in f.readlines():
        content += [line]
    link = '/page/' + str(id)
    article=Text(title,time,content,int(id),link)
    context['title']=title
    context['Text']=article
    list=sim.dic_sim[int(id)]
    f1 = open('mysite/data/content/' + str(list[0]), 'r', encoding='UTF-8')
    title1=f1.readline()
    link1='/page/'+str(list[0])
    f2 = open('mysite/data/content/' + str(list[1]), 'r', encoding='UTF-8')
    title2 = f2.readline()
    link2 = '/page/' + str(list[1])
    f3 = open('mysite/data/content/' + str(list[2]), 'r', encoding='UTF-8')
    title3 = f3.readline()
    link3 = '/page/' + str(list[2])
    context['title1']=title1
    context['link1']=link1
    context['title2'] = title2
    context['link2'] = link2
    context['title3'] = title3
    context['link3'] = link3

    return render(request,'page.html',context)

def show(request,page):
    context={}
    context['total_num']='共有'+str(3000)+'则新闻'
    context['name']='新浪新闻'
    Textlist = []
    num=3000
    if int(page)==(num-1)//10+1:
        for id in range(int(page)*10-10,num):
            f = open('mysite/data/content/' + str(id), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(id)
            Textlist += [Text(title, _time, content, id, link)]
        context['Textlist'] = Textlist
    else:
        for id in range(int(page)*10-10,int(page)*10):
            f = open('mysite/data/content/' + str(id), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(id)
            Textlist += [Text(title, _time, content, id, link)]
        context['Textlist'] = Textlist
    context['front_page_link'] = '/show/' +'1'
    context['last_page_link'] = '/show/' +str(int(page)-1)
    context['next_page_link'] = '/show/' +str(int(page)+1)
    context['end_page_link'] = '/show/'  + str((num-1) // 10 + 1)
    context['page']=page
    context['total_page']=str((num-1) // 10 + 1)

    return render(request,'show.html',context)


def _search(request,string,page):
    time1 = time.time()
    context={}
    context['title'] = '搜索结果'
    context['keywords'] = string
    list = data.dic[string]
    Textlist=[]
    if int(page)==(len(list)-1)//10+1:
        for id in range(int(page)*10-10,len(list)):
            f = open('mysite/data/content/' + str(list[id]), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(list[id])
            Textlist += [Text(title, _time, content, list[id], link)]
        context['Textlist'] = Textlist
    else:
        for id in range(int(page)*10-10,int(page)*10):
            f = open('mysite/data/content/' + str(list[id]), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(list[id])
            Textlist += [Text(title, _time, content, list[id], link)]
        context['Textlist'] = Textlist
    time2 = time.time()
    search_time=time2-time1
    context['search_title'] = r'"' + string + r'"的搜索结果'
    context['search_time'] = '本次搜索耗时' + str(search_time) + '秒'
    context['search_num'] = '共找到' + str(len(list)) + '条结果'
    context['front_page_link'] = '/search/' + string + '/1'
    context['last_page_link'] = '/search/' + string + '/'+str(int(page)-1)
    context['next_page_link'] = '/search/' + string + '/'+str(int(page)+1)
    context['end_page_link'] = '/search/' + string + '/' + str((len(list)-1) // 10 + 1)
    context['page']=page
    context['total_page']=str((len(list)-1) // 10 + 1)
    return render(request, 'search.html', context)

def homepage(request):
    context={}
    context['bigtitle']='新浪新闻信息整合与检索系统'
    context['introduction']='本网站的全部内容来源于新浪新闻'
    context['title']='新浪新闻信息整合与检索系统'
    context['show']='新闻展示'
    context['search']='新闻搜索'
    context['time_search']='按时间高级搜索'
    context['multi_search']='多关键字搜索'
    context['show_link']='/show/1'
    context['search_link']='/search_form'
    context['time_search_link']='/time_search_form'
    context['multi_search_link']='/multi_search_form'
    return render(request,'homepage.html',context)

def multi_search_form(request):
    context={}
    context['title'] = '多关键词检索'
    context['search_title'] = '多关键词检索'
    return render(request,'multi_search_form.html',context)

def time_search_form(request):
    context={}
    context['title']='按照时间搜索'
    context['search_title']='按照时间搜索'
    return render(request,'time_search_form.html',context)

def multi_search(request):
    time1 = time.time()
    context = {}
    context['title'] = '搜索结果'
    string = request.POST['content']
    fenci_list=[]
    _list=string.split(' ')
    string="".join(_list)
    list=[]
    for word in _list:
        fenci_list+=jieba.cut_for_search(word)
    for ci in fenci_list:
        if ci in data.dic:
            list+=data.dic[ci]
    biao=[0]*3000
    for number in list:
        biao[number]+=1
    enum = (sorted(enumerate(biao), key=lambda item: -item[1]))
    list=[]
    for idd,aaa in enum:
        if aaa:
            list+=[idd]
    Textlist=[]
    if (len(list) <= 10):
        for num in list:
            f = open('mysite/data/content/' + str(num), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(num)
            Textlist += [Text(title, _time, content, num, link)]
    else:
        for i in range(10):
            f = open('mysite/data/content/' + str(list[i]), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(list[i])
            Textlist += [Text(title, _time, content, list[i], link)]
    time2 = time.time()
    search_time = time2 - time1
    context['Textlist'] = Textlist
    context['search_title'] = r'"' + string + r'"的搜索结果'
    context['search_time'] = '本次搜索耗时' + str(search_time) + '秒'
    context['search_num'] = '共找到' + str(len(list)) + '条结果'
    context['front_page_link'] = 'multi_search/' + string + '/1'
    context['last_page_link'] = 'multi_search/' + string + '/1'
    context['next_page_link'] = 'multi_search/' + string + '/2'
    context['end_page_link'] = 'multi_search/' + string + '/' + str((len(list) - 1) // 10 + 1)
    context['page'] = '1'
    context['total_page'] = str((len(list) - 1) // 10 + 1)
    __list=[]
    for char in string:
        __list+=char
    context['keywords'] = __list
    return render(request, 'multi_search.html', context)

def _multi_search(request,string,page):
    time1 = time.time()
    context = {}
    context['title'] = '搜索结果'
    fenci_list = []
    _list = string.split(' ')
    string = "".join(_list)
    list = []
    for word in _list:
        fenci_list += jieba.cut_for_search(word)
    for ci in fenci_list:
        if ci in data.dic:
            list += data.dic[ci]
    biao = [0] * 3000
    for number in list:
        biao[number] += 1
    enum = (sorted(enumerate(biao), key=lambda item: -item[1]))
    list = []
    for idd, aaa in enum:
        if aaa:
            list += [idd]
    Textlist = []
    if int(page)==(len(list)-1)//10+1:
        for id in range(int(page)*10-10,len(list)):
            f = open('mysite/data/content/' + str(list[id]), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(list[id])
            Textlist += [Text(title, _time, content, list[id], link)]
        context['Textlist'] = Textlist
    else:
        for id in range(int(page)*10-10,int(page)*10):
            f = open('mysite/data/content/' + str(list[id]), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(list[id])
            Textlist += [Text(title, _time, content, list[id], link)]
        context['Textlist'] = Textlist
    time2 = time.time()
    search_time=time2-time1
    context['search_title'] = r'"' + string + r'"的搜索结果'
    context['search_time'] = '本次搜索耗时' + str(search_time) + '秒'
    context['search_num'] = '共找到' + str(len(list)) + '条结果'
    context['front_page_link'] = '/multi_search/' + string + '/1'
    context['last_page_link'] = '/multi_search/' + string + '/'+str(int(page)-1)
    context['next_page_link'] = '/multi_search/' + string + '/'+str(int(page)+1)
    context['end_page_link'] = '/multi_search/' + string + '/' + str((len(list)-1) // 10 + 1)
    context['page']=page
    context['total_page']=str((len(list)-1) // 10 + 1)
    __list = []
    for char in string:
        __list += char
    context['keywords'] = __list
    return render(request,"multi_search.html",context)

def time_search(request):
    if(request.POST):
        time1 = time.time()
        context={}
        date=request.POST['year']+'年'+request.POST['month']+'月'+request.POST['day']+'日'
        context['title'] = '搜索结果'
        string = request.POST['content']
        context['keywords'] = string
        if request.POST['content'] not in data.dic.keys():
            temp = {}
            temp['title'] = "找不到搜索结果"
            temp['text'] = r'没有找到"' + string + r'"的结果'
            return render(request, 'search_error.html', temp)
        else:
            list = data.dic[request.POST['content']]
            Textlist = []
            for num in list:
                f = open('mysite/data/content/' + str(num), 'r', encoding='UTF-8')
                content = []
                title = f.readline()
                _time = f.readline()
                for line in f.readlines():
                    content += [line]
                link = '/page/' + str(num)
                Textlist += [Text(title, _time, content, num, link)]
            Time_Textlist=[]
            for article in Textlist:
                if article.time[:11]==date:
                    Time_Textlist+=[article]
            if(len(Time_Textlist)<=10):
                reallist=Time_Textlist
            else:
                reallist=Time_Textlist[:10]
            time2 = time.time()
            search_time = time2 - time1
            context['Textlist'] = reallist
            context['search_title'] = r'"' + string + r'"的搜索结果'
            context['search_time'] = '本次搜索耗时' + str(search_time) + '秒'
            context['search_num'] = '共找到' + str(len(Time_Textlist)) + '条结果'
            context['front_page_link'] = 'time_search/' + string + '/'+date+'/1'
            context['last_page_link'] = 'time_search/' + string + '/'+date+'/1'
            context['next_page_link'] = 'time_search/' + string + '/'+date+'/2'
            context['end_page_link'] = 'time_search/' + string + '/' +date+'/'+ str((len(Time_Textlist) - 1) // 10 + 1)
            context['page']='1'
            context['total_page']=str((len(Time_Textlist) - 1) // 10 + 1)
            return render(request, 'time_search.html', context)

def _time_search(request,string,date,page):
    time1 = time.time()
    context = {}
    context['title'] = '搜索结果'
    context['keywords'] = string
    if string not in data.dic.keys():
        temp = {}
        temp['title'] = "找不到搜索结果"
        temp['text'] = r'没有找到"' + string + r'"的结果'
        return render(request, 'search_error.html', temp)
    else:
        list = data.dic[string]
        Textlist = []
        for num in list:
            f = open('mysite/data/content/' + str(num), 'r', encoding='UTF-8')
            content = []
            title = f.readline()
            _time = f.readline()
            for line in f.readlines():
                content += [line]
            link = '/page/' + str(num)
            Textlist += [Text(title, _time, content, num, link)]
        Time_Textlist = []
        for article in Textlist:
            if article.time[:11] == date:
                Time_Textlist += [article]
        if (int(page) == (len(Time_Textlist)-1)//10+1):
            reallist = Time_Textlist[int(page)*10-10:]
        else:
            reallist = Time_Textlist[int(page)*10-10:int(page)*10]
        time2 = time.time()
        search_time = time2 - time1
        context['Textlist'] = reallist
        context['search_title'] = r'"' + string + r'"的搜索结果'
        context['search_time'] = '本次搜索耗时' + str(search_time) + '秒'
        context['search_num'] = '共找到' + str(len(Time_Textlist)) + '条结果'
        context['front_page_link'] = '/time_search/' + string + '/' + date + '/1'
        context['last_page_link'] = '/time_search/' + string + '/' + date + '/'+str(int(page)-1)
        context['next_page_link'] = '/time_search/' + string + '/' + date + '/'+str(int(page)+1)
        context['end_page_link'] = '/time_search/' + string + '/' + date + '/' + str((len(Time_Textlist) - 1) // 10 + 1)
        context['page']=page
        context['total_page']=str((len(Time_Textlist) - 1) // 10 + 1)
        return render(request, 'time_search.html', context)
