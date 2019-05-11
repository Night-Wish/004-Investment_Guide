from PyQt5 import QtWidgets,QtCore

class Login(QtWidgets.QWidget):
    
    serverFeedback=QtCore.pyqtSignal(str)
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
        self.arrangeUI()
        self.setupConnection()
        
    def initUI(self):
        self.usernameLabel=QtWidgets.QLabel('Username:')
        self.usernameLineEdit=QtWidgets.QLineEdit(self)
        self.passwordLabel=QtWidgets.QLabel('Password:')
        self.passwordLineEdit=QtWidgets.QLineEdit(self)
        self.rememberCheckBox=QtWidgets.QCheckBox('Remember')
        self.autoLogCheckBox=QtWidgets.QCheckBox('Auto Login')
        self.loginPushBtn=QtWidgets.QPushButton('Login')
        
        self.mainLayout=QtWidgets.QGridLayout(self)
        
        self.setWindowTitle("Login")
        
    def arrangeUI(self):
        self.mainLayout.addWidget(self.usernameLabel,0,0)
        self.mainLayout.addWidget(self.usernameLineEdit,0,1,1,2)
        self.mainLayout.addWidget(self.passwordLabel,1,0)
        self.mainLayout.addWidget(self.passwordLineEdit,1,1,1,2)
        self.mainLayout.addWidget(self.rememberCheckBox,2,0)
        self.mainLayout.addWidget(self.autoLogCheckBox,2,1)
        self.mainLayout.addWidget(self.loginPushBtn,2,2)
        
    def setupConnection(self):
        self.loginPushBtn.clicked.connect(self.loginBtnClicked)
        
    def loginBtnClicked(self):
        self.serverFeedback.emit('1')