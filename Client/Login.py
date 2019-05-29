from PyQt5 import QtWidgets,QtCore
import socket

class Login(QtWidgets.QWidget):
    
    #Signals:
    serverFeedback=QtCore.pyqtSignal(str)
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
        self.setupSocket()
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
        
    def setupConnection(self):
        self.loginPushBtn.clicked.connect(self.loginBtnClicked)
        self.usernameLineEdit.returnPressed.connect(self.loginBtnClicked)
        self.passwordLineEdit.returnPressed.connect(self.loginBtnClicked)
        self.rememberCheckBox.stateChanged.connect(self.rememberStateChanged)
        self.autoLogCheckBox.stateChanged.connect(self.autologStateChanged)
        
    def setupSocket(self):
        self.loginSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        
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
        if self.usernameLineEdit.text().isalnum() and self.passwordLineEdit.text().isalnum():
            msg=self.usernameLineEdit.text()+' '+self.passwordLineEdit.text()
            msg=msg.encode()
            self.loginSocket.sendto(msg,('127.0.0.1',9999))
            resultChecked=self.loginSocket.recv(1024).decode()
            if resultChecked=='1':
                QtWidgets.QMessageBox.information(self,'Error message','The password is wrong.')
            elif resultChecked=='3':
                QtWidgets.QMessageBox.information(self,'Error message','There is no such username.')
            elif resultChecked=='2':
                self.serverFeedback.emit('1')
            else:
                QtWidgets.QMessageBox.information(self,'Error message','Can not build connection right now.') 
        else:
            QtWidgets.QMessageBox.information(self,'Error message','The username and password can only contain numbers and letters.')
    
    def rememberStateChanged(self):
        if self.rememberCheckBox.isChecked():
            pass
        else:
            self.autoLogCheckBox.setChecked(False)
        
    def autologStateChanged(self):
        if self.autoLogCheckBox.isChecked():
            self.rememberCheckBox.setChecked(True)

    