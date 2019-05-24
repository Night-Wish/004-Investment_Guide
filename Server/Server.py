import socket

class Server():
    
    def __init__(self):
        self.setupSocket()
        
    def setupSocket(self):
        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.serverSocket.bind(('127.0.0.1',9999))
        print('Start to bind UDP on 9999. ')
        while True:
            self.dataRecv,self.addr=self.serverSocket.recvfrom(1024)
            print('Received from %s:%s.'%self.addr)
            print('Received massage: ',self.dataRecv.decode())
            self.openFile(1)
    
    def openFile(self, mode):
        self.file=open('userdata.dat','r')
        if mode==1:
            self.checkLogin()
        self.file.close()
            
    def checkLogin(self):
        usernameList=self.file.readline().split()
        passwordList=self.file.readline().split()
        recvList=self.dataRecv.decode().split()
        tempNum=0
        for tempStr in usernameList:
            if tempStr==recvList[0]:
                break
            else:
                tempNum+=1
        if tempNum==len(usernameList):
            self.serverSocket.sendto(b'3',self.addr)   #返回3表示不存在该用户名
        else:
            if recvList[1]==passwordList[tempNum]:
                self.serverSocket.sendto(b'2',self.addr)   #返回2表示登录成功
            else:
                self.serverSocket.sendto(b'1',self.addr)   #返回1表示用户名与密码不匹配