import sys
import os
import shutil
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from database.conexion import Database
from error.logger import log
from datetime import datetime

class AgregarPeliculas(QtWidgets.QWidget):
    def __init__(self):
        super(AgregarPeliculas, self).__init__()
        loadUi('ui\\agregarPelicula.ui', self)  
        
        # Conectar los botones a funciones
        self.btn_cancelar.clicked.connect(self.cancelar)  
        self.btn_aceptar.clicked.connect(self.aceptar)   
        self.btn_seleccionar_pelicula.clicked.connect(self.seleccionar_pelicula)  
    
        self.imagenes_dir = 'movies'

        # Variable para almacenar la ruta de la imagen seleccionada
        self.imagen_seleccionada = None

        # Configurar la fecha actual como fecha por defecto
        fecha_actual = QtCore.QDate.currentDate()
        self.dateEdit_estreno_mundial.setDate(fecha_actual)
        self.dateEdit_fecha_inicio.setDate(fecha_actual)
        self.dateEdit_fecha_fin.setDate(fecha_actual)

        # Habilitar la selección de fecha mediante un calendario
        self.dateEdit_estreno_mundial.setCalendarPopup(True)
        self.dateEdit_fecha_inicio.setCalendarPopup(True)
        self.dateEdit_fecha_fin.setCalendarPopup(True)

    def cancelar(self):
        self.close() 

    def aceptar(self):
        # Obtener los valores de los campos
        nombre_pelicula = self.nombre_pelicula.text()
        resumen = self.textEdit_Resumen.toPlainText()
        pais_origen = self.lineEdit_pais_origen.text()
        fecha_estreno = self.dateEdit_estreno_mundial.date().toString("yyyy-MM-dd")
        fecha_fin = self.dateEdit_fecha_fin.date().toString("yyyy-MM-dd")
        fecha_inicio = self.dateEdit_fecha_inicio.date().toString("yyyy-MM-dd")
        duracion = self.duracion.value()
        clasificacion = self.clasificacion.currentText()

        # Verificar si los campos están vacíos
        if not nombre_pelicula:
            self.mostrar_advertencia("El campo 'Nombre de la película' está vacío.")
            return
        if not resumen:
            self.mostrar_advertencia("El campo 'Resumen' está vacío.")
            return
        if not pais_origen:
            self.mostrar_advertencia("El campo 'País de Origen' está vacío.")
            return
        if not fecha_estreno:
            self.mostrar_advertencia("El campo 'Fecha de Estreno' está vacío.")
            return
        if not fecha_inicio:
            self.mostrar_advertencia("El campo 'Fecha de Inicio' está vacío.")
            return
        if not fecha_fin:
            self.mostrar_advertencia("El campo 'Fecha de Fin' está vacío.")
            return
        if duracion < 60:
            self.mostrar_advertencia("La duración debe ser como mínimo 60.")
            return
        if not self.imagen_seleccionada:
            self.mostrar_advertencia("No se ha seleccionado ninguna imagen.")
            return

        # Obtener la fecha y hora actual y formatearla
        fecha_hora_actual = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        # Concatenar el nombre de la película con la fecha y hora de guardado
        nombre_con_fecha_hora = f"{nombre_pelicula} ({fecha_hora_actual})"

        # Inicializar la variable nueva_ruta_imagen
        nueva_ruta_imagen = None

        # Si hay una imagen seleccionada, copiarla a la carpeta con el nuevo nombre
        if self.imagen_seleccionada:
            nombre_archivo_imagen = os.path.basename(self.imagen_seleccionada)
            extension = os.path.splitext(nombre_archivo_imagen)[1]  # Obtener la extensión de la imagen
            nueva_ruta_imagen = os.path.join(self.imagenes_dir, f"{nombre_con_fecha_hora}{extension}")

            # Copiar la imagen seleccionada a la carpeta destino con el nuevo nombre
            shutil.copy2(self.imagen_seleccionada, nueva_ruta_imagen)
            
            # Guardar solo el nombre del archivo con la fecha y hora en la base de datos
            nombre_archivo_guardado = f"{nombre_con_fecha_hora}{extension}"
        
        db = Database()
        try:
            db.insertar_pelicula(nombre_pelicula, resumen, pais_origen, fecha_estreno, duracion, clasificacion, nombre_archivo_guardado, fecha_inicio, fecha_fin)
            QMessageBox.information(self, 'Éxito', 'La película ha sido guardada exitosamente.')
        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', f'Ocurrió un error al guardar la película: {e}')
        
        self.close()

    def mostrar_advertencia(self, mensaje):
        # Mostrar una ventana emergente de advertencia
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setText(mensaje)
        msg_box.setWindowTitle("Advertencia")
        msg_box.exec_()

    def seleccionar_pelicula(self):
        # Abrir el explorador de archivos para seleccionar una imagen
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        archivo_imagen, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)", options=options)
        
        if archivo_imagen:
            # Obtener el nombre del archivo seleccionado
            nombre_archivo = os.path.basename(archivo_imagen)
            
            # Definir una ruta temporal para la imagen seleccionada (sin copiar todavía)
            self.imagen_seleccionada = archivo_imagen

            # Mostrar la imagen seleccionada en el QLabel 'label_peli'
            pixmap = QtGui.QPixmap(self.imagen_seleccionada)
            self.label_peli.setPixmap(pixmap)
            self.label_peli.setScaledContents(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AgregarPeliculas()
    window.show()
    sys.exit(app.exec_())

