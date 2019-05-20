from PyQt5 import QtWidgets,QtCore,QtNetwork

class Login(QtWidgets.QWidget):
    
    #Signals:
    serverFeedback=QtCore.pyqtSignal(str)
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
        self.setupSocket()
        self.setupLoginSettings()
        self.setupConnection()
        
    #Functions:
    def initUI(self):
        self.usernameLabel=QtWidgets.QLabel('Username:')
        self.usernameLineEdit=QtWidgets.QLineEdit(self)
        self.usernameLineEdit.setPlaceholderText('Input your username')
        self.passwordLabel=QtWidgets.QLabel('Password:')
        self.passwordLineEdit=QtWidgets.QLineEdit(self)
        self.passwordLineEdit.setPlaceholderText('Input your password')
        self.passwordLineEdit.setEchoMode(self.passwordLineEdit.Password)
        self.rememberCheckBox=QtWidgets.QCheckBox('Remember')
        self.autoLogCheckBox=QtWidgets.QCheckBox('Auto Login')
        self.loginPushBtn=QtWidgets.QPushButton('Login')
        
        self.mainLayout=QtWidgets.QGridLayout(self)
        self.mainLayout.addWidget(self.usernameLabel,0,0)
        self.mainLayout.addWidget(self.usernameLineEdit,0,1,1,2)
        self.mainLayout.addWidget(self.passwordLabel,1,0)
        self.mainLayout.addWidget(self.passwordLineEdit,1,1,1,2)
        self.mainLayout.addWidget(self.rememberCheckBox,2,0)
        self.mainLayout.addWidget(self.autoLogCheckBox,2,1)
        self.mainLayout.addWidget(self.loginPushBtn,2,2)
        
        self.setWindowTitle("Login")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
    def setupLoginSettings(self):
        file=QtCore.QFile('remember.dat')
        if not file.open(QtCore.QIODevice.Text and QtCore.QIODevice.ReadOnly):
            return
        textStream=QtCore.QTextStream(file)
        username=textStream.readLine()
        if username=='':
            return
        else:
            self.usernameLineEdit.setText(username)
            self.rememberCheckBox.setChecked(True)
            password=textStream.readLine()
            if password=='':
                return
            else:
                self.passwordLineEdit.setText(password)
                self.autoLogCheckBox.setChecked(True)
                self.loginBtnClicked()
        file.close()
        
    def setupConnection(self):
        self.loginPushBtn.clicked.connect(self.loginBtnClicked)
        self.usernameLineEdit.returnPressed.connect(self.loginBtnClicked)
        self.passwordLineEdit.returnPressed.connect(self.loginBtnClicked)
        
    def setupSocket(self):
        self.loginSocket=QtNetwork.QUdpSocket(self)
        
    def saveLoginSettings(self):
        file=QtCore.QFile('remember.dat')
        if not file.open(QtCore.QIODevice.Text and QtCore.QIODevice.WriteOnly):
            print(1)
            return
        textStream=QtCore.QTextStream(file)
        if self.rememberCheckBox.isChecked():
            textStream<<self.usernameLineEdit.text()
        if self.autoLogCheckBox.isChecked():
            textStream<<'\n'<<self.passwordLineEdit.text()
        file.close()
        
    #Slots:
    def loginBtnClicked(self):
        self.saveLoginSettings()
        msg='0:'+self.usernameLineEdit.text()+' '+self.passwordLineEdit.text()
        msg=msg.encode()
        self.loginSocket.writeDatagram(msg,QtNetwork.QHostAddress.LocalHost,9999)
        