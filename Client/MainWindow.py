import Login
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.initUI()
        
    def initUI(self):
        self.login=Login.Login()
        self.setCentralWidget(self.login)