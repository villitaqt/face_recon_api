# Sistema de Reconocimiento Facial

Un sistema completo de reconocimiento facial utilizando PCA (Principal Component Analysis) con FastAPI y PostgreSQL con pgvector.

## 🚀 Características

- **Detección facial** usando MTCNN
- **Extracción de características** con PCA
- **Almacenamiento vectorial** en PostgreSQL con pgvector
- **API REST** con FastAPI
- **Docker** para fácil despliegue
- **Reconocimiento en tiempo real**

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 16+ con extensión pgvector
- Docker y Docker Compose (opcional)

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd proyecto_facerecon
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

#### Opción A: Usando Docker (Recomendado)
```bash
docker-compose up -d
```

#### Opción B: PostgreSQL local
1. Instalar PostgreSQL 16+
2. Habilitar extensión pgvector:
```sql
CREATE EXTENSION vector;
```

### 5. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 6. Entrenar el modelo PCA
```bash
python entrenador_pca.py
```

### 7. Inicializar la base de datos
```bash
python database.py
```

## 🚀 Uso

### Iniciar la API
```bash
python main.py
```

La API estará disponible en `http://localhost:8000`

### Documentación automática
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 Endpoints de la API

### Usuarios
- `POST /users/` - Crear usuario con imagen facial
- `GET /users/` - Listar todos los usuarios
- `GET /users/{user_id}` - Obtener usuario específico
- `DELETE /users/{user_id}` - Eliminar usuario

### Reconocimiento Facial
- `POST /recognize/` - Reconocer rostro en imagen

### Utilidades
- `GET /` - Información de la API
- `GET /health` - Estado de salud del sistema

## 🔧 Configuración

### Variables de entorno importantes

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión a PostgreSQL | `postgresql://admin:admin@localhost:5432/reconocimiento_facial_db` |
| `FACE_RECOGNITION_THRESHOLD` | Umbral de similitud para reconocimiento | `1000` |
| `PCA_COMPONENTS` | Número de componentes PCA | `150` |

## 📁 Estructura del proyecto

```
proyecto_facerecon/
├── main.py                 # API principal con FastAPI
├── database.py             # Configuración de base de datos
├── facial_preprocesador.py # Preprocesamiento de imágenes
├── face_embedding_extractor.py # Extracción de embeddings
├── entrenador_pca.py       # Entrenamiento del modelo PCA
├── requirements.txt        # Dependencias de Python
├── docker-compose.yml      # Configuración de Docker
├── .gitignore             # Archivos a ignorar en Git
├── env.example            # Ejemplo de variables de entorno
├── README.md              # Este archivo
├── data/
│   └── initial_enrollment/ # Imágenes para entrenamiento
├── models/
│   └── pca_model.pkl      # Modelo PCA entrenado
└── test_images/           # Imágenes de prueba
```

## 🧪 Pruebas

### Probar preprocesamiento
```bash
python facial_preprocesador.py
```

### Probar extracción de embeddings
```bash
python face_embedding_extractor.py
```

### Probar la API
```bash
# Crear usuario
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: multipart/form-data" \
  -F "name=Juan Pérez" \
  -F "face_image=@/path/to/image.jpg"

# Reconocer rostro
curl -X POST "http://localhost:8000/recognize/" \
  -H "Content-Type: multipart/form-data" \
  -F "face_image=@/path/to/image.jpg"
```

## 🔍 Solución de problemas

### Error: "No se pudo cargar el modelo PCA"
- Asegúrate de haber ejecutado `python entrenador_pca.py`
- Verifica que el archivo `models/pca_model.pkl` existe

### Error: "No se pudo detectar un rostro"
- Verifica que la imagen contiene un rostro claro
- Asegúrate de que la imagen no esté muy oscura o borrosa

### Error de conexión a la base de datos
- Verifica que PostgreSQL esté ejecutándose
- Confirma que las credenciales en `.env` son correctas
- Asegúrate de que la extensión pgvector esté habilitada

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- Tu nombre - Trabajo inicial

## 🙏 Agradecimientos

- MTCNN para detección facial
- scikit-learn para PCA
- FastAPI para el framework web
- pgvector para almacenamiento vectorial 