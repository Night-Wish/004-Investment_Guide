import MainWindow
import sys
from PyQt5 import QtWidgets

if __name__=='__main__':
    print('About to start Client...')
    app=QtWidgets.QApplication(sys.argv)
    mainWindow=MainWindow.MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
    print('Started Client...')