# coding: UTF-8
 
"""
本函数以20日线为标准，当前股价低于20日线的时候就卖出，高于20日线的时候就买入。

计算该这个策略的效果。
code_list输入想要计算收益的股票代码
然后加了一个 rate 参数，这是用于统计每次买卖后的收益。
这里有个0.002的值，表示两块一个是印花税卖出后有1%的印花税要抽，一个是券商的佣金，按万5来算，
一来一回也是千分之一。
"""


import numpy as np
import tushare as ts
 
def parse(code_list):
    '''process stock'''
    is_buy    = 0
    buy_val   = []
    buy_date  = []
    sell_val  = []
    sell_date = []
    df = ts.get_hist_data(code_list)
    ma20 = df[u'ma20']
    close = df[u'close']
    #name = df[u'name']
    rate = 1.0
    idx = len(ma20)
 
    while idx > 0:
        idx -= 1
        close_val = close[idx]
        ma20_val = ma20[idx]
        if close_val > ma20_val:
                if is_buy == 0:
                        is_buy = 1
                        buy_val.append(close_val)
                        buy_date.append(close.keys()[idx])
        elif close_val < ma20_val:
                if is_buy == 1:
                        is_buy = 0
                        sell_val.append(close_val)
                        sell_date.append(close.keys()[idx])
 
    #print("stock number: ",code_list)
    #print("stock name:" ,name)
    #print ("buy count   :" ,len(buy_val))
    #print ("sell count  :" ,len(sell_val))
 
    for i in range(len(sell_val)):
        rate = rate * (sell_val[i] * (1 - 0.002) / buy_val[i])
        #print ("buy date : %s, buy price : %.2f" %(buy_date[i], buy_val[i]))
        #print ("sell date: %s, sell price: %.2f" %(sell_date[i], sell_val[i]))
 
    #print ("rate: %.2f" % rate)
    result='buy count: '+str(len(buy_val))+'\n'+'sell count: '+str(len(sell_val))+'\n'+'rate: '+'%.2f' % rate
    return result

 
