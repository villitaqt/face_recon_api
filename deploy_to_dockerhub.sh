#!/bin/bash

# Script para construir y subir la imagen a Docker Hub
# Uso: ./deploy_to_dockerhub.sh [version]

set -e

# Configuración
DOCKER_USERNAME="tu_usuario_dockerhub"  # Cambiar por tu usuario de Docker Hub
IMAGE_NAME="facerecon-api"
VERSION=${1:-"latest"}

echo "🐳 Construyendo imagen Docker para producción..."

# Construir imagen de producción
docker build -f Dockerfile.prod -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} .

echo "✅ Imagen construida: ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

# Etiquetar como latest si no es la versión actual
if [ "$VERSION" != "latest" ]; then
    docker tag ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
    echo "✅ Imagen etiquetada como latest"
fi

echo "📤 Subiendo imagen a Docker Hub..."

# Subir imagen a Docker Hub
docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}

if [ "$VERSION" != "latest" ]; then
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
fi

echo "🎉 ¡Imagen subida exitosamente a Docker Hub!"
echo "📋 URL de la imagen: ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"
echo ""
echo "🔧 Para usar en Render.com:"
echo "   Image: ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"
echo "   Port: 8000"
echo ""
echo "🔧 Variables de entorno necesarias:"
echo "   DATABASE_URL=postgresql://user:password@host:port/database"
echo "   FACE_RECOGNITION_THRESHOLD=4000"
echo "   ALERT_ENABLED=true" 