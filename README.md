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

