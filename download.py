#! /usr/bin/env python
import urllib
from urllib import request
from bs4 import BeautifulSoup 
import re
import sys
import datetime

from data import config


headers = {
    'cookie': config.weibo_cn_cookie,
    'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36',
    #'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4,ja;q=0.2',
    'Host':'weibo.cn',
    #'Connection':'keep-alive',
    #'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding':'gzip, deflate, sdch'
}


def get(url):
    req = urllib.request.Request(url, headers=headers) 
    result = urllib.request.urlopen(req)
    text = result.read()
    if len(text) < 20:
        print("connect error")
        exit()
    return  text.decode('utf-8','ignore') 
    
def extract_page_weibos(url):
    text = get(url)
    data=[]
    #soup = BeautifulSoup(''.join(text))
    #items =  soup.findAll('span', attrs={"class":"ctt"})
    #dates =  soup.findAll('span', attrs={"class":"ct"})
    items = re.findall('<span class="ctt">(.*?)</span>',text)
    dates = re.findall('<span class="ct">(.*?)</span>',text)
    
    try:
        if url.endswith('=1'):
            assert len(dates) == len(items)-2
            items=items[2:]
        else:
            assert len(dates) == len(items)
    except AssertionError:
        print('\nNumber Error:')
        print(url)
        print(len(dates),sep=' ',end='')
        print(len(items),sep=' ')
        for i in dates:
            print(i)
        for i in items:
            print(i)
        exit() 

    for i in range(len(dates)):
        date=dates[i]
        date=date.replace('&nbsp;', ' ') 
        content=re.sub('<.*?>', '', items[i])
        data.append({'date':date, 'content':content})

        try:
            assert date!=None
            assert content!=None
        except AssertionError:
            print('\nNone appear:')
            print(dates[i])
            print(items[i])

    return data

def get_all_posts():
    data=[]
    url=config.njmetro_url
    fo = open("output-data", "w")

    # get pages number
    text=get(url)
    pages=re.findall("1/(\d+)页</div>", text)
    assert len(pages) == 1
    pages=int(pages[0])
    print("pages needs capture: {0}".format(pages))
    print("processing:     ",sep='', end='')

    # get posts
    for i in range(1,pages+1):
    #for i in range(1,3):
        print('\b\b\b\b{:4d}'.format(i), sep='', end='')
        sys.stdout.flush()
        url = config.njmetro_url + '?page={0}'.format(i)
        extract_info(url, data)

    print()
    print('data items: {0}'.format(len(data)))

    for i in data:
        fo.write(i['date'])
        fo.write('\n')
        fo.write(i['content'])
        fo.write('\n')
    fo.close

def get_flow_weibos_from_all_weibos(file):
    data=[]
    double=1
    for line in open(file,'r').readlines():
        if double ==1:
            date=line[0:-1]
            double = 0
        else:
            content =line[0:-1]
            double = 1
            result = re.search('昨日客流|客流报告', content)
            if result:
                data.append({'date':date, 'content':content}) 
    
    print('passage flow records: {0}'.format(len(data)))

    fo = open("passenger-flow-weibo.txt", "w")
    for i in data:
        # date
        if re.match('今天',i['date']):
            i['date'] = '2015-03-07'
        date=re.match('(\d+)月(\d+)日',i['date'])
        if date:
            date = "2015-{0}-{1}".format(date.group(1), date.group(2))
        else:
            date = i['date'][0:10]
        
        # datetime.date
        date = datetime.date(*[int(val) for val in date.split('-')])

        # output    
        fo.write(date.isoformat())
        fo.write(' ')
        fo.write(i['content'])
        fo.write('\n')
    fo.close

def get_date(date):
    result=None
    if re.match('今天',date):
        result = datetime.date.today()
    else:
        find=re.match('(\d+)月(\d+)日',date)
        if find:
            result = datetime.date(datetime.date.today().year, int(find.group(1)), int(find.group(2)))
        else:
            find=re.match('(\d+)-(\d+)-(\d+)',date)
            if find:
                result = datetime.date(*[int(i) for i in find.groups()])
            else:
                print()
                print("get_date() Except:")
                print(date)
    return result


def is_target(content):
    find = re.search('昨日客流|客流报告', content)
    if find:
        return True
    else:
        return False


def get_new_posts(archive_file=None):
    if archive_file:
        f = open(archive_file,"r")
        line = f.readline()
        f.close()
        dates=re.match('# updated to (\w+)-(\w+)-(\w+)', line)
        if not dates:
            print("error get_new_posts() updated to")
            return
        updated_date = datetime.date(*[int(i) for i in dates.groups()])
        print('已有数据更新至 {0}'.format(updated_date.isoformat()))
    else:
        updated_date = datetime.date(2012,9,8)
    # 7号数据8号更新，故增1
    updated_date += datetime.timedelta(days=1)

    url=config.njmetro_url

    # get pages number
    text=get(url)
    pages=re.findall("1/(\d+)页</div>", text)
    try:
        assert len(pages) == 1
    except AssertionError:
        print(pages)
        exit(0)

    pages=int(pages[0])
    print("pages find: {0}".format(pages))

    # get posts
    new_weibos = [[],[]]
    isEnd=False
    for i in range(1,pages+1):
        if isEnd: break
        print('\rprocessing page: {:4d}'.format(i), sep='', end='')
        sys.stdout.flush()
        url = config.njmetro_url + '?page={0}'.format(i)
        data = extract_page_weibos(url)
        for item in data:
            if not is_target(item['content']):
                continue
            date = get_date(item['date'])
            if date > updated_date:
                print('\n找到 {0} 日微博'.format(date.isoformat()))
                new_weibos[0].append(date)
                new_weibos[1].append(item['content'])
            if date == updated_date:
                isEnd=True
                break
    
    if len(new_weibos[0]) == 0:
        return
    # 翻转数据
    new_weibos[0].append(updated_date)
    new_weibos[0].reverse()
    new_weibos[0].pop()
    new_weibos[1].reverse()
    # 存档
    new_updated = new_weibos[0][-1].isoformat()
    new_archive_= archive_file + '+' + new_updated
    new_archive_file = 'passenger-flow-weibos' + '+' + new_updated
    f = open(new_archive_file, 'w')
    f.write('# updated to {0}\n'.format(new_updated))
    # copy former weibos
    if archive_file:
        for line in open(archive_file):
            if line[0] !='#':
                f.write(line)

    for i in range(0,len(new_weibos[0])):
        f.write(new_weibos[0][i].isoformat())
        f.write(' ')
        f.write(new_weibos[1][i])
        f.write('\n')
    f.close

#get_flow_weibos_from_all_weibos('all-njmetro-weibo')
#get_all_posts()
get_new_posts("passenger-flow-weibos.txt")
