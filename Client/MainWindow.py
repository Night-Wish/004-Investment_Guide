import Login
import StockBrowser
from PyQt5 import QtWidgets,QtGui

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self,parent=None):
        print('Initializing mainwindow')
        QtWidgets.QMainWindow.__init__(self,parent)
        self.initUI()
        self.setupConnection()
        self.login.setupLoginSettings()
        print('Initialized mainwindow')
        
    #Functions:
    def initUI(self):
        print('Initializing the UI of mainwindow...')
        self.login=Login.Login()
        self.setCentralWidget(self.login)
        self.icon=QtGui.QIcon('loginIcon(Temporary).jpg')
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Login')
        print('Initialized the UI of mainwindow')
        
    def setupConnection(self):
        print('Setting up connections...')
        self.login.serverFeedback.connect(self.feedbackReceived)
        print('Setup connections')
    #Slots:
    def feedbackReceived(self,feedback):
        print('Feedback Received...')
        if feedback == '1':
            self.stockBrowser=StockBrowser.StockBrowser()
            self.login.close()
            self.setCentralWidget(self.stockBrowser)
            self.resize(1000,500)
            self.setWindowTitle('Quantum Investment Guide')
