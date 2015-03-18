#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.lines as mlines
from pylab import figure


class DrawFigure():
    def __init__(self, datas, figsize=(20,6), datarange='all'):
        plt.style.use('ggplot')
        fig = plt.figure(figsize=figsize)
        fig.set_tight_layout(True)
        self.ax = fig.add_subplot(1,1,1)
        self.datas = datas
        self.datarange= datarange
    
    def set_locator_and_formatter(self):
        years    = mdates.YearLocator()   # every year
        months   = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')
        monthsFmt = mdates.DateFormatter('%m')  #%b

        # format the ticks
        self.ax.set_yticks([0,20,40,60,80,100,120,140,160,180,200,220])
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
        self.ax.set_yticks([0,20,40,60,80,100,120,140,160,180,200,220])
        self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(mdates.MONDAY))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.ax.xaxis.set_minor_locator(mdates.DayLocator())
        self.ax.grid(True)  # 'minor' major'(default)

    def add_plot(self):
        for item in self.datas:
            self.ax.plot(item['x'], item['y'], color=item['color'], linewidth=item['linewidth'])

        # Legend 图例
        handlers=[]
        for item in self.datas:
            line = mlines.Line2D([],[], color=item['color'], linewidth=2.5, label=item['label'])
            handlers.append(line)

        self.ax.legend(handles=handlers, loc='upper left', ncol=2,\
            fancybox=True )

    def draw(self):
        if self.datarange == 'all':
            print('Draw all data')
            title='Number of Passengers Carried by Nanjing Metro per Day (since 2012-9-7)'
            fname='Nanjing-Metro-passenger-Flow-since-20120907.png'
            self.set_locator_and_formatter()
        else:
            print('Draw data 2015')
            title='Number of Passengers Carried by Nanjing Metro per Day (since 2015-1-1)'
            fname='Nanjing-Metro-passenger-Flow-2005.png'
            self.set_one_year()
        self.add_plot()

        self.ax.format_xdata = mdates.DateFormatter('%Y-%m-%d') # pointer info
         
        plt.title(title) # plot title
        plt.ylabel('Passenger Flow (unit: 10k)') # Y label
        #plt.xlabel('date') # X label
        plt.ylim(0, 220)
        #pl.xlim(0.0, 9.0)# set axis limits

        plt.savefig('img/'+fname)
        plt.show()
    
