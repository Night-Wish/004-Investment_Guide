import pyqtgraph as pg
from PyQt5 import QtGui,QtCore

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