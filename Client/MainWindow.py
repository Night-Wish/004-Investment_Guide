import Login
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self,parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.initUI()
        
    def initUI(self):
        self.login=Login.Login()
        self.setCentralWidget(self.login)
        self.icon=QIcon('loginIcon(Temporary).jpg')
        self.setWindowIcon(self.icon)
        self.setWindowTitle('Login')