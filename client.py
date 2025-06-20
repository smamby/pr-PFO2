# client.py
import requests

BASE_URL = "http://127.0.0.1:5000"

def obtener_bienvenida():
    try:
        response = requests.get(f"{BASE_URL}/tareas")
        response.raise_for_status()
        print("\n--- Contenido de la Página de Bienvenida ---")
        print(response.text)
        print("------------------------------------------")
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la bienvenida: {e}")

def registrar_usuario(usuario, password):
    try:
        response = requests.post(f"{BASE_URL}/registro", json={"usuario": usuario, "password": password})
        response.raise_for_status()
        print(f"\nRespuesta registro: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error al registrar usuario: {e}")

def iniciar_sesion(usuario, password):
    try:
        response = requests.post(f"{BASE_URL}/login", json={"usuario": usuario, "password": password})
        response.raise_for_status()
        print(f"\nRespuesta login: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error al iniciar sesión: {e}")

if __name__ == '__main__':
    # Ejemplo de uso:
    print("--- Probando el Cliente de Consola ---")
    print("")
    
    # 1. Registrar un usuario
    print("1. Registrar un usuario")
    registrar_usuario("testuser2", "password123")
    print("")
    print("-------------------------------------------------------------")
    
    # 2. Intentar registrar el mismo usuario (debería dar error)
    print("2. Intentar registrar el mismo usuario (debería dar error)")
    registrar_usuario("testuser2", "password123")
    print("")
    print("-------------------------------------------------------------")

    # 3. Iniciar sesión con el usuario
    print("3. Iniciar sesión con el usuario")
    iniciar_sesion("testuser2", "password123")
    print("")
    print("-------------------------------------------------------------")
    
    # 4. Iniciar sesión con credenciales incorrectas
    print("4. Iniciar sesión con credenciales incorrectas")
    iniciar_sesion("testuser2", "wrongpassword")
    print("")
    print("-------------------------------------------------------------")
    
    # 5. Obtener la página de bienvenida
    print("5. Obtener la página de bienvenida")
    obtener_bienvenida()