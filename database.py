import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_NAME = 'tasks.db' # Nombre del archivo de tu base de datos

# --- USUARIO POR DEFECTO ---
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD_HASH = "pbkdf2:sha256:260000$xxxxxxxx$yyyyyyyyyy"

def get_db_connection():
    """
    Establece y devuelve una conexión a la base de datos SQLite.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn

def init_db():
    """
    Inicializa la base de datos, creando la tabla 'users' si no existe.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );
    ''')
    conn.commit()
    # conn.close()
    print(f"Base de datos '{DATABASE_NAME}' inicializada (tabla 'users' verificada/creada).")


    cursor.execute("SELECT id FROM users WHERE username = ?", (DEFAULT_ADMIN_USERNAME,))
    existing_admin = cursor.fetchone()

    if existing_admin is None:
        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                            (DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD_HASH))
            conn.commit()
            print(f"Usuario por defecto '{DEFAULT_ADMIN_USERNAME}' insertado exitosamente.")
        except sqlite3.IntegrityError:
            # Esto puede ocurrir si hay una condición de carrera muy rara,
            # pero el SELECT anterior debería prevenirlo.
            print(f"Usuario por defecto '{DEFAULT_ADMIN_USERNAME}' ya existía (manejo de concurrencia).")
    else:
        print(f"Usuario por defecto '{DEFAULT_ADMIN_USERNAME}' ya existe en la base de datos. No se insertó.")

    conn.close()
    print(f"Base de datos '{DATABASE_NAME}' inicializada (tabla 'users' verificada/creada).")


def find_user_by_username(username):
    """
    Busca un usuario por su nombre de usuario.
    Retorna un diccionario con los datos del usuario o None si no lo encuentra.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return user

def add_user(username, password_hash):
    """
    Añade un nuevo usuario a la base de datos.
    Retorna el ID del nuevo usuario o None si el usuario ya existe.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        # Esto ocurre si el username no es UNIQUE (ya existe)
        return None
    finally:
        conn.close()

# Si quieres que la base de datos se inicialice al ejecutar server.py,
# puedes llamarla en el propio server.py o aquí si este archivo se importa
# y la llamas al inicio de tu aplicación Flask.
# Por ejemplo, puedes añadir un chequeo para ver si ya se inicializó.
# if not os.path.exists(DATABASE_NAME):
#     init_db()