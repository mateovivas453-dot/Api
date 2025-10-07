# Mi Proyecto: CipherWall — Demostración de Fuerza Bruta (Parcial 1)

Este repositorio contiene una implementación didáctica destinada a la evaluación del primer parcial. He desarrollado una API REST básica empleando **FastAPI** con almacenamiento de usuarios en memoria (sin persistencia en base de datos). El propósito principal del proyecto es demostrar de forma práctica un **ataque de fuerza bruta optimizado** dirigido al endpoint de autenticación (`/login`) y analizar las implicaciones de seguridad asociadas.

## Objetivo y alcance

El objetivo de este trabajo es reproducir y exponer, en un entorno controlado, la vulnerabilidad que permite la enumeración de contraseñas por fuerza bruta. Para facilitar la demostración, la contraseña del usuario `admin` está deliberadamente fijada como `abc`, de modo que el ataque puede completarse en segundos y evidenciar la necesidad de contramedidas como límites de tasa y mecanismos de defensa adicionales.

## Tecnologías utilizadas

* **FastAPI:** Framework principal para la implementación de la API, elegido por su rendimiento y capacidad de generar documentación automática.
* **Uvicorn:** Servidor ASGI recomendado para ejecutar aplicaciones FastAPI en entornos de desarrollo y pruebas.
* **Pydantic:** Biblioteca para la validación y modelado de datos en las peticiones y respuestas.
* **requests (Python):** Biblioteca empleada por el script atacante para realizar peticiones HTTP.
* **itertools (Python):** Utilizada por el script atacante para generar de forma exhaustiva las combinaciones de contraseñas.

## Despliegue y ejecución

Para ejecutar el proyecto se requieren dos terminales simultáneas: una para iniciar el servidor y otra para correr el script que realiza el ataque de fuerza bruta.

### Requisitos

Asegúrese de contar con un entorno virtual de Python activado e instale las dependencias necesarias:

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux / macOS
# source venv/bin/activate

pip install fastapi uvicorn[standard] requests
```

### Iniciar el servidor (Terminal 1)

En la primera terminal, inicie la API. El ejemplo parte del supuesto de que el archivo principal se llama `main.py`:

```bash
uvicorn main:app --reload
```

La API quedará escuchando en `http://127.0.0.1:8000`.

### Ejecutar el script de ataque (Terminal 2)

En la segunda terminal, active el mismo entorno virtual y ejecute el script optimizado de fuerza bruta (por ejemplo `brute_force_optimized.py`). Para esta demostración deben aplicarse las siguientes configuraciones en el script:

* `USERNAME = "admin"`
* `MAX_LENGTH = 3`

Ejemplo de ejecución:

```bash
# Asegúrese de tener el entorno activo en esta terminal también
.\venv\Scripts\activate

python brute_force_optimized.py
```

El script recorrerá las combinaciones de contraseñas hasta encontrar `abc` en el diccionario de usuarios en memoria, evidenciando la vulnerabilidad.

## Consideraciones de seguridad y optimizaciones del ataque

La implementación y el script incluyen decisiones conscientes que permiten realizar la prueba sin provocar la caída inmediata del servidor de pruebas:

1. **Ausencia de limitación de tasa:** La API está deliberadamente expuesta sin mecanismos de rate limiting en el endpoint `/login`, lo que posibilita un número ilimitado de intentos por unidad de tiempo y facilita la ejecución de ataques de fuerza bruta.

2. **Reutilización de conexión HTTP:** El script atacante emplea `requests.Session()` para reutilizar la misma conexión HTTP durante múltiples intentos, reduciendo la sobrecarga asociada a la creación y cierre repetido de conexiones.

3. **Pausa entre intentos:** Se incorpora un retraso mínimo (`time.sleep(0.001)`) entre solicitudes para mitigar la saturación inmediata del hilo principal del servidor y permitir que la demostración se ejecute de forma estable en el entorno local.

4. **Manejo de errores de validación:** El script contempla el código de respuesta **422 Unprocessable Entity**, gestionándolo como una respuesta esperada derivada de las validaciones de Pydantic y no como un fallo crítico del servidor.

## Limitaciones y recomendaciones

La presente implementación tiene fines demostrativos y no debe utilizarse en entornos de producción. Para mitigar la vulnerabilidad mostrada en este ejercicio, recomiendo las siguientes medidas:

* Implementar **limitación de tasa** (rate limiting) por IP y por cuenta de usuario.
* Incorporar mecanismos de bloqueo temporal tras múltiples intentos fallidos (account lockout) y notificaciones de seguridad.
* Exigir contraseñas con complejidad mínima y utilizar políticas de gestión de contraseñas (longitud mínima, uso de caracteres diversos).
* Emplear autenticación multifactor (MFA) para las cuentas con privilegios elevados.
* Registrar y monitorizar intentos de acceso para detectar patrones de ataque y activar respuestas automáticas.

## Conclusión

Este proyecto tiene carácter pedagógico: permite reproducir en un entorno controlado un ataque de fuerza bruta y comprender las medidas de mitigación necesarias. La configuración deliberada —contraseña débil y ausencia de límites de tasa— facilita la observación práctica del riesgo y sirve como base para discutir y aplicar mejoras de seguridad en implementaciones reales.

---

