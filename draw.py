#!/usr/bin/env python
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import matplotlib.font_manager as mfont
from pylab import figure


class DrawFigure():
    def __init__(self, datas, year=None, update=''):
        plt.style.use('ggplot')
        self.font_title = mfont.FontProperties(
                fname='/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc',
                size=20)
        self.font_label = mfont.FontProperties(
                fname='/usr/share/fonts/wenquanyi/wqy-microhei/wqy-microhei.ttc',
                size=15)
        if year:
            l = int(len(datas[0]['x'])/365*20)
            if l<15: l = 10
            figsize = (l,6)
        else:
            figsize = (20,6)
        fig = plt.figure(figsize=figsize)
        fig.set_tight_layout(True)
        self.ax = fig.add_subplot(1,1,1)
        self.datas = datas
        self.year = year
        self.update=update
    
    def set_locator_and_formatter(self):
        years    = mdates.YearLocator()   # every year
        months   = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')
        monthsFmt = mdates.DateFormatter('%b')  #%b

        # format the ticks
        self.ax.set_yticks([0,20,40,60,80,100,120,140,160,180,200,220,240,260,280])
        self.ax.xaxis.set_major_locator(years)
        self.ax.xaxis.set_major_formatter(yearsFmt)
        self.ax.xaxis.set_minor_locator(months)
        self.ax.xaxis.set_minor_formatter(monthsFmt)

        self.ax.grid(True, which='both')  # 'minor' major'(default)
        self.ax.xaxis.set_tick_params(which='major', pad=16, labelsize='large',
             width=1.5, length=4)

    def set_one_year(self):
        years    = mdates.YearLocator()   # every year
        months   = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')
        monthsFmt = mdates.DateFormatter('%m')

        #ax.plot(data_total[0], data_total[1])
        # format the ticks
        self.ax.set_yticks([0,20,40,60,80,100,120,140,160,180,200,220,240,260,280])
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(mdates.MONDAY))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        self.ax.xaxis.set_minor_locator(mdates.DayLocator())
        self.ax.grid(True)  # 'minor' major'(default)

    def add_plot(self):
        for item in self.datas:
            self.ax.plot(item['x'], item['y'], color=item['color'], 
                    linewidth=item['linewidth'])

        # Legend 图例
        handlers=[]
        for item in self.datas:
            line = mlines.Line2D([],[], color=item['color'], linewidth=2.5, 
                    label=item['label'])
            handlers.append(line)

        self.ax.legend(handles=handlers, loc='upper left', ncol=2,\
            fancybox=True)

    def draw(self):
        if self.year == None:
            print('Drawing all datas:')
            title='南京地铁每日客运量  '+ \
                  '(2012-09-07 ~ {0})'.format(self.update)
            fname='Nanjing-Metro-passenger-Flow-since-20120907.png'
            self.set_locator_and_formatter()
        else:
            print('Drawing datas of {0}:'.format(self.year))
            year_end = datetime.date(self.year, 12, 31)
            if year_end.isoformat() != self.update:
                year_end = self.update
            title='南京地铁每日客运量  '+\
                  '({0}-01-01 ~ {1})'.format(self.year, year_end)
            fname='Nanjing-Metro-passenger-Flow-2005.png'
            self.set_one_year()

        self.add_plot()
        #self.ax.format_xdata = mdates.DateFormatter('%Y-%m-%d') # pointer info
        
        plt.title(title, fontproperties=self.font_title) # plot title
        plt.ylabel('客运量 (万)',fontproperties=self.font_label) # Y label
        #plt.xlabel('date') # X label
        plt.ylim(0, 280)
        #pl.xlim(0.0, 9.0)# set axis limits

        plt.savefig('img/'+fname)
        plt.show()
    
