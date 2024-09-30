# agregarUsuario.py

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from database.conexion import Database
from error.logger import log

class AgregarUsuario(QMainWindow):   
    def __init__(self, parent=None):
        super(AgregarUsuario, self).__init__(parent)
        loadUi("ui\\agregarUsuario.ui", self)

        # Conectar el botón de guardar a la función para agregar usuario
        self.btnAceptar_3.clicked.connect(self.agregar_usuario)

        # Configurar el valor por defecto del comboBox
        self.comboBoxUsuario.setCurrentText("Administrador")

    def validar_contrasena(self, contrasena):
        """Verifica si la contraseña cumple con los requisitos mínimos."""
        # Requisitos: al menos 8 caracteres
        if len(contrasena) < 8:
            return False
        # Puedes añadir más validaciones como la presencia de números, caracteres especiales, etc.
        return True
    
    def agregar_usuario(self):
        """Obtiene los datos del formulario y los inserta en la base de datos."""
        nombre = self.lineEdit_Nombre.text()
        contrasena = self.lineEdit_Contrasenia.text()
        rol = self.comboBoxUsuario.currentText()  # Obtener el rol seleccionado

        if not nombre:
            QMessageBox.warning(self, 'Advertencia', 'El campo de nombre de usuario es obligatorio.')
            return

        if not contrasena:
            QMessageBox.warning(self, 'Advertencia', 'El campo de contraseña es obligatorio.')
            return
        
        if not self.validar_contrasena(contrasena):
            QMessageBox.warning(self, 'Advertencia', 'La contraseña debe tener al menos 8 caracteres.')
            return
        # Insertar usuario en la base de datos
        try:
            db = Database()
            db.insertar_usuario(nombre, contrasena, rol)
            QMessageBox.information(self, 'Éxito', 'Usuario agregado correctamente.')

            self.close()
            # # Limpiar los campos después de guardar
            # self.lineEdit_Nombre.clear()
            # self.lineEdit_Contrasenia.clear()
            # self.comboBoxUsuario.setCurrentText("Administrador")  # Resetear el ComboBox al valor por defecto
        except Exception as error:
            log(error, "error")  
            QMessageBox.critical(self, 'Error', f"Hubo un error al agregar el usuario: {error}")

def main():
    app = QApplication(sys.argv)
    ventana = AgregarUsuario()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
