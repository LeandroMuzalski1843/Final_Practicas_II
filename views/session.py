class UserSession:
    _instance = None  # Variable de clase para almacenar la única instancia de la clase (Singleton).

    def __new__(cls):
        # Si no se ha creado una instancia, se crea una nueva.
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)  # Llama al método __new__ de la superclase para crear la instancia.
            # Inicializa los atributos
            cls._instance.username = None   
            cls._instance.grupo = None  
        return cls._instance  

    def set_user(self, username, grupo):
        # Método para establecer el nombre de usuario y correo electrónico en la sesión.
        self.username = username  
        self.grupo = grupo

    def clear_user(self):
        # Método para limpiar los datos del usuario, simulando un cierre de sesión.
        self.username = None  
        self.grupo = None  

    def is_logged_in(self):
        # Método para verificar si un usuario está logueado.
        return self.username is not None  # Retorna True si 'username' no es None (usuario logueado), de lo contrario False.


