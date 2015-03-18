#! /usr/bin/env python
import re
import sys
import datetime

from draw import DrawFigure


updated_date=None
start_date=datetime.date(2012,9,7)
L10_start_date=datetime.date(2014,7,1)
S8_start_date=datetime.date(2014,8,1)

data_total = [[],[]]
data_1     = [[],[]]
data_2     = [[],[]]
data_10    = [[],[]]
data_S1    = [[],[]]
data_S8    = [[],[]]


def write_date_content(file, date, content):
    assert len(date) == len(content)
    f = open(file, "w")
    for i in range(0,len(date)):
        f.write(date[i].isoformat())
        f.write(content[i])
    f.close

def is_filtered(date):
    if filter_year:
        if date.year == filter_year:
            return True 
        else:
            return False
    else: 
        return True

def _search_data(content, date):
    # total passenger flow
    flow = re.search('客运量约?为?近?([0-9.]+)', content)
    if not flow:
        print("not find flow")
        exit()
    flow = float(flow.group(1))
    if flow > 10000:
        flow = flow/10000
    #flow='{:.1f}'.format(flow)
    data_total[0].append(date)
    data_total[1].append(flow)
    
    # line 1 & 2 passenger flow
    find = re.search('(1|一)号线((\(|（)含南延线(\)|）))?(?P<line_1>\d+(\.\d+)?).*(二|2)号线(?P<line_2>\d+(\.\d+)?)', content)
    if find:
        line_1 = float(find.group('line_1'))
        if line_1:
            if line_1 > 10000:
                line_1 = line_1/10000
            #line_1 = '{:.1f}'.format(line_1)
            data_1[0].append(date)
            data_1[1].append(line_1)
        line_2 = float(find.group('line_2'))
        if line_2:
            if line_2 > 10000:
                line_2 = line_2/10000
            #line_2 = '{:.1f}'.format(line_2)
            data_2[0].append(date)
            data_2[1].append(line_2)
    else:
        return
    
    #十号线 机场线
    #十号线11.30,机场线5.00.主要车站:新街口站12.18(以上单位:万人次)
    #10号线4.3,  S1号线(机场线)4,  S8号线(宁天线)1.6  (以上单位:万人次)
    find = re.search('(10|十)号线(?P<line_10>\d+(\.\d+)?).*((机场线(\)|）)?)|(S1号线))(?P<line_S1>\d+(\.\d+)?)', content)
    if find:
        line_10 = find.group('line_10')
        if line_10:
            line_10 = float(line_10)
            if line_10 > 10000:
                line_10 = line_10/10000
            #line_10 = '{:.1f}'.format(line_10)
            data_10[0].append(date)
            data_10[1].append(line_10)

        line_S1 = find.group('line_S1')
        if line_S1:
            line_S1 = float(line_S1)
            if line_S1 > 10000:
                line_S1 = line_S1/10000
            #line_S1 = '{:.1f}'.format(line_S1)
            data_S1[0].append(date)
            data_S1[1].append(line_S1)
    else:
        return

    # 宁天 2014-08-01 通车后格式
    #S8号线（宁天线）6.97.（以上单位：万人次）  PS: 大家猜猜看,昨天3条新线10号线,S1号线,S8号线最大客流分别出现在哪个站？[偷乐]
    find = re.search('宁天线(\)|）)?(?P<line_S8>\d+(\.\d+)?)', content)
    if find:
        line_S8 = find.group('line_S8')
        if line_S8:
            line_S8 = float(line_S8)
            if line_S8 > 10000:
                line_S8 = line_S8/10000
            #line_S8 = '{:.1f}'.format(line_S8)
            data_S8[0].append(date)
            data_S8[1].append(line_S8)
    else:
        return

def filter_data(year=None, month=None, day=None):
    global filter_year
    filter_year=year

def get_updated_date(file):
    f = open(file,"r")
    line = f.readline()
    f.close()
    dates=re.match('# updated to (\w+)-(\w+)-(\w+)', line)
    if not dates:
        raise Exception("Error in get_updated_date(): didn't get updated_date")
    return datetime.date(*[int(i) for i in dates.groups()])

def check_data():
    #the day data lost
    # 2014-12-12 【昨日客流】12月12日全线网客运量为166.2万人次。
    # 2014-12-13 【昨日客流】南京地铁12月13日全线网客运量为151.2万人次
    deficiency = 2
    # check data_S8
    try:
        assert (updated_date - S8_start_date).days+1-deficiency == len(data_S8[0])
    except AssertionError:
        error = (updated_date - S8_start_date).days+1-len(data_S8[0])
        print('S8 错误天数 {0}'.format(error))

    delta = datetime.timedelta(days=1)
    pre_date = None
    for i in data_S8[0]:
        if pre_date and i != datetime.date(2014,12,14):
            try:
                assert i == pre_date + delta
            except AssertionError:
                print("data_S8 check error: ", sep='', end='')
                print(i)
        pre_date = i
    # check data_10

def get_passenger_flow_data(file, check=False):
    global updated_date
    updated_date = get_updated_date(file)
    count=0
    delta=datetime.timedelta(days=1)
    pre_date=None
    for line in open(file,'r').readlines():
        if line[0] == '#': continue
        count+=1
        date = line[0:10]
        date = datetime.date(*[int(val) for val in date.split('-')])
        if pre_date:
            if pre_date != date-delta:
                print(date)
        pre_date = date
        if is_filtered(date):
            _search_data(line[10:], date)
    
    print('passage flow records: {0}'.format(count))
    print('line  1 records: {0}'.format(len(data_1[0])))
    print('line  2 records: {0}'.format(len(data_2[0])))
    print('line 10 records: {0}'.format(len(data_10[0])))
    print('line S1 records: {0}'.format(len(data_S1[0])))
    print('line S8 records: {0}'.format(len(data_S8[0])))
    if check:
        check_data()
    
filter_year = None
#filter_data(year=2015)

get_passenger_flow_data('./passenger-flow-weibos.txt', check=False)

datas = [{'x': data_total[0], 'y':data_total[1], 'color':'#999999', 'linewidth':1.5, 'label':'total'},
        {'x': data_1[0],     'y':data_1[1],     'color':'#13A1E6', 'linewidth':1, 'label':'Line  1'},
        {'x': data_2[0],     'y':data_2[1],     'color':'#E40011', 'linewidth':1, 'label':'Line  2'},
        {'x': data_10[0],    'y':data_10[1],    'color':'#D1AE61', 'linewidth':1, 'label':'Line 10'},
        {'x': data_S1[0],    'y':data_S1[1],    'color':'#4BBBB4', 'linewidth':1, 'label':'Line S1'},
        {'x': data_S8[0],    'y':data_S8[1],    'color':'#F28C4D', 'linewidth':1, 'label':'Line S8'}
]

if filter_year:
    show = DrawFigure(datas, datarange='year')
else:
    show = DrawFigure(datas)
show.draw()
