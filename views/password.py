
import bcrypt

def generar_password(password):
    """Genera un hash para la contraseña usando bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verifica_password(password, generar_password):
    """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
    return bcrypt.checkpw(password.encode('utf-8'), generar_password.encode('utf-8'))


a=generar_password(123)
print(a)