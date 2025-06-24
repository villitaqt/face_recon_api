# 🚀 Guía de Despliegue - Face Recognition API

## 📋 Resumen

Esta guía te ayudará a desplegar la API de Reconocimiento Facial en Render.com usando Docker Hub.

## 🐳 Paso 1: Preparar Docker Hub

### 1.1 Crear cuenta en Docker Hub
- Ve a [hub.docker.com](https://hub.docker.com)
- Crea una cuenta gratuita

### 1.2 Configurar el script de despliegue
Edita `deploy_to_dockerhub.sh` y cambia:
```bash
DOCKER_USERNAME="tu_usuario_dockerhub"  # Tu usuario de Docker Hub
```

### 1.3 Construir y subir la imagen
```bash
# Dar permisos de ejecución
chmod +x deploy_to_dockerhub.sh

# Construir y subir (versión específica)
./deploy_to_dockerhub.sh v1.0.0

# O usar latest
./deploy_to_dockerhub.sh
```

## 🌐 Paso 2: Configurar Render.com

### 2.1 Crear cuenta en Render
- Ve a [render.com](https://render.com)
- Crea una cuenta gratuita

### 2.2 Configurar el render.yaml
Edita `render.yaml` y cambia:
```yaml
image: tu_usuario_dockerhub/facerecon-api:latest  # Tu usuario de Docker Hub
```

### 2.3 Desplegar en Render
1. Conecta tu repositorio de GitHub a Render
2. Render detectará automáticamente el `render.yaml`
3. El despliegue comenzará automáticamente

## 🔧 Configuración de Variables de Entorno

### Variables requeridas:
- `DATABASE_URL`: URL de conexión a PostgreSQL (se configura automáticamente)
- `FACE_RECOGNITION_THRESHOLD`: 4000 (umbral de reconocimiento)
- `ALERT_ENABLED`: true (sistema de alertas)

### Variables opcionales:
- `PYTHONPATH`: /app
- `PYTHONUNBUFFERED`: 1

## 📊 Características del Despliegue

### ✅ Incluido en la imagen:
- **Modelo PCA robusto** (704 imágenes de entrenamiento)
- **150 componentes PCA** (alta precisión)
- **Inicialización automática** del modelo
- **Sistema de alertas** configurado
- **API completa** lista para producción

### 🔄 Inicialización automática:
- La aplicación entrena automáticamente el modelo PCA si no existe
- Usa LFW dataset + data augmentation para robustez
- Configura la base de datos automáticamente

## 🧪 Verificación del Despliegue

### 1. Health Check
```bash
curl https://tu-app.onrender.com/health
```

### 2. Endpoints disponibles
- `GET /` - Información de la API
- `GET /health` - Estado del servidor
- `GET /stats/` - Estadísticas del sistema
- `POST /usuarios/` - Registrar usuario
- `POST /recognize/` - Reconocimiento facial
- `GET /alertas/` - Usuarios requisitoriados

## 🔍 Troubleshooting

### Error: "Modelo PCA no encontrado"
- Normal durante el primer despliegue
- El modelo se entrenará automáticamente
- Puede tomar 2-3 minutos

### Error: "Database connection failed"
- Verificar que la base de datos PostgreSQL esté creada
- Verificar la variable `DATABASE_URL`

### Error: "Port already in use"
- Render usa automáticamente el puerto 8000
- No cambiar la configuración del puerto

## 📱 Uso desde la App Móvil

### URL base:
```
https://tu-app.onrender.com
```

### Endpoints principales:
- **Registro**: `POST /usuarios/`
- **Reconocimiento**: `POST /recognize/`
- **Alertas**: `GET /alertas/`

## 🎯 Estado Final

Una vez desplegado, tendrás:
- ✅ API de reconocimiento facial funcionando
- ✅ Modelo PCA robusto entrenado
- ✅ Base de datos PostgreSQL configurada
- ✅ Sistema de alertas activo
- ✅ Listo para ser consumido por la app móvil

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en Render Dashboard
2. Verifica las variables de entorno
3. Asegúrate de que la imagen esté en Docker Hub 