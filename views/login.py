import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from views.principalAdmin import MainWindow  
from views.principalUser import MainWindowUser
from PyQt5.QtCore import Qt
from error.logger import log  
from PyQt5.uic import loadUi 
from views.session import UserSession  
from mysql.connector import MySQLConnection, Error  
from database.python_mysql_config import config_db  

class ClaseLogin(QMainWindow):   
    def __init__(self, parent=None):
        super(ClaseLogin, self).__init__(parent)
        try:
            # Cargar el diseño de la interfaz de usuario
            loadUi("ui\\login.ui", self)
            self.setup()

            # Eliminar la barra de título de la ventana y ajustar la opacidad
            self.setWindowFlags(Qt.FramelessWindowHint) 
            self.setWindowOpacity(1.0)  # Opacidad completa (1.0 es totalmente opaco)

        except FileNotFoundError as error:
            log(error, "error")  # Registrar el error en el log
            QMessageBox.critical(self, 'Error', 'El programa no pudo encontrar la pantalla de login. Consulte con el administrador.')
            sys.exit(1)  # Cerrar la aplicación si hay un error crítico

    def setup(self):
        # Conectar el botón de aceptar con el método para procesar el login
        self.btn_aceptar.clicked.connect(self.aceptar_clicked)
        self.btn_cancelar.clicked.connect(self.close)

    def aceptar_clicked(self):
        # Manejar el proceso de login
        nombre=self.lineEdit_Usuario.text()
        contrasena = self.lineEdit_Contrasenia.text()

        #Basico por editar
        if len(nombre) < 1:
            print("Error en el nombre de usuario")
            QMessageBox.information(self,"Error","Debe ingresar el usuario",QMessageBox.Ok)
        elif len(contrasena) < 1:
            QMessageBox.information(self,"Error","Debe ingresar la contraseña",QMessageBox.Ok)
        else:
            if nombre == "leo":
                if contrasena == "123":
                    self.hide()
                    self.main_window = MainWindow()
                    self.main_window.show()
                else:
                    QMessageBox.warning(self,"Error","Contraseña incorrecta",QMessageBox.Ok)
            elif nombre == "juan":
                if contrasena == "456":
                    self.hide()
                    self.main_window_user = MainWindowUser()
                    self.main_window_user.show()
                else:
                    QMessageBox.warning(self,"Error","Contraseña incorrecta",QMessageBox.Ok)
            else:
                QMessageBox.warning(self,"Error","Usuario incorrecta",QMessageBox.Ok)

            
        # Corregir con el profe
        # self.login()

    def login(self):
        # Obtener los valores ingresados en los campos de email y contraseña
        email = self.lineEdit_Usuario.text()
        contrasena = self.lineEdit_Contrasenia.text()

        # INICIO: Código de prueba, luego borrar
        nombre = "juan"  # Nombre de usuario ficticio para pruebas


        # Almacena la sesión
        session = UserSession()
        session.set_user(nombre, email)

        # Ocultar la ventana de login
        self.hide()

        # Muestra la ventana principal con el nombre y email del usuario
        self.main_window = MainWindow(nombre, email)
        self.main_window.show()
        # FIN: Código de prueba, luego borrar

        """ 
        try:
            # Configuración de la base de datos
            db_config = config_db()
            db = MySQLConnection(**db_config)
            cursor = db.cursor()

            # Ejecutar la consulta para verificar si el usuario existe
            cursor.execute("SELECT nombre, password FROM usuarios WHERE email = %s", (email,))
            resultado = cursor.fetchone()
        except Error as error:
            # Registrar el error en el log y mostrar un mensaje de advertencia
            log(error, "error")
            QMessageBox.warning(self, 'Error', 'No se pudo finalizar el proceso debido a un error con la base de datos.')
        finally:
            # Cerrar la conexión con la base de datos
            if db is not None and db.is_connected():
                cursor.close()
                db.close()

        # Si el email existe en la base de datos
        if resultado:
            nombre, contrasena_encriptada = resultado
            # Verificar si la contraseña ingresada coincide con la encriptada
            if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_encriptada.encode('utf-8')):
                # Almacenar la sesión del usuario
                session = UserSession()
                session.set_user(nombre, email)

                # Ocultar la ventana de login y abrir la principal
                self.hide()
                self.main_window = MainWindow(nombre, email)
                self.main_window.show()
            else:
                # Mostrar mensaje si la contraseña es incorrecta
                QMessageBox.warning(self, 'Error', 'Contraseña incorrecta.')
        else:
            # Mostrar mensaje si el email no se encuentra en la base de datos
            QMessageBox.warning(self, 'Error', 'Email no encontrado.')
        """

def main():
    # Iniciar la aplicación
    app = QApplication(sys.argv)
    ventana = ClaseLogin()  # Crear la ventana de login
    ventana.show()  # Mostrar la ventana de login
    app.exec()  # Iniciar el loop de eventos

if __name__ == "__main__":
    main()
