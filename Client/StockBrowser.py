from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
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
        self.stockPriceGraph=self.plotRandomStock()
        
        self.leftLayout=QtWidgets.QVBoxLayout()
        self.leftLayout.addWidget(self.searchLineEdit)
        self.leftLayout.addWidget(self.stockList)
        
        self.middleLayout=QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.stockPriceGraph)
        
        self.mainLayout=QtWidgets.QHBoxLayout(self)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.setStretchFactor(self.leftLayout,3)
        self.mainLayout.setStretchFactor(self.middleLayout,7)
        
        self.fillStockList()
        
    def plotRandomStock(self):
        self.stockCode='002230'
        data=ts.get_hist_data(self.stockCode)
        data=data['close']
        data=np.array(data)
        data=data[::-1]
        figure=plt.figure()
        plt.plot(data)
        canvas=FigureCanvas(figure)
        canvas.draw()
        return canvas
    
    def fillStockList(self):
        self.rawData=np.loadtxt('industry.txt',str,delimiter=',')
        for stock in self.rawData:
            self.stockList.addItem(stock[0]+'\t'+stock[1]+'\t'+stock[2])
            
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
        for stock in self.rawData:
            count=0
            for info in stock:
                if searchContent in info:
                    count+=len(searchContent)
            matchRateList.append([str(count),stock])
        return matchRateList
        
    def getMatchRate(self,matchRateList):
        return matchRateList[0]
                    