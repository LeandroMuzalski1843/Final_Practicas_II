import sys
import os
import shutil
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QFileDialog, QMessageBox, QDialog, QCheckBox, 
    QDialogButtonBox, QVBoxLayout
)
from database.conexion import Database
from error.logger import log
from datetime import datetime, date

class GenerosPeliculas(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleccionar Géneros")
        self.seleccionar_generos = []
        layout = QVBoxLayout()
        self.checkboxes = []

        try:
            database = Database()
            self.genres = [genre[1] for genre in database.obtener_generos()]
        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', 'No se pudo cargar la lista de géneros.')
            self.genres = []

        for genre in self.genres:
            checkbox = QCheckBox(genre)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def accept(self):
        self.seleccionar_generos = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        super().accept()


class ModificarPelicula(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        loadUi('ui/modificarPelicula.ui', self)

        self.db = Database()
        self.imagenes_dir = 'movies'
        self.imagen_seleccionada = None
        self.datos_originales = {}

        self.lineEdit_generos.setReadOnly(True)
        os.makedirs(self.imagenes_dir, exist_ok=True)

        self.cargar_peliculas_en_combo()

        fecha_actual = QtCore.QDate.currentDate()
        self.dateEdit_estreno_mundial.setDate(fecha_actual)
        self.dateEdit_fecha_inicio.setDate(fecha_actual)
        self.dateEdit_fecha_fin.setDate(fecha_actual)

        for date_edit in [self.dateEdit_estreno_mundial, 
                          self.dateEdit_fecha_inicio, 
                          self.dateEdit_fecha_fin]:
            date_edit.setCalendarPopup(True)

        self.btn_cancelar.clicked.connect(self.cancelar)
        self.btn_aceptar.clicked.connect(self.aceptar)
        self.btn_seleccionar_pelicula.clicked.connect(self.seleccionar_pelicula)
        self.btn_generos.clicked.connect(self.abrir_seleccion_generos)
        self.comboBox_peliculas.currentIndexChanged.connect(self.rellenar_datos_pelicula)

    def cargar_peliculas_en_combo(self):
        try:
            peliculas = self.db.obtener_peliculas()
            self.comboBox_peliculas.clear()
            self.comboBox_peliculas.addItem("Seleccionar Película", None)

            for pelicula in peliculas:
                self.comboBox_peliculas.addItem(pelicula[1], pelicula[0])
        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', 'No se pudo cargar la lista de películas.')

    def rellenar_datos_pelicula(self):
        id_pelicula = self.comboBox_peliculas.currentData()
        if not id_pelicula:
            return

        try:
            datos_pelicula = self.db.obtener_datos_pelicula(id_pelicula)
            if not datos_pelicula:
                return

            self.datos_originales = datos_pelicula  # Guardamos los datos originales

            self.nombre_pelicula.setText(datos_pelicula['nombre'])
            self.textEdit_Resumen.setPlainText(datos_pelicula['resumen'])
            self.lineEdit_pais_origen.setText(datos_pelicula['pais_origen'])

            self.dateEdit_estreno_mundial.setDate(self.convertir_fecha(datos_pelicula['fecha_estreno']))
            self.dateEdit_fecha_inicio.setDate(self.convertir_fecha(datos_pelicula['fecha_inicio']))
            self.dateEdit_fecha_fin.setDate(self.convertir_fecha(datos_pelicula['fecha_fin']))

            self.duracion.setValue(datos_pelicula.get('duracion', 60))
            self.clasificacion.setCurrentText(datos_pelicula['clasificacion'])

            generos = self.db.obtener_generos_pelicula(id_pelicula)
            self.lineEdit_generos.setText(", ".join(generos))

            self.cargar_imagen(datos_pelicula.get('imagen'))
        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', f'Error al cargar los datos de la película: {e}')

    def convertir_fecha(self, fecha):
        if isinstance(fecha, str):
            return QtCore.QDate.fromString(fecha, "yyyy-MM-dd")
        elif isinstance(fecha, (date, datetime)):
            return QtCore.QDate(fecha.year, fecha.month, fecha.day)
        return QtCore.QDate()

    def cargar_imagen(self, nombre_imagen):
        if not nombre_imagen:
            self.label_peli.clear()
            return

        ruta = os.path.join(self.imagenes_dir, nombre_imagen)
        if os.path.exists(ruta):
            pixmap = QtGui.QPixmap(ruta)
            self.label_peli.setPixmap(pixmap)
            self.label_peli.setScaledContents(True)
        else:
            QMessageBox.warning(self, 'Advertencia', f'No se encontró la imagen: {nombre_imagen}')

    def cancelar(self):
        self.close()

    def aceptar(self):
        #TODO
        try:
            # Validar que se haya seleccionado una película
            id_pelicula = self.comboBox_peliculas.currentData()
            print(f"ID de la película seleccionada: {id_pelicula}")  # Log para verificar el ID

            if not id_pelicula:
                QMessageBox.warning(self, 'Advertencia', 'Selecciona una película válida.')
                return

            # Recuperar los datos ingresados
            nombre = self.nombre_pelicula.text()
            resumen = self.textEdit_Resumen.toPlainText()
            pais = self.lineEdit_pais_origen.text()
            estreno = self.dateEdit_estreno_mundial.date().toString("yyyy-MM-dd")
            inicio = self.dateEdit_fecha_inicio.date().toString("yyyy-MM-dd")
            fin = self.dateEdit_fecha_fin.date().toString("yyyy-MM-dd")
            duracion = self.duracion.value()
            clasificacion = self.clasificacion.currentText()
            generos = self.lineEdit_generos.text().split(", ")

            # Validar que los campos obligatorios no estén vacíos y mostrar cuál está vacío
            if not nombre:
                QMessageBox.warning(self, 'Advertencia', 'El campo "Nombre de la película" está vacío.')
                return
            if not resumen:
                QMessageBox.warning(self, 'Advertencia', 'El campo "Resumen" está vacío.')
                return
            if not pais:
                QMessageBox.warning(self, 'Advertencia', 'El campo "País de origen" está vacío.')
                return
            if not generos or generos == ['']:
                QMessageBox.warning(self, 'Advertencia', 'Debe seleccionar al menos un género.')
                return
            if duracion <= 60:
                QMessageBox.warning(self, 'Advertencia', 'La duración debe ser mayor a 60 minutos.')
                return

            # Copiar imagen si se seleccionó una nueva
            if self.imagen_seleccionada:
                nombre_imagen = os.path.basename(self.imagen_seleccionada)
                nueva_ruta = os.path.join(self.imagenes_dir, nombre_imagen)
                shutil.copy2(self.imagen_seleccionada, nueva_ruta)
            else:
                nombre_imagen = self.datos_originales.get('imagen')
            
            # Modificar la película en la base de datos primero
            try:
                resultado = self.db.modificar_pelicula(id_pelicula, nombre, resumen, pais, estreno, duracion, clasificacion, nombre_imagen, inicio, fin)

                # Verificar que la modificación fue exitosa
                if not resultado:
                    raise Exception(f"No se encontró la película con Id {id_pelicula} o no se pudo modificar.")
                print(f"Película modificada exitosamente con ID: {id_pelicula}")
            
            except Exception as e:
                raise Exception(f"Ocurrió un error al modificar la película: {e}")
            
            # Si la película fue modificada correctamente, actualizar los géneros
            try:
                print(f"Actualizando géneros para la película con ID: {id_pelicula}")
                self.actualizar_generos(id_pelicula, generos)

            except Exception as e:
                raise Exception(f"Ocurrió un error al actualizar los géneros: {e}")

            # Mostrar mensaje de éxito si todo funcionó correctamente
            QMessageBox.information(self, 'Éxito', 'Película modificada y géneros actualizados exitosamente.')
            self.close()

        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', f'Ocurrió un error: {e}')



    def actualizar_generos(self, id_pelicula, generos):
        """Actualiza los géneros asociados a una película en la base de datos."""
        try:
            # Eliminar los géneros existentes para esa película
            self.db.eliminar_generos_pelicula(id_pelicula)

            # Insertar los nuevos géneros, si no están vacíos
            for genero in generos:
                if genero.strip():  # Validamos que el género no esté vacío
                    id_genero = self.db.obtener_id_genero(genero.strip())
                    if id_genero is not None:
                        self.db.insertar_generos(id_pelicula, id_genero)

        except Exception as e:
            log(e, "error")
            raise Exception(f'Ocurrió un error al actualizar los géneros: {e}')




    def seleccionar_pelicula(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp)")
        if archivo:
            self.imagen_seleccionada = archivo
            pixmap = QtGui.QPixmap(archivo)
            self.label_peli.setPixmap(pixmap)
            self.label_peli.setScaledContents(True)

    def abrir_seleccion_generos(self):
        dialog = GenerosPeliculas()
        if dialog.exec_():
            self.lineEdit_generos.setText(", ".join(dialog.seleccionar_generos))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ModificarPelicula()
    window.show()
    sys.exit(app.exec_())
