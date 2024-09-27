import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

class AgregarUsuario(QMainWindow):   
    def __init__(self,parent = None):
        super(AgregarUsuario,self).__init__(parent)
        loadUi("ui\\agregarUsuario.ui",self)

def main():
    app = QApplication(sys.argv)
    ventana = AgregarUsuario()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
