from urllib.request import urlopen
import re

id=0

def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile("//<!\[CDATA\[[^>]*//\]\]>", re.I)  #匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    #re_nbsp=re.compile('&nbsp')
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    #s = re_nbsp.sub('',s)
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s

def getTitle(url):
    try:
        print(url)
        html=urlopen(url).read().decode('UTf-8')
        header=re.findall("<h1 class=\"main-title\">(.+?)</h1>",html)
        return header[0]
    except:
        print('network error!')

def getText(url):
    try:
        global id
        print(url)
        _s=[]
        html = urlopen(url).read().decode('UTf-8')
        header = re.findall("<h1 class=\"main-title\">(.+?)</h1>", html)[0]
        time = re.findall("<span class=\"date\">(.+?)</span>", html)[0]
        text = re.findall("<div class=\"article\" id=\"article\">([\w\W]+?)<!-- 正文 end -->",html,re.M)[0]
        _str = re.findall("<p.*?>(.+?)</p>",text)
        for s in _str:
            _s+=[filter_tags(s)]
        f=open(str(id),'w',encoding='UTF-8')
        f.write(header)
        f.write('\n')
        f.write(time)
        f.write('\n')
        for s in _s:
            f.write(s)
            f.write('\n')
        id+=1
        return(_s)
    except:
        print('network error!')

def getTime(url):
    try:
        print(url)
        html = urlopen(url).read().decode('UTf-8')
        time = re.findall("<span class=\"date\">(.+?)</span>",html)
        return time[0]
    except:
        print('network error!')

urls=[]
for i in range(1,200):
    html = urlopen("http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_"+str(i)+".shtml").read().decode('GBK')
    urls+=re.findall("<li><a href=\"(.+?)\"",html)
    print(i)
for url in urls:
    getText(url)