# facial_preprocesador.py
# -----------------------
# Este módulo es una herramienta fundamental en nuestro pipeline de IA.
# Su responsabilidad es tomar una imagen cruda y devolver un rostro
# perfectamente estandarizado (100x100 píxeles, escala de grises, ecualizado)
# listo para el análisis PCA.

import cv2
import numpy as np
import os
from mtcnn.mtcnn import MTCNN

# --- Inicialización del Modelo de Detección ---
# Creamos la instancia del detector MTCNN aquí, a nivel de módulo.
# Esto es una optimización clave para que el modelo pesado se cargue
# en memoria solo una vez cuando la aplicación se inicia.
try:
    detector_mtcnn = MTCNN()
except Exception as e:
    print(f"Error grave: no se pudo inicializar el detector MTCNN. Error: {e}")
    detector_mtcnn = None

def preprocesar_cara(ruta_imagen, tamaño_requerido=(100, 100)):
    """
    Pipeline completo de pre-procesamiento de un rostro desde una imagen
    para compatibilidad con el modelo PCA.

    Pasos:
    1. Lee la imagen.
    2. Usa MTCNN para detectar la cara principal.
    3. Recorta la cara.
    4. La convierte a escala de grises.
    5. Normaliza la iluminación con Ecualización del Histograma.
    6. La redimensiona a un tamaño estándar (100x100 píxeles).

    Args:
        ruta_imagen (str): La ruta completa al archivo de imagen.
        tamaño_requerido (tuple): El tamaño final de la imagen (ancho, alto).
                                 Por defecto, 100x100 píxeles para PCA.

    Returns:
        numpy.ndarray: La imagen del rostro procesada y estandarizada (escala de grises),
                       o None si ocurre algún error o no se detecta una cara.
    """
    if detector_mtcnn is None:
        print("Error: El detector MTCNN no está inicializado.")
        return None

    # 1. Leer la imagen desde la ruta proporcionada
    img = cv2.imread(ruta_imagen)
    if img is None:
        print(f"Advertencia: No se pudo leer la imagen en la ruta: {ruta_imagen}")
        return None

    # MTCNN espera imágenes RGB para la detección
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    
    # 2. Detectar rostros en la imagen usando MTCNN
    resultados = detector_mtcnn.detect_faces(img_rgb)

    if resultados:
        # Tomamos el primer rostro detectado (generalmente el más prominente)
        x, y, ancho, alto = resultados[0]['box']
        
        # Corregir coordenadas negativas (un bug común de MTCNN en los bordes)
        x, y = abs(x), abs(y)
        
        # 3. Recortar la cara de la imagen original
        # Asegurarse de que el recorte no se salga de los límites de la imagen
        x2, y2 = x + ancho, y + alto
        cara = img[max(0, y):min(img.shape[0], y2), 
                   max(0, x):min(img.shape[1], x2)]

        if cara.size == 0:
            print(f"Advertencia: Recorte de cara inválido (tamaño cero) para {os.path.basename(ruta_imagen)}. Skipping.")
            return None

        # 4. Convertir la cara a escala de grises
        cara_gris = cv2.cvtColor(cara, cv2.COLOR_BGR2GRAY)

        # 5. Ecualización del Histograma para normalizar la iluminación
        cara_ecualizada = cv2.equalizeHist(cara_gris)

        # 6. Redimensionar la cara al tamaño estándar
        cara_estandarizada = cv2.resize(cara_ecualizada, tamaño_requerido)
        
        return cara_estandarizada
    else:
        # Si la lista de resultados está vacía, no se encontraron caras
        print(f"Advertencia: No se detectó ningún rostro en la imagen {os.path.basename(ruta_imagen)}.")
        return None

# --- Bloque de Prueba (para verificar la función) ---
if __name__ == "__main__":
    # Para probar esta función, crea un directorio 'test_images'
    # en el mismo nivel que tu script y coloca algunas fotos de rostros allí.
    
    test_image_dir = 'test_images'
    if not os.path.exists(test_image_dir):
        os.makedirs(test_image_dir)
        print(f"Directorio '{test_image_dir}' creado. Por favor, coloca algunas imágenes de rostros aquí para probar.")
    else:
        print(f"\n--- Probando facial_preprocesador.py con imágenes de '{test_image_dir}' ---")
        for filename in os.listdir(test_image_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(test_image_dir, filename)
                print(f"Procesando: {filename}")
                processed_face = preprocesar_cara(full_path)

                if processed_face is not None:
                    print(f"  Rostro procesado exitosamente. Dimensiones: {processed_face.shape} (esperado: (100, 100))")
                    # Opcional: Guarda la imagen procesada para ver el resultado
                    output_path = os.path.join(test_image_dir, f"processed_{filename}")
                    cv2.imwrite(output_path, processed_face) # Guarda directamente la imagen en escala de grises
                    print(f"  Guardado en: {output_path}")
                else:
                    print(f"  Fallo al procesar el rostro en {filename}.")
        print("\n--- Pruebas de pre-procesamiento completadas ---")
