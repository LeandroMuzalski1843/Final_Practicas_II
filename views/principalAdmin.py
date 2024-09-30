import os
import sys
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizeGrip,QMessageBox,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from views.agregarUsuario import AgregarUsuario
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from views.session import UserSession
from database.conexion import Database
from error.logger import log
from views.eliminarUsuario import EliminarUsuario

class MainWindow(QMainWindow):   
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # Cargar el archivo .ui que contiene la interfaz gráfica
        loadUi("ui\\menu.ui", self)
        
        # Diccionario de descripciones de películas
        self.descripciones_peliculas = {
            0: "Descripcion",
            1: "Descripción: Después de más de treinta años de servicio como uno de los mejores aviadores de la Marina, Pete ''Maverick'' Mitchell (Tom Cruise) está donde pertenece, superando los límites como un valiente piloto de pruebas y esquivando el avance de rango que lo dejaría en tierra..",
            2: "Descripción:'Interstellar' narra la historia de Joseph Cooper, un granjero que trabajó como astronauta de la NASA, quien debe volver a colocarse su traje de viajero espacial para ir en un viaje casi sin retorno con el fin de salvar a la humanidad de la degradación ambiental que aqueja a la tierra",
            3: "AVENGERS: ENDGAME está ambientada después de los catastróficos sucesos de Avengers: Infinity War, en los que Thanos eliminó deliberadamente a la mitad del universo al usar las gemas del infinito. Los que no se fueron, están desesperados por hacer algo (lo que sea) para traer de vuelta a sus seres queridos."
        }

        
        # Eliminar la barra de título de la ventana y ajustar la opacidad
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.setWindowOpacity(1.0)  # Opacidad completa (1.0 es totalmente opaco)

        # SizeGrip para redimensionar la ventana desde la esquina inferior derecha
        self.gripSize = 10  # Tamaño del QSizeGrip
        self.grip = QSizeGrip(self)  # Crear el QSizeGrip
        self.grip.resize(self.gripSize, self.gripSize)  # Ajustar el tamaño del grip

        # Ocultar el menú lateral al inicio (iniciar con width=0)
        self.frame_lateral.setMinimumWidth(0)

        # Iniciar en la primera página (self.page)
        self.stackedWidget.setCurrentWidget(self.page)

        # Asignar el evento de mover la ventana al arrastrar el frame superior
        self.frame_superior.mouseMoveEvent = self.mover_ventana  
        
        # Configurar los botones para cambiar de páginas dentro de un stackedWidget
        self.bt_inicio.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page))			
        self.bt_uno.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_uno))
        self.bt_dos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_dos))	
        self.bt_tres.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_tres))
        self.bt_cuatro.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cuatro))			
        self.bt_cinco.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.page_cinco))	


        #Saludo de bienvenida
        session = UserSession()
        saludo = session.username if session.username else "Usuario"  # Valor por defecto "Usuario"

        # Acortar el nombre si es demasiado largo (máximo 10 caracteres)
        max_length = 10
        if len(saludo) > max_length:
            saludo = saludo[:max_length] + "..."  # Truncar el nombre y agregar "..."

        # Actualizar el QLabel con el saludo
        self.label_bienvenida.setText(f"Hola, {saludo}!")



        #Configuracion botones pagina Usuarios
        self.bt_agregar_usuario.clicked.connect(self.abrir_agregar_usuario)
        self.btn_eliminar_usuario.clicked.connect(self.abrir_eliminar_usuarios)

        # Control de los botones de la barra de títulos (minimizar, maximizar/restaurar, cerrar)
        self.bt_minimizar.clicked.connect(self.control_bt_minimizar)		
        self.bt_restaurar.clicked.connect(self.control_bt_normal)
        self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
        self.bt_cerrar.clicked.connect(lambda: self.close())

        # Ocultar el botón de restaurar por defecto, ya que no está maximizada
        self.bt_restaurar.hide()

        # Asignar el evento al botón del menú lateral para animarlo
        self.bt_menu.clicked.connect(self.mover_menu)
        


        #Imagen en la cartelera y selección de película
        self.comboBox_cartelera.currentIndexChanged.connect(self.display_image)
        self.comboBox_cartelera.currentIndexChanged.connect(self.cambiar_pelicula)
        self.comboBox_cartelera.setCurrentIndex(0)
        self.display_image(0)
        # Actualizar descripción
        self.comboBox_cartelera.currentIndexChanged.connect(lambda: self.actualizar_descripcion(self.comboBox_cartelera.currentIndex()))  
        
        # Llenar tabla de usuarios al iniciar
        self.cargar_usuarios_en_tabla()
        # Conectar el botón de actualizar con el método cargar_usuarios_en_tabla
        self.btn_actualizarUsuario.clicked.connect(self.cargar_usuarios_en_tabla)



