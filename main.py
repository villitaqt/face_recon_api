# main.py
# -------
# Este es el archivo principal de nuestra API. Aquí definimos la aplicación
# FastAPI y crearemos todos los endpoints (rutas) que nuestra app móvil
# consumirá.

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import uuid
import os
import tempfile
import json
from datetime import datetime
import shutil

# Importaciones locales
from database import get_db, User, create_db_tables
from face_embedding_extractor import extraer_embedding_pca
from facial_preprocesador import preprocesar_cara

# --- 1. Creación de la Instancia de la Aplicación ---
app = FastAPI(
    title="API de Reconocimiento Facial",
    description="API para gestionar usuarios y realizar reconocimiento facial con sistema de alertas.",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración del sistema desde variables de entorno
RECOGNITION_THRESHOLD = float(os.getenv("FACE_RECOGNITION_THRESHOLD", "4000"))
ALERT_ENABLED = os.getenv("ALERT_ENABLED", "true").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/facerecon")

# Asegurar que el directorio de fotos existe
FOTOS_DIR = "static/fotos_perfil"
os.makedirs(FOTOS_DIR, exist_ok=True)

# --- 2. Endpoint Raíz ---
@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint de bienvenida. Devuelve un mensaje JSON para confirmar
    que la API está funcionando correctamente.
    """
    return {
        "API": "Sistema de Reconocimiento Facial", 
        "Version": "2.0",
        "Features": ["User Management", "Face Recognition", "Alert System", "Continuous Learning"]
    }

# --- 3. Endpoints de Usuarios ---

@app.post("/usuarios/", tags=["Users"])
async def create_user(
    nombre: str = Form(...),
    apellido: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    requisitoriado: bool = Form(False),
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo usuario con su imagen facial, email y teléfono.
    """
    # Validar tipo de archivo
    if not foto.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    # Verificar si el email ya existe
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya existe")
    
    # Guardar imagen temporalmente para procesamiento
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        content = await foto.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Extraer embedding del rostro
        embedding = extraer_embedding_pca(tmp_file_path)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No se pudo detectar un rostro en la imagen")
        
        # Crear usuario en la base de datos primero para obtener el ID
        user = User(
            name=f"{nombre} {apellido}",
            email=email,
            telefono=telefono,
            requested=requisitoriado,
            embedding=embedding.tolist()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Generar nombre de archivo usando el ID del usuario
        foto_filename = f"{user.id}.jpg"
        foto_path = os.path.join(FOTOS_DIR, foto_filename)
        
        # Guardar la imagen en el directorio estático
        shutil.copy2(tmp_file_path, foto_path)
        
        return {
            "id": str(user.id), 
            "nombre": nombre,
            "apellido": apellido,
            "email": user.email,
            "telefono": user.telefono,
            "requisitoriado": user.requested,
            "url_foto": f"/static/fotos_perfil/{foto_filename}",
            "message": "Usuario creado exitosamente"
        }
    
    finally:
        # Limpiar archivo temporal
        os.unlink(tmp_file_path)

@app.get("/usuarios/", tags=["Users"])
def get_users(
    requisitoriado_solo: bool = False,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de todos los usuarios o solo los marcados como "requisitoriado".
    """
    query = db.query(User)
    if requisitoriado_solo:
        query = query.filter(User.requested == True)
    
    users = query.all()
    return [
        {
            "id": str(user.id), 
            "nombre": user.name.split()[0] if user.name else "",
            "apellido": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
            "email": user.email,
            "telefono": user.telefono,
            "requisitoriado": user.requested,
            "url_foto": f"/static/fotos_perfil/{user.id}.jpg",
            "created_at": user.created_at.isoformat() if user.created_at else None
        } 
        for user in users
    ]

@app.get("/usuarios/{user_id}", tags=["Users"])
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    Obtener un usuario específico por ID.
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    
    user = db.query(User).filter(User.id == user_uuid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return {
        "id": str(user.id), 
        "nombre": user.name.split()[0] if user.name else "",
        "apellido": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
        "email": user.email,
        "telefono": user.telefono,
        "requisitoriado": user.requested,
        "url_foto": f"/static/fotos_perfil/{user.id}.jpg",
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None
    }

@app.put("/usuarios/{user_id}", tags=["Users"])
async def update_user(
    user_id: str,
    nombre: Optional[str] = Form(None),
    apellido: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    requisitoriado: Optional[bool] = Form(None),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    """
    Actualizar un usuario existente.
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    
    user = db.query(User).filter(User.id == user_uuid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos básicos
    if nombre is not None and apellido is not None:
        user.name = f"{nombre} {apellido}"
    elif nombre is not None:
        current_name = user.name.split() if user.name else []
        user.name = f"{nombre} {' '.join(current_name[1:]) if len(current_name) > 1 else ''}"
    elif apellido is not None:
        current_name = user.name.split() if user.name else []
        user.name = f"{current_name[0] if current_name else ''} {apellido}"
    
    if email is not None:
        # Verificar si el email ya existe en otro usuario
        existing_user = db.query(User).filter(
            User.email == email, 
            User.id != user_uuid
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El email ya existe")
        user.email = email
    
    if telefono is not None:
        user.telefono = telefono
    
    if requisitoriado is not None:
        user.requested = requisitoriado
    
    # Actualizar embedding si se proporciona nueva imagen
    if foto is not None:
        if not foto.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            content = await foto.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        
        try:
            # Extraer embedding del rostro
            embedding = extraer_embedding_pca(tmp_file_path)
            if embedding is None:
                raise HTTPException(status_code=400, detail="No se pudo detectar un rostro en la imagen")
            
            # Actualizar embedding
            user.embedding = embedding.tolist()
            
            # Actualizar imagen si es necesario
            file_extension = os.path.splitext(foto.filename)[1]
            new_foto_path = os.path.join(FOTOS_DIR, f"{user.id}{file_extension}")
            shutil.copy2(tmp_file_path, new_foto_path)
            
        finally:
            os.unlink(tmp_file_path)
    
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return {
        "id": str(user.id),
        "nombre": user.name.split()[0] if user.name else "",
        "apellido": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
        "email": user.email,
        "telefono": user.telefono,
        "requisitoriado": user.requested,
        "message": "Usuario actualizado exitosamente"
    }

@app.delete("/usuarios/{user_id}", tags=["Users"])
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """
    Eliminar un usuario existente.
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    
    user = db.query(User).filter(User.id == user_uuid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

# --- 4. Endpoints de Reconocimiento Facial ---

@app.post("/recognize/", tags=["Face Recognition"])
async def recognize_face(
    face_image: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Reconocer un rostro en la imagen proporcionada.
    Incluye sistema de alertas para usuarios marcados como "requisitoriado".
    """
    # Validar tipo de archivo
    if not face_image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    # Guardar imagen temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
        content = await face_image.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Extraer embedding del rostro
        embedding = extraer_embedding_pca(tmp_file_path)
        print("[DEBUG] Embedding extraído para reconocimiento:", embedding)
        if embedding is None:
            raise HTTPException(status_code=400, detail="No se pudo detectar un rostro en la imagen")
        
        # Buscar coincidencias en la base de datos usando pgvector
        users = db.query(User).all()
        print(f"[DEBUG] Usuarios en base de datos: {len(users)}")
        best_match = None
        best_distance = float('inf')
        
        for user in users:
            print(f"[DEBUG] Comparando con usuario: id={user.id}, name={user.name}")
            if user.embedding is not None:
                print(f"[DEBUG] Embedding usuario: {user.embedding}")
                # Calcular distancia euclidiana
                distance = sum((a - b) ** 2 for a, b in zip(embedding, user.embedding)) ** 0.5
                print(f"[DEBUG] Distancia calculada: {distance}")
                if distance < best_distance:
                    best_distance = distance
                    best_match = user
            else:
                print(f"[DEBUG] Usuario {user.id} no tiene embedding guardado.")
        
        # Umbral de similitud (ajustar según necesidad)
        threshold = RECOGNITION_THRESHOLD
        print(f"[DEBUG] Mejor distancia encontrada: {best_distance}, Umbral: {threshold}")
        if best_match:
            print(f"[DEBUG] Usuario best_match: id={best_match.id}, name={best_match.name}")
        print(f"[DEBUG] Reconocido? {best_match is not None and best_distance < threshold}")
        
        if best_match and best_distance < threshold:
            # Verificar si el usuario está marcado como "requisitoriado"
            alert_triggered = best_match.requested and ALERT_ENABLED
            
            # Si hay alerta, registrar en background
            if alert_triggered and background_tasks:
                background_tasks.add_task(
                    log_alert, 
                    user_id=str(best_match.id),
                    user_name=best_match.name,
                    email=best_match.email,
                    telefono=best_match.telefono,
                    confidence=1.0 / (1.0 + best_distance)
                )
            
            return {
                "success": True,
                "user": {
                    "id": str(best_match.id), 
                    "nombre": best_match.name.split()[0] if best_match.name else "",
                    "apellido": " ".join(best_match.name.split()[1:]) if best_match.name and len(best_match.name.split()) > 1 else "",
                    "email": best_match.email,
                    "telefono": best_match.telefono,
                    "requisitoriado": best_match.requested,
                    "url_foto": f"/static/fotos_perfil/{best_match.id}.jpg"
                },
                "confidence": 1.0 / (1.0 + best_distance),
                "distance": best_distance,
                "alert_triggered": alert_triggered,
                "alert_message": "¡ALERTA! Usuario marcado como requisitoriado." if alert_triggered else None
            }
        else:
            return {
                "success": False,
                "message": "Rostro no reconocido",
                "distance": best_distance if best_match else None,
                "alert_triggered": False
            }
    
    finally:
        # Limpiar archivo temporal
        os.unlink(tmp_file_path)

# --- 5. Endpoints de Sistema de Alertas ---

@app.get("/alertas/", tags=["Alerts"])
def get_alerts(db: Session = Depends(get_db)):
    """
    Obtener lista de usuarios marcados como "requisitoriado".
    """
    requested_users = db.query(User).filter(User.requested == True).all()
    return [
        {
            "id": str(user.id),
            "nombre": user.name.split()[0] if user.name else "",
            "apellido": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
            "email": user.email,
            "telefono": user.telefono,
            "url_foto": f"/static/fotos_perfil/{user.id}.jpg",
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in requested_users
    ]

@app.post("/usuarios/{user_id}/toggle-requisitoriado", tags=["Alerts"])
def toggle_requested_status(user_id: str, db: Session = Depends(get_db)):
    """
    Cambiar el estado "requisitoriado" de un usuario.
    """
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID de usuario inválido")
    
    user = db.query(User).filter(User.id == user_uuid).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.requested = not user.requested
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    return {
        "id": str(user.id),
        "nombre": user.name.split()[0] if user.name else "",
        "apellido": " ".join(user.name.split()[1:]) if user.name and len(user.name.split()) > 1 else "",
        "requisitoriado": user.requested,
        "message": f"Usuario {'marcado como requisitoriado' if user.requested else 'desmarcado como requisitoriado'}"
    }

# --- 6. Endpoints de Estadísticas y Mejora Continua ---

@app.get("/stats/", tags=["Statistics"])
def get_system_stats(db: Session = Depends(get_db)):
    """
    Obtener estadísticas del sistema para monitoreo y mejora continua.
    """
    total_users = db.query(User).count()
    requested_users = db.query(User).filter(User.requested == True).count()
    
    return {
        "total_users": total_users,
        "requisitoriado_users": requested_users,
        "recognition_threshold": RECOGNITION_THRESHOLD,
        "alert_system_enabled": ALERT_ENABLED,
        "system_version": "2.0.0"
    }

# --- 7. Endpoint de Salud ---
@app.get("/health", tags=["Health"])
def health_check():
    """
    Verificar el estado de la API.
    """
    return {"status": "healthy", "message": "API funcionando correctamente"}

# --- 8. Funciones de Utilidad ---

def log_alert(user_id: str, user_name: str, email: str, telefono: str, confidence: float):
    """
    Registrar alerta en el sistema (simulación de notificación a autoridades).
    """
    alert_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "user_name": user_name,
        "email": email,
        "telefono": telefono,
        "confidence": confidence,
        "alert_type": "USER_RECOGNIZED_REQUESTED"
    }
    
    # En producción, aquí enviarías la alerta a un sistema de notificaciones
    # Por ahora, solo lo guardamos en un archivo de log
    try:
        with open("alerts.log", "a") as f:
            f.write(json.dumps(alert_data) + "\n")
    except Exception as e:
        print(f"Error al registrar alerta: {e}")

# --- 9. Inicialización de la Base de Datos ---
@app.on_event("startup")
async def startup_event():
    """
    Inicializar la base de datos y el modelo PCA al arrancar la aplicación.
    """
    print("🚀 Iniciando aplicación de reconocimiento facial...")
    
    # Crear tablas de base de datos
    create_db_tables()
    print("✅ Base de datos inicializada")
    
    # Inicializar modelo PCA si no existe
    try:
        from init_model import init_model
        if init_model():
            print("✅ Modelo PCA inicializado")
        else:
            print("⚠️  Error inicializando modelo PCA")
    except Exception as e:
        print(f"⚠️  Error durante inicialización del modelo: {e}")
    
    print("🎯 Aplicación lista para recibir requests")

@app.get("/debug/distances", tags=["Debug"])
def debug_distance_matrix(db: Session = Depends(get_db)):
    """
    Devuelve una matriz de distancias euclidianas entre todos los embeddings de usuarios.
    Útil para depuración y ajuste de umbral.
    """
    users = db.query(User).all()
    user_infos = [(str(u.id), u.name, u.embedding) for u in users if u.embedding is not None]
    n = len(user_infos)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0.0)
            else:
                emb1 = user_infos[i][2]
                emb2 = user_infos[j][2]
                dist = sum((a - b) ** 2 for a, b in zip(emb1, emb2)) ** 0.5
                row.append(dist)
        matrix.append(row)
    # Return as JSON with user info
    return {
        "users": [{"id": uid, "name": name} for uid, name, _ in user_infos],
        "distance_matrix": matrix
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
