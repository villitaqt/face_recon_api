# Guía de Despliegue en Render.com con Docker

## 📋 Requisitos Previos

- Cuenta en [Render.com](https://render.com)
- Cuenta en [GitHub](https://github.com)
- Código subido a un repositorio de GitHub
- Docker instalado localmente (para pruebas)

## 🐳 Configuración Docker

### Archivos de Configuración
- `Dockerfile` - Configuración del contenedor
- `docker-compose.yml` - Para pruebas locales
- `render.yaml` - Configuración de Render con Docker
- `.dockerignore` - Archivos excluidos del build

## 🚀 Pasos para el Despliegue

### 1. Preparar el Repositorio

Asegúrate de que tu repositorio contenga estos archivos:
- `main.py` - Aplicación FastAPI
- `database.py` - Configuración de base de datos
- `requirements.txt` - Dependencias de Python
- `Dockerfile` - Configuración Docker
- `render.yaml` - Configuración de Render
- `models/pca_model.pkl` - Modelo PCA entrenado
- `facial_preprocesador.py` - Preprocesamiento de imágenes
- `face_embedding_extractor.py` - Extracción de embeddings

### 2. Probar Localmente con Docker

```bash
# Construir la imagen
docker build -t facerecon-api .

# Ejecutar con docker-compose
docker-compose up --build

# O ejecutar directamente
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://villitaqt:VIwhRET7lfwuyggiYPU7KERwqorA1ndH@dpg-d1cpf86r433s7384v5hg-a.oregon-postgres.render.com/face_recon_db" \
  -e FACE_RECOGNITION_THRESHOLD=4000 \
  -e ALERT_ENABLED=true \
  -v $(pwd)/static/fotos_perfil:/app/static/fotos_perfil \
  facerecon-api
```

### 3. Crear Servicio en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Haz clic en **"New +"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Render detectará automáticamente el `render.yaml`
5. Haz clic en **"Apply"**

### 4. Configuración Automática

El `render.yaml` configurará automáticamente:
- ✅ **Servicio web** con Docker
- ✅ **Variables de entorno** (DATABASE_URL, etc.)
- ✅ **Persistent Disk** para imágenes (`/app/static/fotos_perfil`)
- ✅ **Health checks** automáticos

## 🔧 Variables de Entorno

El servicio usará estas variables automáticamente:
- `DATABASE_URL` - Conexión a PostgreSQL
- `FACE_RECOGNITION_THRESHOLD` - Umbral de reconocimiento (4000)
- `ALERT_ENABLED` - Sistema de alertas (true)

## 💾 Persistencia de Imágenes

### En Render:
- **Persistent Disk** montado en `/app/static/fotos_perfil`
- **1GB** de almacenamiento
- **Sobrevive** a reinicios y redeploys
- **URLs accesibles** via `/static/fotos_perfil/{user_id}.jpg`

### Localmente:
- **Volume Docker** montado en `./static/fotos_perfil`
- **Sincronizado** con el host
- **Persistente** entre ejecuciones

## 🧪 Testing

### Health Check
```bash
curl https://tu-app.onrender.com/health
```

### Endpoints Disponibles
- `GET /health` - Estado del servicio
- `GET /usuarios/` - Lista de usuarios
- `POST /usuarios/` - Crear usuario
- `POST /recognize/` - Reconocimiento facial
- `GET /alertas/` - Usuarios con alertas

## 🔍 Troubleshooting

### Problemas Comunes

1. **Build falla:**
   - Verifica que `Dockerfile` esté en la raíz
   - Revisa los logs de build en Render

2. **Imágenes no persisten:**
   - Verifica que el Persistent Disk esté montado
   - Confirma la ruta `/app/static/fotos_perfil`

3. **Error de conexión a DB:**
   - Verifica `DATABASE_URL` en variables de entorno
   - Confirma que la base de datos esté activa

4. **Servicio no inicia:**
   - Revisa los logs en Render Dashboard
   - Verifica el health check

### Logs de Render
1. Ve a tu servicio en el dashboard
2. Haz clic en **"Logs"**
3. Busca errores de arranque o conexión

## 📱 Configuración del Frontend

### URL Base
```
https://tu-app.onrender.com
```

### Endpoints de Imágenes
```
https://tu-app.onrender.com/static/fotos_perfil/{user_id}.jpg
```

## ✅ Checklist Post-Despliegue

- [ ] Servicio está "Live" en Render
- [ ] Health check responde correctamente
- [ ] Endpoints funcionan (probar con Postman)
- [ ] Imágenes se guardan y sirven correctamente
- [ ] Frontend conecta sin problemas
- [ ] Reconocimiento facial funciona
- [ ] Base de datos conecta correctamente

## 🚀 ¡Listo!

Tu API estará disponible en:
```
https://tu-app.onrender.com
```

Y funcionará desde cualquier lugar sin necesidad de estar en tu red local. 