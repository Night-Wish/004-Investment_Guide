'''
请对Spyder进行设置：
Run-> Configuration per file-> General Settings-> Remove all variables before execution. 
这项设置非常重要，否则程序会因为重复调用而崩溃。

Anaconda应该默认装好了PyQt5，如果没有，可以在Anaconda Navigator的Environments中找到并装好
或在Anaconda Prompt中输入命令“pip install PyQt5”安装

该程序仅作为教程，实际程序不会有这么多注释
'''

from PyQt5 import QtWidgets,QtCore
#从PyQt5的包中导入这两个组件，其中QtCore为所有Qt程序必须包括的，QtWidgets为Qt的控件基类
import sys
#这个组件主要是为迎合Qt的C++本性，相当于获取int main(*argv,*args)的两个参数
#我们不会涉及使用，但Qt仍对此有要求

class Login(QtWidgets.QWidget):
#这里创建了一个Login类，该类继承自QtWidgets.QWidget
#相当于我们在QWidget的基础上创建一个自定义Widget
#在Qt中，这句类的声明写为：class Login : public QWidget {...}
    def __init__(self,parent=None):
#在Python中，__init__是类的构造函数的标准格式，不允许更改
#类会在被声明创建的时候自动调用__init__
#一般而言，__XX__格式的函数都是该类的隐式函数，不会显式调用
#在C++中，构造函数的名字与类的名称一样，且没有类型（在C++中这非常特殊），如Login类的构造函数为：Login()

#对于两个参数，在Python面向对象编程中，类下的任何一个函数都必须传入self，我也不知道为什么，反正C++不用
#第二个参数为父窗口，用于下面一条语句，且已经在声明时定义为None，表明我们的Login在调用时，如果不特殊声明，没有父窗口
#传入parent参数是Qt的构造函数的必须参数，这点会在下面有体现
        QtWidgets.QWidget.__init__(self,parent)
#这条语句显式调用了QWidget的构造函数，且将Login的parent传入
#这么做是因为Login的基类是QWidget，言外之意，我们只是在QWidget上增加自己的东西，因此QWidget部分也需要创建
#在C++中，这种做法就方便许多，语句为：Login(QWidget *parent) : QWidget(parent)
#当然，我个人认为，难理解许多，反正我也是最近才理解的
        self.initUI()
#这里将控件的创造过程封装成一个函数，并在类的构造函数中调用，这么做主要是为了控制构造函数的长度，维护可读性
    
    def initUI(self):
        self.usernameLabel=QtWidgets.QLabel('Username:')
#这里创建了一个QLabel，并在QLabel中初始化显示字符串'Username:'
#QLabel是Qt中使用最广泛的控件，它可以显示文字也可以显示图片QPixmap
        self.usernameLineEdit=QtWidgets.QLineEdit(self)
#这里创建了一个QLineEdit，作为用户输入用户名的控件
#将self参数传给它是告诉程序该控件的父窗口为Login
        self.passwordLabel=QtWidgets.QLabel('Password:')
        self.passwordLineEdit=QtWidgets.QLineEdit(self)
        self.rememberCheckBox=QtWidgets.QCheckBox('Remember')
#这里创建了一个QCheckBox，作为用户进行登陆设置的地方，初始化其显示的字符串为'Remember'
        self.autoLogCheckBox=QtWidgets.QCheckBox('Auto Login')
        self.loginPushBtn=QtWidgets.QPushButton('Login')
#这里创建了一个QPushButton，作为用户点击的按钮，初始字符串为'Login'
        
        
        self.mainLayout=QtWidgets.QGridLayout(self)
#这里创建了一个网格布局器QGridLayout，布局器作为各个控件的容器对它们进行排版
#self意味着该布局器mainLayout的父窗口是Login，也意味着Login将直接使用mainLayout作为其布局
#也可以在此不声明mainLayout的父窗口为self，而在之后从self的角度调用self.setLayout(mainLayout)
        self.mainLayout.addWidget(self.usernameLabel,0,0)
#这个语句即，将usernameLabel放在布局器的第0行，第0列
        self.mainLayout.addWidget(self.usernameLineEdit,0,1,1,2)
#这个语句即，将usernameLineEdit放在布局器的第0行，第1列，且它跨1行，跨2列
#多出来的两个参数即代表columnStretch跨行数，rowStretch跨列数
#实际上，在以后可能会接触的HTML中，都是这样表述的
#下面同理
        self.mainLayout.addWidget(self.passwordLabel,1,0)
        self.mainLayout.addWidget(self.passwordLineEdit,1,1,1,2)
        self.mainLayout.addWidget(self.rememberCheckBox,2,0)
        self.mainLayout.addWidget(self.autoLogCheckBox,2,1)
        self.mainLayout.addWidget(self.loginPushBtn,2,2)
        

if __name__ == '__main__':
#Qt，同C++，要求程序必须有一个main函数，这也是这个代码块存在的意义
#为什么这样表述，我也不清楚
    app=QtWidgets.QApplication(sys.argv)
#这里需要创建一个QApplication实例，是所有Qt程序必须有的一步，其来源于QtCore
    login=Login()
#这里创建了一个Login类，创建的时候便会调用其构造函数Login.__init__()
    login.setWindowTitle('Login')
#Login类的这个操作继承自QWidget，是用于改变窗口名称的
    login.show()
#最后调用show()函数显示我们的窗体
    sys.exit(app.exec())
#这一操作便是将操作权从main函数交给Qt库，其具体细节我也尚不了解