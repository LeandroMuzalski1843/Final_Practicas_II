import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QPixmap

from PyQt5.uic import loadUi

class ClaseAgregarUsuario(QMainWindow):   
    def __init__(self,parent = None):
        super(ClaseAgregarUsuario,self).__init__(parent)
        loadUi("ui\\agregarUsuario.ui",self)
        self.setup()
    def setup(self):
        pass
        

def main ():
    app = QApplication(sys.argv)
    ventana = ClaseAgregarUsuario()
    ventana.show()
    app.exec()

if __name__ =="__main__":
    main()