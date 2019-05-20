from PyQt5 import QtWidgets,QtNetwork

class Server(QtWidgets.QWidget):
    
    def __init__(self,parent=None):
        QtWidgets.QWidget.__init__(self,parent)
        self.initUI()
        self.setupSocket()
        self.setupConnection()
        
    def initUI(self):
        self.msgBrowser=QtWidgets.QTextBrowser()
        self.mainLayout=QtWidgets.QGridLayout(self)
        self.mainLayout.addWidget(self.msgBrowser)
        
        self.setWindowTitle('Server')
        
    def setupSocket(self):
        self.serverSocket=QtNetwork.QUdpSocket(self)
        self.serverSocket.bind(QtNetwork.QHostAddress.LocalHost,9999)
    
    
    def setupConnection(self):
        self.serverSocket.readyRead.connect(self.readData)
        
    def readData(self):
        while self.serverSocket.hasPendingDatagrams():
            datagram,host,port=self.serverSocket.readDatagram(self.serverSocket.pendingDatagramSize())
            datagram=datagram.decode()
            self.msgBrowser.append(datagram)