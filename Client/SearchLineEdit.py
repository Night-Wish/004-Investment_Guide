from PyQt5 import QtWidgets,QtGui,QtCore

class SearchLineEdit(QtWidgets.QLineEdit):
    
    def __init__(self,parent=None):
        QtWidgets.QLineEdit.__init__(self,parent)
        self.initUI()
        
    def initUI(self):
        self.buttonSize=19
        self.searchIcon=QtGui.QIcon('SearchIcon.jpg')
        self.searchBtn=QtWidgets.QPushButton(self)
        self.searchBtn.setIcon(self.searchIcon)
        self.searchBtn.setMaximumSize(self.buttonSize,self.buttonSize)
        self.searchBtn.setMinimumSize(self.buttonSize,self.buttonSize)
        self.spacerItem=QtWidgets.QSpacerItem(10,10,QtWidgets.QSizePolicy.Expanding)
        self.mainLayout=QtWidgets.QHBoxLayout(self)
        
        self.searchBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.mainLayout.addSpacerItem(self.spacerItem)
        self.mainLayout.addWidget(self.searchBtn)
        self.mainLayout.addSpacing(1)
        self.mainLayout.setContentsMargins(0,0,0,0)