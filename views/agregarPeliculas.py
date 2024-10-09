import sys
import os
import shutil
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from database.conexion import Database
from error.logger import log
class AgregarPeliculas(QtWidgets.QWidget):
    def __init__(self):
        super(AgregarPeliculas, self).__init__()
        loadUi('ui\\agregarPelicula.ui', self)  # Carga el archivo .ui
        
        # Conectar los botones a funciones
        self.btn_cancelar.clicked.connect(self.cancelar)  # Botón "Cancelar"
        self.btn_aceptar.clicked.connect(self.aceptar)   # Botón "Aceptar"
        self.btn_seleccionar_pelicula.clicked.connect(self.seleccionar_pelicula)  # Botón "Seleccionar Pelicula"
        
        # Crear una carpeta para guardar las imágenes si no existe
        self.imagenes_dir = 'movies'
        if not os.path.exists(self.imagenes_dir):
            os.makedirs(self.imagenes_dir)

        # Variable para almacenar la ruta de la imagen seleccionada
        self.imagen_seleccionada = None

    def cancelar(self):
        # Acción al hacer clic en "Cancelar"
        print("Cancelado")
        self.close()  # Cerrar la ventana

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
        if duracion <= 0:
            self.mostrar_advertencia("La duración debe ser mayor a 0.")
            return
        if not self.imagen_seleccionada:
            self.mostrar_advertencia("No se ha seleccionado ninguna imagen.")
            return

        # Si todos los campos están completos, continúa con la lógica de aceptar
        db = Database()
        try:
            db.insertar_pelicula(nombre_pelicula, resumen, pais_origen, fecha_estreno, duracion, clasificacion, self.imagen_seleccionada,fecha_inicio,fecha_fin)
            QMessageBox.information(self, 'Éxito', 'La película ha sido guardada exitosamente.')
        except Exception as e:
            log(e,"error")
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
            
            # Definir la ruta de destino donde se guardará la imagen seleccionada
            destino = os.path.join(self.imagenes_dir, nombre_archivo)
            
            # Copiar la imagen seleccionada a la carpeta destino
            shutil.copy(archivo_imagen, destino)
            print(f"Imagen seleccionada: {archivo_imagen}")
            print(f"Imagen guardada en: {destino}")

            # Mostrar la imagen seleccionada en el QLabel 'label_peli'
            pixmap = QtGui.QPixmap(destino)
            self.label_peli.setPixmap(pixmap)
            self.label_peli.setScaledContents(True)

            # Almacenar la ruta de la imagen seleccionada
            self.imagen_seleccionada = destino

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AgregarPeliculas()
    window.show()
    sys.exit(app.exec_())
