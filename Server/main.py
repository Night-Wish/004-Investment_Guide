import sys
import Server
from PyQt5 import QtWidgets

if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    server=Server.Server()
    server.show()
    sys.exit(app.exec())