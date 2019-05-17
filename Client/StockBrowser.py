from PyQt5 import QtWidgets,QtCore
import pyqtgraph as pg
import tushare as ts
import numpy as np
import SearchLineEdit
import datetime
from CandlestickItem import CandlestickItem

class StockBrowser(QtWidgets.QWidget):
    
    industryData=np.loadtxt('industry.txt',str,delimiter=',')
    code=industryData[0,0]
    data=ts.get_hist_data(code=code).sort_index()

    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
        self.setupConnection()
        
    #Functions:
    def initUI(self):
        self.searchLineEdit=SearchLineEdit.SearchLineEdit()
        self.stockList=QtWidgets.QListWidget()
        self.fillStockList()
        self.stockKLine=pg.PlotWidget()
        self.plotKLine()
        
        self.leftLayout=QtWidgets.QVBoxLayout()
        self.leftLayout.addWidget(self.searchLineEdit)
        self.leftLayout.addWidget(self.stockList)
        
        self.middleLayout=QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.stockKLine)
        
        self.mainLayout=QtWidgets.QHBoxLayout(self)
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.setStretchFactor(self.leftLayout,3)
        self.mainLayout.setStretchFactor(self.middleLayout,7)
    
    def fillStockList(self):
        for stock in self.industryData:
            self.stockList.addItem(stock[0]+'\t'+stock[1]+'\t'+stock[2])
            
    def updateStockData(self):
        self.data=ts.get_hist_data(self.code).sort_index()
            
    def setupConnection(self):
        self.searchLineEdit.textChanged.connect(self.searchStockList)
        self.stockList.itemDoubleClicked.connect(self.stockFocusChanged)
        self.moveSlot=pg.SignalProxy(self.stockKLine.scene().sigMouseMoved,rateLimit=60,slot=self.printSlot)
        self.testSlot=pg.SignalProxy(self.stockKLine.sigScaleChanged,slot=self.test)
        
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
    
    def plotKLine(self):
        yMin=self.data['low'].min()
        yMax=self.data['high'].max()
        xMax=len(self.data['open'])
        dataList=[]
        index=0
        for date,row in self.data.iterrows():
            openPrice,highPrice,closePrice,lowPrice=row[:4]
            OCLH=(index,openPrice,closePrice,lowPrice,highPrice)
            dataList.append(OCLH)
            index+=1
        self.axisDict=dict(enumerate(self.data.index))
        axis=[(i,list(self.data.index)[i]) for i in range(0,len(self.data.index),3)] 
        self.stockKLine.getAxis("bottom").setTicks([axis,self.axisDict.items()])
        self.stockKLine.plotItem.clear()
        item = CandlestickItem(dataList)
        self.stockKLine.addItem(item)
        self.stockKLine.showGrid(x=True,y=True)
        self.stockKLine.setYRange(yMin,yMax)
        self.stockKLine.setXRange(0,xMax)
        self.stockKLine.setLabel(axis='left',text='Price')
        self.stockKLine.setLabel(axis='bottom',text='Date')
        self.label=pg.TextItem()
        self.stockKLine.addItem(self.label)
 
        self.vLine = pg.InfiniteLine(angle=90,movable=False)
        self.hLine = pg.InfiniteLine(angle=0,movable=False)
        self.stockKLine.addItem(self.vLine)
        self.stockKLine.addItem(self.hLine)
    
    #Slots:
    def searchStockList(self):
        searchContent=self.searchLineEdit.text()
        matchRateList=self.matchRate(searchContent)
        matchRateList.sort(key=self.getMatchRate,reverse=True)
        self.stockList.clear()
        for stock in matchRateList:
            info=stock[1]
            self.stockList.addItem(info[0]+'\t'+info[1]+'\t'+info[2])
    
    def stockFocusChanged(self,item):
        stock=item.text()
        stock=stock.split('\t')
        self.code=stock[0]
        self.updateStockData()
        self.plotKLine()
        
    def printSlot(self, event=None):
        pos = event[0]  # 获取事件的鼠标位置
        # 如果鼠标位置在绘图部件中
        if self.stockKLine.sceneBoundingRect().contains(pos):
            mousePoint = self.stockKLine.plotItem.vb.mapSceneToView(pos)  # 转换鼠标坐标
            index = int(mousePoint.x())  # 鼠标所处的X轴坐标
            pos_y = int(mousePoint.y())  # 鼠标所处的Y轴坐标
            if -1 < index < len(self.data.index):
                # 在label中写入HTML
                self.label.setHtml("<p style='color:white'><strong>Date: {0}</strong></p><p style='color:white'>Open: {1}</p><p style='color:white'>Close: {2}</p><p style='color:white'>High: <span style='color:red;'>{3}</span></p><p style='color:white'>Low: <span style='color:green;'>{4}</span></p>".format(self.axisDict[index], self.data['open'][index], self.data['close'][index],self.data['high'][index], self.data['low'][index]))
                self.label.setPos(mousePoint.x(), mousePoint.y())  # 设置label的位置
            # 设置垂直线条和水平线条的位置组成十字光标
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
                    
    def test(self):
        print('Test')