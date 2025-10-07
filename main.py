import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Esquemas de datos
class EsquemaAcceso(BaseModel):
    usuario: str
    contrasena: str

class EsquemaCreacionUsuario(BaseModel):
    nombre: str
    contrasena: str
    email: str
    activo: bool = True

class EsquemaActualizacionUsuario(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[bool] = None

# CAMBIO: Usamos 'app' como nombre de la aplicación
app = FastAPI()

# Base de datos en memoria
USUARIOS = [
    {"id": 1, "nombre": "admin", "contrasena": "abc", "email": "admin@cipherwall.com", "activo": True},
    {"id": 2, "nombre": "user1", "contrasena": "secret", "email": "user1@lab.com", "activo": True},
]
siguiente_id = 3

# Función auxiliar para encontrar usuario
def encontrar_usuario(user_id: int):
    for u in USUARIOS:
        if u["id"] == user_id:
            return u
    return None

# --- Endpoints Generales ---

@app.get("/")
def inicio():
    return {"mensaje": "Bienvenido al Laboratorio de Seguridad"}

# --- Endpoints de Login (Para el ataque de fuerza bruta) ---

@app.post("/login")
def iniciar_sesion(peticion: EsquemaAcceso):
    print(f"Intento de Acceso: Usuario='{peticion.usuario}', Contraseña='{peticion.contrasena}'")

    for u in USUARIOS:
        if u["nombre"] == peticion.usuario and u["contrasena"] == peticion.contrasena:
            if not u["activo"]:
                raise HTTPException(status_code=401, detail="Cuenta inactiva")
            
            return {"message": f"login successful", "user": u["nombre"]} 
            
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

# --- Endpoints de Usuarios (CRUD) ---

@app.post("/users")
def crear_usuario(peticion: EsquemaCreacionUsuario):
    global siguiente_id
    
    for u in USUARIOS:
        if u["nombre"] == peticion.nombre:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
            
    nuevo_usuario = {
        "id": siguiente_id, 
        "nombre": peticion.nombre, 
        "contrasena": peticion.contrasena, 
        "email": peticion.email, 
        "activo": peticion.activo
    }
    USUARIOS.append(nuevo_usuario)
    siguiente_id += 1
    return {"mensaje": "Usuario creado", "usuario": nuevo_usuario}

@app.get("/users")
def listar_usuarios():
    # Devuelve solo datos sin la contraseña para simular un listado seguro
    lista_limpia = [{"id": u["id"], "nombre": u["nombre"], "email": u["email"], "activo": u["activo"]} for u in USUARIOS]
    return lista_limpia

@app.get("/users/{user_id}")
def obtener_usuario(user_id: int):
    usuario = encontrar_usuario(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    # Devuelve solo datos sin la contraseña
    return {"id": usuario["id"], "nombre": usuario["nombre"], "email": usuario["email"], "activo": usuario["activo"]}

@app.put("/users/{user_id}")
def actualizar_usuario(user_id: int, peticion: EsquemaActualizacionUsuario):
    usuario = encontrar_usuario(user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if peticion.nombre is not None:
        usuario["nombre"] = peticion.nombre
    if peticion.email is not None:
        usuario["email"] = peticion.email
    if peticion.activo is not None:
        usuario["activo"] = peticion.activo
        
    # Devuelve solo datos sin la contraseña
    return {"mensaje": "Usuario actualizado", "usuario": {"id": usuario["id"], "nombre": usuario["nombre"], "email": usuario["email"], "activo": usuario["activo"]}}

@app.delete("/users/{user_id}")
def eliminar_usuario(user_id: int):
    global USUARIOS
    usuario_a_eliminar = encontrar_usuario(user_id)
    
    if not usuario_a_eliminar:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    USUARIOS = [u for u in USUARIOS if u["id"] != user_id]
    
    return {"mensaje": f"Usuario {user_id} eliminado"}

if __name__ == "__main__":
    # CAMBIO: La cadena de ejecución ahora usa 'app'
    uvicorn.run("api_servidor:app", host="127.0.0.1", port=8000, reload=True)
