from PyQt5 import QtWidgets,QtCore,QtGui
import pyqtgraph as pg
import tushare as ts
import numpy as np

import ChooseStock
import StockChoose_hist_data

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
        self.searchLineEdit=SearchLineEdit()
        self.stockList=QtWidgets.QListWidget()
        self.fillStockList()
        self.stockKLine=pg.PlotWidget()
        self.plotKLine()
        self.analyseBtn=QtWidgets.QPushButton('Analyse')
        self.analyseText=QtWidgets.QTextEdit()
        
        self.leftLayout=QtWidgets.QVBoxLayout()
        self.leftLayout.addWidget(self.searchLineEdit)
        self.leftLayout.addWidget(self.stockList)
        
        self.middleLayout=QtWidgets.QVBoxLayout()
        self.middleLayout.addWidget(self.analyseBtn)
        self.middleLayout.addWidget(self.stockKLine)
        self.middleLayout.addWidget(self.analyseText)
        
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
        self.analyseBtn.clicked.connect(self.recommend)
        
    def recommend(self):
        self.codeRec,self.codeLimUp=ChooseStock.recommend()
        tempTotal=self.stockList.count()
        for i in range(tempTotal):
            tempText=self.stockList.item(i).text()
            tempNum=tempText[0:6]
            for j in self.codeRec:
                if tempNum==j:
                    self.stockList.item(i).setBackground(QtGui.QColor('deepskyblue'))
                    break
            for j in self.codeLimUp:
                if tempNum==j:
                    self.stockList.item(i).setBackground(QtGui.QColor('tomato'))
                    break
        print('analyse over')
    
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
        self.updateStockText()
        self.plotKLine()
        
    def updateStockText(self):
        self.stockPreText=StockChoose_hist_data.parse(self.code)
        self.analyseText.setPlainText(self.stockPreText)
        
    def printSlot(self, event=None):
        pos = event[0]
        if self.stockKLine.sceneBoundingRect().contains(pos):
            mousePoint = self.stockKLine.plotItem.vb.mapSceneToView(pos)
            index = float(mousePoint.x())
            index=round(index)
            pos_y = int(mousePoint.y())
            if -1 < index < len(self.data.index):
                self.label.setHtml("<p style='color:white'><strong>Date: {0}</strong></p><p style='color:white'>Open: {1}</p><p style='color:white'>Close: {2}</p><p style='color:white'>High: <span style='color:red;'>{3}</span></p><p style='color:white'>Low: <span style='color:green;'>{4}</span></p>".format(self.axisDict[index], self.data['open'][index], self.data['close'][index],self.data['high'][index], self.data['low'][index]))
                self.label.setPos(mousePoint.x(), mousePoint.y())
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
            
                    
class SearchLineEdit(QtWidgets.QLineEdit):
    
    def __init__(self,parent=None):
        QtWidgets.QLineEdit.__init__(self,parent)
        self.initUI()
    
    #Functions:        
    def initUI(self):
        self.buttonSize=19
        self.searchIcon=QtGui.QIcon('SearchIcon.jpg')
        self.searchBtn=QtWidgets.QPushButton(self)
        self.searchBtn.setIcon(self.searchIcon)
        self.searchBtn.setMaximumSize(self.buttonSize,self.buttonSize)
        self.searchBtn.setMinimumSize(self.buttonSize,self.buttonSize)
        self.spacerItem=QtWidgets.QSpacerItem(10,10,QtWidgets.QSizePolicy.Expanding)
        self.mainLayout=QtWidgets.QHBoxLayout(self)
        
        self.mainLayout.addSpacerItem(self.spacerItem)
        self.mainLayout.addWidget(self.searchBtn)
        self.mainLayout.addSpacing(1)
        self.mainLayout.setContentsMargins(0,0,0,0)
        
        
class CandlestickItem(pg.GraphicsObject):
    
    def __init__(self,data):
        pg.GraphicsObject.__init__(self)
        self.data=data
        self.generatePicture()
        
    def generatePicture(self):
        self.picture=QtGui.QPicture()
        painter=QtGui.QPainter(self.picture)
        painter.setPen(pg.mkPen('w'))
        width=(self.data[1][0]-self.data[0][0])/3
        for (t,open,close,min,max) in self.data:
            painter.drawLine(QtCore.QPointF(t,min),QtCore.QPointF(t,max))
            if open>close:
                painter.setBrush(pg.mkBrush('g'))
            else:
                painter.setBrush(pg.mkBrush('r'))
            painter.drawRect(QtCore.QRectF(t-width,open,width*2,close-open))
        painter.end()
        
    def paint(self,painter, *args):
        painter.drawPicture(0,0,self.picture)
        
    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())