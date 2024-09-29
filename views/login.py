import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from views.principalAdmin import MainWindow  
from views.principalUser import MainWindowUser
from PyQt5.QtCore import Qt
from error.logger import log  
from PyQt5.uic import loadUi 
from views.session import UserSession  
from database.conexion import Database


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
        """ Maneja el proceso de login """
        user = self.lineEdit_Usuario.text()
        password = self.lineEdit_Contrasenia.text()

        # Crea una sesión de usuario y almacena el nombre y el correo.
        

        # Conexión y validación con la base de datos
        db = Database()
        try:
            resultado = db.obtener_usuario(user,password)
            if resultado:
                grupo=resultado[3]
                print(grupo)
                if grupo=="Administrador":
                    # Crea la sesión del usuario.
                    session = UserSession()
                    session.set_user(user, grupo)

                    self.hide()
                    self.main_window = MainWindow()
                    self.main_window.show() 
                else:
                    pass
                
            else:
                QMessageBox.warning(self, 'Error', 'Datos Incorectos.')

            #REVISAR bcrypt
            # if resultado:
                # nombre, contrasena_encriptada = resultado
                # # Verificar la contraseña encriptada
                # if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_encriptada.encode('utf-8')):
                #     # Si el login es correcto, crea la sesión y redirige a la ventana principal
                #     session = UserSession()
                #     session.set_user(nombre, email)

                #     self.hide()
                #     self.main_window = MainWindow(nombre, email)
                #     self.main_window.show()
                # else:
                #     QMessageBox.warning(self, 'Error', 'Contraseña incorrecta.')
        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', f'Ocurrió un error: {str(e)}')







        #Funca(se guarda por las dudas)
        #================
        # db_config = config_db()
        # conn = None

        # #log('iniciando lectura de dato')
        # try:
        #     conn = MySQLConnection(**db_config)
        #     if conn.is_connected():
        #         print('Conexión establecida')
        #     else:
        #         print('No se pudo conectar')

        #     cursor = conn.cursor()
        #     cursor.execute('SELECT * FROM usuarios WHERE NombreUsuario = %s AND Contrasena = %s', (nombre, contrasena))

        #     resultado = cursor.fetchone()
        #     if nombre in resultado:
        #         print("funca")
        # except Error as error:
        #     log(error, "error")
        #     QMessageBox.warning(self, 'Error', 'No se pudo finalizar el proceso debido a un error con la base de datos.')
        # finally:
        #     # Cierra la conexión con la base de datos si está abierta.
        #     if conn is not None and conn.is_connected():
        #         cursor.close()
        #         conn.close()
        
            
        # if len(nombre) < 1:
        #     QMessageBox.information(self, "Error", "Debe ingresar el usuario", QMessageBox.Ok)
        # elif len(contrasena) < 1:
        #     QMessageBox.information(self, "Error", "Debe ingresar la contraseña", QMessageBox.Ok)
        # else:
        #     # Intentar autenticar el usuario
        #     if resultado:
        #         QMessageBox.information(self, 'Éxito', 'Login exitoso.')
        #         self.hide()
        #         self.main_window = MainWindow()
        #         self.main_window.show() 
                
        #         # Aquí puedes redirigir al usuario a otra ventana si es necesario.
        #     else:
        #         QMessageBox.warning(self, 'Error', 'Usuario o contraseña incorrectos.')
            

def main():
    # Iniciar la aplicación
    app = QApplication(sys.argv)
    ventana = ClaseLogin()  # Crear la ventana de login
    ventana.show()  # Mostrar la ventana de login
    app.exec()  # Iniciar el loop de eventos

if __name__ == "__main__":
    main()
