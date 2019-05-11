import Login
import StockBrowser
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.initUI()
        self.setupConnection()
        
    def initUI(self):
        self.login=Login.Login()
        self.setCentralWidget(self.login)
        self.icon=QIcon('loginIcon(Temporary).jpg')
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Login')
        
    def setupConnection(self):
        self.login.serverFeedback.connect(self.feedbackReceived)
        
    def feedbackReceived(self,feedback):
        if feedback == '1':
            self.stockBrowser=StockBrowser.StockBrowser()
            self.login.close()
            self.setCentralWidget(self.stockBrowser)
            self.resize(800,400)
