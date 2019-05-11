from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import tushare as ts
import numpy as np
class StockBrowser(QtWidgets.QWidget):
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
    
    def initUI(self):
        self.searchLineEdit=QtWidgets.QLineEdit()
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