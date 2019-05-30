# -*- coding: utf-8 -*-
"""
Created on Sun May 26 21:34:02 2019

@author: 12613
"""
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf 
from statsmodels.graphics.tsaplots import plot_pacf
import seaborn as sns
import tushare  as ts
data=ts.get_hist_data('600603',start='2018-01-01')
data.to_csv('data.csv')
df=pd.read_csv('data.csv',index_col=0,parse_dates=[0])
#index_col表示把第一列设为index,parse_dates=[0]表示把第一列按datetime格式解析

stock_week=df['close'].resample('W-TUE').mean() 
#将收盘价作为评判标准，resample指按周统计平均数据(可以指定哪天为基准日，此处是周二为基准)

stock_train=stock_week['2017':'2019'].dropna()
#选取2005-2017的数据

stock_diff=stock_train.diff().dropna() #对数据进行差分，目的使数据平缓,满足平稳性的要求

acf=plot_acf(stock_diff,lags=20)
plt.title('ACF')
acf.show()
plt.show()
pacf=plot_pacf(stock_diff,lags=20)
plt.title('PACF')
pacf.show()
plt.show()

model=ARIMA(stock_train,order=(18,1,1),freq='W-TUE')#训练模型,order表示（p,d,q）
result=model.fit()
pred=result.predict('2019-01-01','2019-10-08',dynamic=True,typ='levels')#注意预测的起始时间要在训练时间的范围内，结束时间没有要求
plt.figure(figsize=(6,6))
plt.xticks(rotation=45)
plt.plot(pred)
plt.plot(stock_train)
plt.show()