#==============================================================================================================
    #Comprar pelis

    #Cambiar imagen
    def cambiar_pelicula(self):
        """Cambia la película seleccionada en la cartelera."""
        pelicula_actual = self.comboBox_cartelera.currentText()
        print(f"Cambiando a película: {pelicula_actual}")
        # Aquí puedes agregar la lógica para actualizar la interfaz o realizar las acciones necesarias

    def display_image(self, index):
        images = {
            0: os.path.join(os.getcwd(), "img", "download.jpg"),
            1: os.path.join(os.getcwd(), "img", "descarga (1).jpeg"),
            2: os.path.join(os.getcwd(), "img", "descarga (2).jpeg"),
            3: os.path.join(os.getcwd(), "img", "descarga.jpeg")
        }

        image_path = images.get(index, "")
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():  # Verificar que la imagen se cargó correctamente
                # Ajustar la imagen para que ocupe el 100% del QLabel (sin mantener la relación de aspecto)
                self.label_imagenCartelera.setPixmap(pixmap.scaled(
                    self.label_imagenCartelera.size(),  # Tamaño del QLabel
                    Qt.IgnoreAspectRatio,  # Ignorar la relación de aspecto para llenar el QLabel
                    Qt.SmoothTransformation  # Transformación suave para una mejor calidad
                ))
                self.label_imagenCartelera.setAlignment(Qt.AlignCenter)  # Centrar la imagen en el label
            else:
                self.label_imagenCartelera.clear()
                self.label_imagenCartelera.setText("Error: No se pudo cargar la imagen.")
        else:
            self.label_imagenCartelera.clear()
            self.label_imagenCartelera.setText("No hay imagen seleccionada.")
    
    def actualizar_descripcion(self, index):
        descripcion = self.descripciones_peliculas.get(index, "Descripción no disponible.")
        self.textBrowser_descripcion.setText(descripcion)
    
    #==============================================================================================================
    # Configuracion Pagina Usuario

    def abrir_agregar_usuario(self):
        self.agregar_usuario = AgregarUsuario()
        self.agregar_usuario.show()
    
    def abrir_eliminar_usuarios(self):
        self.eliminar_usuario = EliminarUsuario()
        self.eliminar_usuario.show()

    #==============================================================================================================
    # Configuracion Pagina Usuarios
    
    def cargar_usuarios_en_tabla(self):
        """Carga los usuarios de la base de datos y los muestra en tableWidget_usuarios."""
        database = Database()
        try:
            usuarios = database.obtener_usuarios()
            self.tableWidget_usuarios.setRowCount(0)
            for row_number, row_data in enumerate(usuarios):
                self.tableWidget_usuarios.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_usuarios.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            log(e, "error")
            QMessageBox.critical(self, 'Error', 'No se pudo cargar la tabla de usuarios.')
        


    #==============================================================================================================
    #                         Configuracion - [] X

    # Método para minimizar la ventana
    def control_bt_minimizar(self):
        self.showMinimized()		

    # Método para restaurar la ventana a tamaño normal (si estaba maximizada)
    def control_bt_normal(self): 
        self.showNormal()		
        self.bt_restaurar.hide()  # Ocultar botón restaurar
        self.bt_maximizar.show()  # Mostrar botón maximizar

    # Método para maximizar la ventana
    def control_bt_maximizar(self): 
        self.showMaximized()
        self.bt_maximizar.hide()  # Ocultar botón maximizar
        self.bt_restaurar.show()  # Mostrar botón restaurar

    # Método para mover el menú lateral con una animación
    def mover_menu(self):
        width = self.frame_lateral.width()  # Obtener el ancho actual del menú lateral
        normal = 0  # Ancho mínimo del menú cuando está colapsado
        extender = 200 if width == 0 else normal  # Extender a 200 si está colapsado, si no, reducir a 0
        
        # Animación para cambiar el tamaño del menú lateral
        self.animacion = QPropertyAnimation(self.frame_lateral, b'minimumWidth')
        self.animacion.setDuration(300)  # Duración de la animación en milisegundos
        self.animacion.setStartValue(width)  # Valor inicial (ancho actual)
        self.animacion.setEndValue(extender)  # Valor final (colapsado o extendido)
        self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)  # Tipo de animación

        self.animacion.start()  # Iniciar la animación

    
    ## SizeGrip: Reposicionar el grip cuando la ventana se redimensiona
    def resizeEvent(self, event):
        rect = self.rect()  # Obtener el rectángulo actual de la ventana
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)  # Mover el grip a la esquina inferior derecha
    
    ## Mover la ventana al hacer clic en la parte superior y arrastrar
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()  # Capturar la posición del cursor al hacer clic

    def mover_ventana(self, event):
        if not self.isMaximized():  # Solo permitir mover la ventana si no está maximizada
            if event.buttons() == Qt.LeftButton:  # Si se arrastra con el botón izquierdo
                self.move(self.pos() + event.globalPos() - self.clickPosition)  # Mover la ventana
                self.clickPosition = event.globalPos()  # Actualizar la posición del cursor
                event.accept()  # Aceptar el evento

        # Si se arrastra hacia la parte superior de la pantalla, maximizar la ventana
        if event.globalPos().y() <= 20:  
            self.showMaximized()
        else:
            self.showNormal()

    

def main():
    app = QApplication(sys.argv)  
    ventana = MainWindow()  
    ventana.show()  
    sys.exit(app.exec_())  

if __name__ == "__main__":
    main()

    
