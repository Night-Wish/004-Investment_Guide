'''
在Anaconda Prompt中输入pip install pyecharts==0.5.6
更高级的版本无法使用
该程序一定会在第二次运行时崩溃，初步诊断为QWebEngineView()的问题
'''

from PyQt5 import QtWidgets,QtCore
import pyqtgraph as pg
import tushare as ts
import numpy as np
import SearchLineEdit

class StockBrowser(QtWidgets.QWidget):
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
        self.setupConnection()
    
    def initUI(self):
        self.searchLineEdit=SearchLineEdit.SearchLineEdit()
        self.stockList=QtWidgets.QListWidget()
        self.stockGraph=pg.PlotWidget(self)
        
        self.leftLayout=QtWidgets.QVBoxLayout()
        self.leftLayout.addWidget(self.searchLineEdit)
        self.leftLayout.addWidget(self.stockList)
        
        self.middleLayout=QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.stockGraph)
        
        self.mainLayout=QtWidgets.QHBoxLayout(self)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.setStretchFactor(self.leftLayout,3)
        self.mainLayout.setStretchFactor(self.middleLayout,7)
        
        self.fillStockList()
        self.plotStockGraph()
        
    
    def fillStockList(self):
        self.industryData=np.loadtxt('industry.txt',str,delimiter=',')
        for stock in self.industryData:
            self.stockList.addItem(stock[0]+'\t'+stock[1]+'\t'+stock[2])
            
    def plotStockGraph(self):
        firstStock=self.industryData[0]
        data=ts.get_hist_data(firstStock[0],ktype='5')
        data=data['close']
        data=np.array(data)
        self.stockGraph.plot(data)
            
    def setupConnection(self):
        self.searchLineEdit.textChanged.connect(self.searchStockList)
        
    def searchStockList(self):
        searchContent=self.searchLineEdit.text()
        matchRateList=self.matchRate(searchContent)
        matchRateList.sort(key=self.getMatchRate,reverse=True)
        self.stockList.clear()
        for stock in matchRateList:
            info=stock[1]
            self.stockList.addItem(info[0]+'\t'+info[1]+'\t'+info[2])
        
    def matchRate(self,searchContent):
        matchRateList=[]
        for stock in self.industryData:
            count=0
            for info in stock:
                if searchContent in info:
                    count+=len(searchContent)
            matchRateList.append([str(count),stock])
        return matchRateList
        
    def getMatchRate(self,matchRateList):
        return matchRateList[0]
                    