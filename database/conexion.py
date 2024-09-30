# database.py
from mysql.connector import MySQLConnection, Error
from PyQt5.QtWidgets import QMessageBox
from database.python_mysql_config import config_db
from error.logger import log  

class Database:
    def __init__(self):
        self.db = None
        self.cursor = None

    def conneccion(self):
        """Establece conexión con la base de datos."""
        try:
            db_config = config_db()
            self.db = MySQLConnection(**db_config)
            self.cursor = self.db.cursor()
        except Error as error:
            log(error, "error")
            QMessageBox.warning(self, 'Error', 'No se pudo finalizar el proceso debido a un error con la base de datos.')

    def desconeccion(self):
        """Cierra la conexión a la base de datos."""
        if self.cursor:
            self.cursor.close()
        if self.db and self.db.is_connected():
            self.db.close()

    def obtener_usuario(self, nombre,contrasena):
        """Obtiene el usuario """
        try:
            self.conneccion()
            self.cursor.execute('SELECT * FROM usuarios WHERE NombreUsuario = %s AND Contrasena = %s', (nombre, contrasena))
            return self.cursor.fetchone()
        except Error as e:
            raise Exception(f"Error durante la consulta: {e}")
        finally:
            self.desconeccion()

    def obtener_usuarios(self):
        """Obtiene todos los usuarios de la base de datos."""
        try:
            self.conneccion()
            self.cursor.execute("SELECT * FROM usuarios") 
            return self.cursor.fetchall()
        except Error as e:
            raise Exception(f"Error durante la consulta: {e}")
        finally:
            self.desconeccion()
    
    def insertar_usuario(self, nombre, contrasena, rol):
        """Inserta un nuevo usuario con un rol en la base de datos."""
        try:
            self.conneccion()
            query = "INSERT INTO usuarios (NombreUsuario, Contrasena,Grupo) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (nombre, contrasena, rol))
            self.db.commit()  # Confirmar los cambios
        except Error as e:
            raise Exception(f"Error al insertar usuario: {e}")
        finally:
            self.desconeccion()

    def eliminar_usuario(self, user_id):
        """Elimina un usuario de la base de datos por su ID."""
        try:
            self.conneccion()
            query = "DELETE FROM usuarios WHERE IdUsuarios = %s"
            self.cursor.execute(query, (user_id,))
            self.db.commit()  # Confirmar los cambios
        except Error as e:
            raise Exception(f"Error al eliminar usuario: {e}")
        finally:
            self.desconeccion()