# face_embedding_extractor.py
# ---------------------------
# Este módulo contiene la función para cargar el modelo PCA entrenado
# y usarlo para extraer el vector de características (embedding) de un rostro.
# Este embedding será utilizado para las comparaciones en la base de datos.

import numpy as np
import pickle
import os

# Importamos la función de pre-procesamiento de nuestro módulo
# Asegúrate de que facial_preprocesador.py esté en el mismo directorio
# o en una ruta accesible por Python.
from facial_preprocesador import preprocesar_cara

# --- Inicialización Global del Modelo PCA ---
# Cargamos el modelo PCA entrenado una única vez al inicio del script/servidor.
# Esto es crucial para la eficiencia.
model_pca = None
ruta_modelo_pca = 'models/pca_model.pkl' # Ruta donde se guardará/cargará el modelo PCA

try:
    if os.path.exists(ruta_modelo_pca):
        with open(ruta_modelo_pca, 'rb') as f:
            model_pca = pickle.load(f)
        print(f"Modelo PCA cargado exitosamente desde: {ruta_modelo_pca}")
    else:
        print(f"Advertencia: Modelo PCA no encontrado en {ruta_modelo_pca}. Por favor, entrena el modelo primero ejecutando entrenador_pca.py.")
except Exception as e:
    print(f"Error grave: no se pudo cargar el modelo PCA. Error: {e}")
    model_pca = None

def extraer_embedding_pca(ruta_imagen):
    """
    Extrae el vector de características (embedding) de un rostro desde una imagen
    utilizando el pipeline de pre-procesamiento y el modelo PCA entrenado.

    Pasos:
    1. Pre-procesar la imagen del rostro usando la función de facial_preprocesador.py.
       Esta función ya detecta, recorta, convierte a gris, ecualiza y redimensiona a (100, 100).
    2. Aplanar la imagen pre-procesada a un vector 1D.
    3. Pasar el vector aplanado al modelo PCA para obtener su embedding (vector de características reducido).

    Args:
        ruta_imagen (str): La ruta completa al archivo de imagen.

    Returns:
        numpy.ndarray: El vector de características (embedding) del rostro,
                       o None si ocurre algún error (ej. no se detecta cara, modelo PCA no cargado).
    """
    if model_pca is None:
        print("Error: El modelo PCA no está inicializado. No se puede extraer el embedding.")
        return None

    # 1. Pre-procesar la imagen del rostro
    # La función preprocesar_cara devuelve la imagen en (100, 100) en escala de grises.
    cara_estandarizada = preprocesar_cara(ruta_imagen, tamaño_requerido=(100, 100))
    
    if cara_estandarizada is None:
        print(f"No se pudo obtener una cara estandarizada de {os.path.basename(ruta_imagen)}. Skipping embedding extraction.")
        return None
    
    # 2. Aplanar la imagen pre-procesada a un vector 1D
    # El modelo PCA espera un vector 1D como entrada.
    cara_aplanada = cara_estandarizada.flatten()

    # PCA.transform() espera un batch de muestras, incluso si es solo una.
    # np.expand_dims añade una dimensión extra al inicio para simular un "batch" de 1 muestra.
    embedding = model_pca.transform(np.expand_dims(cara_aplanada, axis=0))[0]
    
    return embedding

# --- Bloque de Prueba ---
if __name__ == "__main__":
    # Para probar esta función, asegúrate de haber:
    # 1. Entrenado el modelo PCA ejecutando entrenador_pca.py previamente.
    # 2. Creado una carpeta 'test_images' y colocado algunas imágenes de rostros en ella.

    test_image_dir = 'test_images' # Asegúrate de que esta carpeta exista y contenga imágenes

    if not os.path.exists(test_image_dir):
        print(f"Error: El directorio de pruebas '{test_image_dir}' no existe.")
        print("Crea la carpeta y coloca algunas imágenes de rostros para probar el extractor.")
    elif not os.path.exists(ruta_modelo_pca):
        print(f"Error: El modelo PCA no fue encontrado en '{ruta_modelo_pca}'.")
        print("Por favor, ejecuta 'entrenador_pca.py' primero para entrenar y guardar el modelo.")
    else:
        print(f"\n--- Probando face_embedding_extractor.py con imágenes de '{test_image_dir}' ---")
        for filename in os.listdir(test_image_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(test_image_dir, filename)
                print(f"Procesando: {filename}")
                
                embedding = extraer_embedding_pca(full_path)

                if embedding is not None:
                    print(f"  Embedding extraído exitosamente. Longitud: {len(embedding)}")
                    print(f"  Primeros 5 valores del embedding: {embedding[:5]}")
                    # La longitud del embedding será n_componentes definida en el entrenamiento del PCA.
                else:
                    print(f"  Fallo al extraer el embedding del rostro en {filename}.")
        print("\n--- Pruebas de extracción de embeddings completadas ---")
