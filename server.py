# server.py
from flask import Flask, render_template, request, jsonify # Añadimos request y jsonify por si las necesitas luego
from werkzeug.security import generate_password_hash, check_password_hash # Para hashear passwords
from database import init_db, add_user, find_user_by_username # Importamos las funciones de database.py

app = Flask(__name__)

# --- Inicializar la base de datos al inicio de la aplicación ---
# Esto asegura que la tabla 'users' se cree si no existe.
# Es importante que esto se ejecute en el contexto de la aplicación.
with app.app_context():
    init_db()

# --- Rutas de la API ---

# 1. Registro de Usuarios
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"mensaje": "Usuario y password son requeridos"}), 400

    hashed_password = generate_password_hash(password)

    # Usamos la función de database.py
    user_id = add_user(usuario, hashed_password)

    if user_id is None:
        return jsonify({"mensaje": "El nombre de usuario ya existe"}), 409 # Conflict
    
    return jsonify({"mensaje": "Usuario registrado exitosamente", "id": user_id}), 201

# 2. Inicio de Sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('password')

    if not usuario or not password:
        return jsonify({"mensaje": "Usuario y password son requeridos"}), 400

    # Usamos la función de database.py
    user = find_user_by_username(usuario)

    # user es un objeto Row de sqlite3.Row, accedemos como diccionario
    if user and check_password_hash(user['password_hash'], password):
        return render_template('bienvenida.html')
        # return jsonify({"mensaje": "Inicio de sesion exitoso"}), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401 # Unauthorized

# 3. Gestión de Tareas (HTML de bienvenida)
@app.route('/tareas', methods=['GET'])
def mostrar_bienvenida():
    # Asegúrate de que tienes una carpeta 'templates' en el mismo directorio que server.py
    # y dentro de ella el archivo 'bienvenida.html'.
    return render_template('bienvenida.html')

# --- INICIO DEL SERVIDOR ---
# Esto es CRUCIAL. Cuando ejecutas 'python server.py', este bloque se ejecuta.
if __name__ == '__main__':
    # debug=True es útil durante el desarrollo para ver errores y recargar automáticamente.
    # En producción, se debería usar un servidor WSGI como Gunicorn o Waitress.
    app.run(debug=True)