Si lo desea, puedo generar una versión más breve para la portada del repositorio, añadir un archivo `LICENSE` sugerido, o proponer cambios de código para integrar rate limiting y bloqueo de cuentas.

Bloque 1: Importaciones y Modelos de Datos (Pydantic)
Esta sección trae las herramientas necesarias y define la estructura de los datos que la API envía y recibe.

Código	Explicación
import uvicorn	Necesario para ejecutar el servidor con uvicorn.run() al final del archivo.
from fastapi import FastAPI, HTTPException	Importa el framework principal (FastAPI) y la herramienta para manejar errores HTTP (HTTPException).
from pydantic import BaseModel	La clase base para definir la estructura de los datos (esquemas de la API).
from typing import Optional	Permite especificar que un campo es opcional (puede ser None).
class EsquemaAcceso(...)	Define el esquema para el endpoint /login. Solo requiere el usuario y la contrasena. Esto es lo que el script de ataque envía.
class EsquemaCreacionUsuario(...)	Define el esquema para crear un nuevo usuario (POST /users).
class EsquemaActualizacionUsuario(...)	Define el esquema para actualizar un usuario (PUT /users/{id}). Todos los campos son Optional porque no tienes que enviar todos para actualizar.
app = FastAPI()	Inicialización de la Aplicación. Crea la instancia de la aplicación FastAPI. Esta instancia, llamada app, es la que Uvicorn busca para iniciar el servidor (main:app).

Exportar a Hojas de cálculo
Bloque 2: Base de Datos en Memoria y Lógica Central
Esta es tu "base de datos" temporal. Los datos se pierden cada vez que reinicias el servidor.

Código	Explicación
USUARIOS = [...]	La lista de Python que actúa como tu base de datos. Contiene diccionarios con la información de los usuarios. El usuario admin con contraseña abc es la víctima del ataque.
siguiente_id = 3	Una variable global que lleva la cuenta para asignar un id único a cada nuevo usuario.
def encontrar_usuario(user_id: int):	Función auxiliar que busca un usuario dentro de la lista USUARIOS por su ID y lo devuelve. Es esencial para los endpoints de GET, PUT y DELETE.

Exportar a Hojas de cálculo
Bloque 3: Endpoint de Raíz y CRUD (Crear, Leer, Actualizar, Eliminar)
Aquí se definen las rutas de tu API.

Endpoint y Función	Explicación
@app.get("/")	El endpoint inicial. Devuelve un mensaje de bienvenida.
@app.post("/users")	Crear Usuario (C): Toma un EsquemaCreacionUsuario. Verifica si el nombre de usuario ya existe. Si no, crea un nuevo diccionario, le asigna el siguiente_id global, lo añade a la lista USUARIOS y actualiza el contador.
@app.get("/users")	Listar Usuarios (R): Devuelve la lista completa de usuarios, pero filtra la contraseña para no exponerla al listado público.
@app.get("/users/{user_id}")	Obtener Usuario por ID (R): Usa encontrar_usuario(). Si no lo encuentra, lanza un HTTPException 404 (No Encontrado). Filtra la contraseña antes de devolver el resultado.
@app.put("/users/{user_id}")	Actualizar Usuario (U): Usa encontrar_usuario(). Recibe un EsquemaActualizacionUsuario y actualiza solo los campos proporcionados (nombre, email, activo).
@app.delete("/users/{user_id}")	Eliminar Usuario (D): Usa encontrar_usuario(). Reemplaza la lista USUARIOS con una nueva lista que excluye al usuario con ese id.

Exportar a Hojas de cálculo
Bloque 4: Endpoint de Login (El Objetivo del Ataque)
Este es el bloque que el script de fuerza bruta bombardea.

Código	Explicación
@app.post("/login")	Define el endpoint /login. Recibe las credenciales en el modelo EsquemaAcceso.
print(f"Intento de Acceso: ...")	Muestra en la terminal del servidor cada intento. Durante el ataque, esto satura la terminal.
for u in USUARIOS:	Itera sobre cada usuario en la lista.
if u["nombre"] == peticion.usuario and u["contrasena"] == peticion.contrasena:	Verificación de Credenciales: La condición que el atacante intenta satisfacer. Si el nombre y la contraseña coinciden, el ataque ha tenido éxito.
return {"message": "login successful", ...}	Respuesta de Éxito (HTTP 200): Se envía si las credenciales son correctas. El script de ataque busca este mensaje.
raise HTTPException(status_code=401, detail="Credenciales incorrectas")	Respuesta de Fallo (HTTP 401): Se lanza si no se encontró ninguna coincidencia en la lista. El script de ataque espera esta respuesta y continúa probando.

Exportar a Hojas de cálculo
Bloque 5: Ejecución del Servidor
Este bloque permite ejecutar tu archivo Python directamente.

Código	Explicación
if __name__ == "__main__":	Estándar de Python: Solo ejecuta el código dentro si el archivo se ejecuta directamente (no si se importa).
uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)	Ejecución Final: Llama a la función run de Uvicorn. Le indica que: 1) Busque la instancia app en el módulo main.py. 2) Escuche en la dirección 127.0.0.1:8000. 3) Se reinicie automáticamente (reload=True) si detecta cambios en el código.

Exportar a Hojas de cálculo







