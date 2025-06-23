# Guía de Despliegue en Render.com

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Cuenta en [GitHub](https://github.com)
- Código subido a un repositorio de GitHub

## 🚀 Pasos para el Despliegue

### 1. Preparar el Repositorio

Asegúrate de que tu repositorio contenga estos archivos:
- `main.py` - Aplicación FastAPI
- `database.py` - Configuración de base de datos
- `requirements.txt` - Dependencias de Python
- `render.yaml` - Configuración de Render
- `models/pca_model.pkl` - Modelo PCA entrenado
- `facial_preprocesador.py` - Preprocesamiento de imágenes
- `face_embedding_extractor.py` - Extracción de embeddings

### 2. Crear Servicio en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Blueprint"**
3. Conecta tu cuenta de GitHub
4. Selecciona tu repositorio
5. Render detectará automáticamente el `render.yaml`

### 3. Configuración Automática

El archivo `render.yaml` configurará automáticamente:
- **Servicio Web**: FastAPI en Python
- **Base de Datos**: PostgreSQL con extensión pgvector
- **Almacenamiento**: Persistent Disk para imágenes
- **Variables de Entorno**: Configuración automática

### 4. Variables de Entorno

Render configurará automáticamente:
- `DATABASE_URL` - Conexión a PostgreSQL
- `FACE_RECOGNITION_THRESHOLD` - Umbral de reconocimiento (4000)
- `ALERT_ENABLED` - Sistema de alertas (true)

### 5. Configuración Manual (si es necesario)

Si no usas `render.yaml`, configura manualmente:

#### Servicio Web:
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

#### Base de Datos:
- Crear servicio PostgreSQL
- Habilitar extensión pgvector: `CREATE EXTENSION vector;`

#### Persistent Disk:
- Nombre: `facerecon-images`
- Mount Path: `/opt/render/project/src/static/fotos_perfil`
- Tamaño: 1GB

## 🔧 Configuración de Base de Datos

### Habilitar pgvector (requerido)

Una vez creada la base de datos, ejecuta en el SQL Editor de Render:

```sql
CREATE EXTENSION vector;
```

### Verificar Tablas

Las tablas se crearán automáticamente al iniciar la aplicación.

## 📱 Endpoints Disponibles

Una vez desplegado, tu API estará disponible en:
`https://tu-app.onrender.com`

### Endpoints Principales:
- `GET /` - Información de la API
- `GET /health` - Estado de salud
- `POST /usuarios/` - Registrar usuario
- `GET /usuarios/` - Listar usuarios
- `POST /recognize/` - Reconocimiento facial
- `GET /alertas/` - Usuarios con alertas

## 🖼️ Almacenamiento de Imágenes

Las imágenes se guardan en:
- **Local**: `static/fotos_perfil/`
- **Render**: Persistent Disk montado en `/opt/render/project/src/static/fotos_perfil`

Las imágenes son accesibles via:
`https://tu-app.onrender.com/static/fotos_perfil/{user_id}.jpg`

## 🔍 Monitoreo y Logs

- **Logs**: Disponibles en el dashboard de Render
- **Métricas**: Uso de CPU, memoria, red
- **Estado**: Health checks automáticos

## 🚨 Solución de Problemas

### Error de Dependencias
- Verifica que `requirements.txt` esté actualizado
- Revisa los logs de build

### Error de Base de Datos
- Verifica que pgvector esté habilitado
- Confirma la conexión en variables de entorno

### Error de Imágenes
- Verifica que el Persistent Disk esté montado
- Confirma permisos de escritura

### Error de Modelo PCA
- Asegúrate de que `models/pca_model.pkl` esté incluido
- Verifica que el modelo esté entrenado

## 📞 Soporte

- **Render Docs**: [docs.render.com](https://docs.render.com)
- **Logs**: Dashboard de Render → Tu servicio → Logs
- **Variables de Entorno**: Dashboard de Render → Tu servicio → Environment

## 🔄 Actualizaciones

Para actualizar la aplicación:
1. Haz push a tu repositorio de GitHub
2. Render detectará automáticamente los cambios
3. Desplegará la nueva versión automáticamente

## 💰 Costos

- **Starter Plan**: $7/mes (incluye 750 horas gratuitas)
- **Base de Datos**: $7/mes
- **Persistent Disk**: $0.25/GB/mes

**Total estimado**: ~$15/mes para uso básico 