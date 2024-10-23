# database.py
from mysql.connector import MySQLConnection, Error
from PyQt5.QtWidgets import QMessageBox
from database.python_mysql_config import config_db
from error.logger import log  
from datetime import datetime

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
    
    def obtener_usuario_por_id(self, user_id):
        """Obtiene el usuario por su ID."""
        try:
            self.conneccion()
            self.cursor.execute('SELECT * FROM usuarios WHERE IdUsuarios = %s', (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            log(e, "error")
            raise Exception(f"Error durante la consulta: {e}")
        finally:
            self.desconeccion()


    def obtener_usuario(self, nombre):
        """Obtiene el usuario """
        try:
            self.conneccion()
            self.cursor.execute('SELECT * FROM usuarios WHERE NombreUsuario = %s', (nombre,))
            return self.cursor.fetchone()
        except Error as e:
            log(e, "error")
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
            log(e, "error")
            raise Exception(f"Error durante la consulta: {e}")
        finally:
            self.desconeccion()
    
    def insertar_usuario(self, nombre, contrasena, rol,feha_creacion):
        """Inserta un nuevo usuario con un rol en la base de datos."""
        try:
            self.conneccion()
            query = "INSERT INTO usuarios (NombreUsuario, Contrasena,Grupo,FechaCreacion) VALUES (%s, %s, %s,%s)"
            self.cursor.execute(query, (nombre, contrasena, rol,feha_creacion))
            self.db.commit()  
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al insertar usuario: {e}")
        finally:
            self.desconeccion()

    def eliminar_usuario(self, user_id):
        """Elimina un usuario de la base de datos por su ID."""
        try:
            self.conneccion()
            query = "DELETE FROM usuarios WHERE IdUsuarios = %s"
            self.cursor.execute(query, (user_id,))
            self.db.commit()  
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al eliminar usuario: {e}")
        finally:
            self.desconeccion()

    def actualizar_ultimo_acceso(self, user_id):
        """Actualiza el último acceso del usuario en la base de datos."""
        try:
            self.conneccion()
            query = "UPDATE usuarios SET FechaUltimoAcceso = %s WHERE IdUsuarios = %s"
            self.cursor.execute(query, (datetime.now(), user_id))
            self.db.commit()  
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al eliminar usuario: {e}")
        finally:
            self.desconeccion()
    
    def modificar_usuario(self, user_id, nuevo_nombre, nueva_contrasena, nuevo_rol, fecha_modificacion):
        """Modifica los datos de un usuario en la base de datos."""
        try:
            self.conneccion()  
            query = """UPDATE usuarios 
                    SET NombreUsuario = %s, Contrasena = %s, Grupo = %s, FechaModificacion = %s
                    WHERE IdUsuarios = %s"""
            self.cursor.execute(query, (nuevo_nombre, nueva_contrasena, nuevo_rol, fecha_modificacion, user_id))
            self.db.commit()
            
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al modificar usuario: {e}")
            
        finally:
            self.desconeccion() 
    
    def obtener_peliculas(self):
        """Obtiene todas las películas de la base de datos."""
        try:
            self.conneccion()
            self.cursor.execute("SELECT * FROM peliculas")  
            return self.cursor.fetchall()
        except Error as e:
            log(e, "error")
            raise Exception(f"Error durante la consulta de películas: {e}")
        finally:
            self.desconeccion()
    
    # def insertar_pelicula(self, nombre_pelicula, resumen, pais_origen, fecha_estreno, duracion, clasificacion, imagen_ruta,fecha_inicio,fecha_fin):
    #     """Inserta una nueva película en la base de datos."""
    #     try:
    #         self.conneccion()
    #         query = """
    #         INSERT INTO peliculas (NombrePelicula, Resumen, PaisOrigen, FechaEstreno, Duracion,FechaEstrenoMundial,FechaInicio,FechaFin, Clasificacion, Imagen)
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    #         """
    #         self.cursor.execute(query, (nombre_pelicula, resumen, pais_origen, fecha_estreno, duracion,fecha_inicio,fecha_fin, clasificacion, imagen_ruta))
    #         self.db.commit()
    #     except Error as e:
    #         log(e, "error")
    #         raise Exception(f"Error al insertar película: {e}")
    #     finally:
    #         self.desconeccion()
    
    #Solucion ChatGPT
    def insertar_pelicula(self, nombre, resumen, pais_origen, fecha_estreno, duracion, clasificacion, imagen_ruta, fecha_inicio, fecha_fin):
        """Inserta una nueva película en la base de datos y retorna el ID de la película."""
        try:
            self.conneccion()

            # Consulta SQL para insertar en la base de datos
            query = """
            INSERT INTO peliculas (NombrePelicula, Resumen, Imagen, PaisOrigen, FechaEstrenoMundial, FechaInicio, FechaFin, Duracion, Clasificacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (nombre, resumen, imagen_ruta, pais_origen, fecha_estreno, fecha_inicio, fecha_fin, duracion, clasificacion)

            self.cursor.execute(query, valores)
            self.db.commit()  # Confirmar la transacción

            # Obtener el ID de la película recién insertada
            return self.cursor.lastrowid

        except Error as e:
            log(e, "error")
            raise Exception(f"Error al insertar película: {e}")

        finally:
            self.desconeccion()

    def modificar_pelicula(self, idPelicula, nombre, resumen, pais_origen, fecha_estreno,duracion, clasificacion, imagen_ruta, fecha_inicio, fecha_fin):
        """Modifica los datos de una película existente en la base de datos."""
        try:
            self.conneccion()

            # Consulta SQL para actualizar la película
            query = """
                    UPDATE peliculas
                    SET NombrePelicula = %s, Resumen = %s, Imagen = %s, PaisOrigen = %s,
                        FechaEstrenoMundial = %s, FechaInicio = %s, FechaFin = %s, 
                        Duracion = %s, Clasificacion = %s
                    WHERE IdPelicula = %s
                """
            valores = (nombre, resumen, imagen_ruta, pais_origen, fecha_estreno, 
                    fecha_inicio, fecha_fin, duracion, clasificacion, idPelicula)

            self.cursor.execute(query, valores)
            self.db.commit()  # Confirmar la transacción

            if self.cursor.rowcount > 0:
                return True  # Retornar True si se actualizó con éxito
            else:
                raise Exception(f"No se encontró la película con Id {idPelicula}")

        except Exception as e:
            log(e, "error")
            raise Exception(f"Error al actualizar película: {e}")

        finally:
            self.desconeccion()



    def eliminar_pelicula(self, pelicula_id):
        """Elimina una película de la base de datos por su ID."""
        try:
            self.conneccion()
            query = "DELETE FROM peliculas WHERE IdPelicula = %s"
            self.cursor.execute(query, (pelicula_id,))
            self.db.commit()  # Confirma los cambios en la base de datos.
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al eliminar película: {e}")
        finally:
            self.desconeccion()
    
    def obtener_generos(self):
        """Obtiene todos los géneros de la base de datos."""
        try:
            self.conneccion()
            self.cursor.execute("SELECT * FROM generos")  
            return self.cursor.fetchall()
        except Error as e:
            log(e, "error")
            raise Exception(f"Error durante la consulta de géneros: {e}")
        finally:
            self.desconeccion()

    def insertar_generos(self, id_pelicula, id_genero):
        """Inserta un registro en la tabla peliculagenero."""
        try:
            self.conneccion()
            query = """
            INSERT INTO peliculagenero (IdPelicula, IdGenero)
            VALUES (%s, %s)
            """
            valores = (id_pelicula, id_genero)
            self.cursor.execute(query, valores)
            self.db.commit()
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al insertar el género para la película: {e}")
        finally:
            self.desconeccion()
    
    def obtener_generos_pelicula(self, pelicula_id):
        """Obtiene los géneros asociados a una película por su ID."""
        try:
            self.conneccion()
            query = """
            SELECT g.NombreGenero 
            FROM peliculagenero pg
            JOIN generos g ON pg.IdGenero = g.IdGeneros
            WHERE pg.IdPelicula = %s
            """
            self.cursor.execute(query, (pelicula_id,))
            return [row[0] for row in self.cursor.fetchall()]  # Retorna una lista de nombres de géneros
        except Error as e:
            log(e, "error")
            raise Exception(f"Error durante la consulta de géneros de la película: {e}")
        finally:
            self.desconeccion()


    def obtener_id_genero_por_nombre(self, nombre_genero):
        """Obtiene el ID de un género por su nombre."""
        try:
            self.conneccion()
            query = "SELECT IdGeneros FROM generos WHERE NombreGenero = %s"
            self.cursor.execute(query, (nombre_genero,))
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado else None
        except Error as e:
            log(e, "error")
            raise Exception(f"Error al obtener el ID del género: {e}")
        finally:
            self.desconeccion()
    
    def obtener_datos_pelicula(self, pelicula_id):
        """Obtiene los datos de una película por su ID."""
        try:
            self.conneccion()
            query = "SELECT NombrePelicula, Resumen, PaisOrigen, FechaEstrenoMundial, FechaInicio, FechaFin, Duracion, Clasificacion, Imagen FROM peliculas WHERE IdPelicula = %s"
            self.cursor.execute(query, (pelicula_id,))
            resultado = self.cursor.fetchone()

            if resultado:
                # Mapear los resultados a un diccionario
                datos_pelicula = {
                    'nombre': resultado[0],
                    'resumen': resultado[1],
                    'pais_origen': resultado[2],
                    'fecha_estreno': resultado[3],
                    'fecha_inicio': resultado[4],
                    'fecha_fin': resultado[5],
                    'duracion': resultado[6],
                    'clasificacion': resultado[7],
                    'imagen': resultado[8]
                }
                return datos_pelicula
            else:
                return None

        except Error as e:
            log(e, "error")
            raise Exception(f"Error durante la consulta de la película: {e}")
        
        finally:
            self.desconeccion()
