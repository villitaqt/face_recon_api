# entrenador_pca.py
# -----------------
# Este es un script de uso offline. Su propósito es "entrenar" nuestro
# modelo PCA. Lee un conjunto de imágenes de rostros, aprende las
# características faciales más importantes (Eigenfaces) y guarda el
# modelo resultante para que nuestra API pueda usarlo en producción.

import os
import numpy as np
import pickle
from sklearn.decomposition import PCA
# Importamos la función de pre-procesamiento de nuestro módulo
from facial_preprocesador import preprocesar_cara 

def entrenar_modelo_pca(directorio_datos, ruta_modelo_salida, n_componentes=150):
    """
    Entrena un modelo PCA a partir de las imágenes en un directorio y lo guarda.

    Args:
        directorio_datos (str): Ruta a la carpeta con las imágenes de entrenamiento (ej: 'data/initial_enrollment/').
        ruta_modelo_salida (str): Ruta completa donde se guardará el modelo entrenado
                                  (ej: 'models/pca_model.pkl').
        n_componentes (int): El número de "Eigenfaces" a generar. Este será
                              la longitud de nuestros vectores de embedding.
    """
    caras_preparadas = []
    
    print("--- Iniciando Fase de Entrenamiento del Modelo PCA ---")
    print(f"Leyendo imágenes del directorio: {directorio_datos}")

    # 1. Leer y pre-procesar todas las imágenes de entrenamiento
    for nombre_archivo in os.listdir(directorio_datos):
        ruta_completa = os.path.join(directorio_datos, nombre_archivo)
        
        # Solo procesar archivos de imagen
        if not nombre_archivo.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Usamos nuestra función de pre-procesamiento
        cara = preprocesar_cara(ruta_completa)
        
        if cara is not None:
            # Aplanamos la matriz de la imagen (100x100 -> 10000) y la añadimos a la lista
            caras_preparadas.append(cara.flatten())
        # Los mensajes de advertencia ya los muestra la función preprocesar_cara
            
    if len(caras_preparadas) == 0:
        print(f"\nError Crítico: No se encontraron imágenes válidas en el directorio '{directorio_datos}'.")
        print("Asegúrate de que la carpeta exista y contenga imágenes de rostros.")
        return

    if len(caras_preparadas) < n_componentes:
        print(f"\nError Crítico: Se necesitan al menos {n_componentes} imágenes válidas para entrenar el modelo,")
        print(f"pero solo se encontraron {len(caras_preparadas)}. Considera reducir n_componentes o añadir más imágenes.")
        # Podemos proceder si n_componentes es mayor que el número de muestras, PCA lo ajustará.
        # Pero es bueno advertir. Ajustar n_componentes si es mayor que num_samples - 1.
        if n_componentes >= len(caras_preparadas):
            print(f"Ajustando n_componentes a {len(caras_preparadas) - 1} para poder entrenar.")
            n_componentes = len(caras_preparadas) - 1
            if n_componentes <= 0:
                print("No hay suficientes muestras para PCA. Abortando.")
                return

    print(f"\nSe han procesado {len(caras_preparadas)} imágenes válidas.")
    print(f"Iniciando entrenamiento de PCA con {n_componentes} componentes...")
    
    # 2. Crear y entrenar el modelo PCA
    pca = PCA(n_components=n_componentes)
    pca.fit(np.array(caras_preparadas))
    
    print("¡Entrenamiento completado!")
    
    # 3. Guardar el modelo entrenado en un archivo
    try:
        # Asegurarse de que el directorio 'models/' exista
        os.makedirs(os.path.dirname(ruta_modelo_salida), exist_ok=True)
        
        with open(ruta_modelo_salida, 'wb') as f:
            pickle.dump(pca, f)
        print(f"\n--- Modelo PCA guardado exitosamente en: {ruta_modelo_salida} ---")
    except Exception as e:
        print(f"\nError Crítico: No se pudo guardar el modelo. Error: {e}")

# Este bloque solo se ejecuta cuando corres 'python entrenador_pca.py' directamente
if __name__ == '__main__':
    # Definir las rutas de entrada y salida
    # !IMPORTANTE: Crea esta carpeta y coloca las 30 imágenes de alumnos aquí!
    directorio_datos_entrenamiento = 'data/initial_enrollment/' 
    ruta_modelo_salida = 'models/pca_model.pkl'

    # Crea el directorio si no existe
    if not os.path.exists(directorio_datos_entrenamiento):
        os.makedirs(directorio_datos_entrenamiento)
        print(f"Directorio '{directorio_datos_entrenamiento}' creado.")
        print("Por favor, coloca las imágenes de perfil de los 30 alumnos aquí para entrenar el PCA.")
    else:
        # Llamar a la función principal
        entrenar_modelo_pca(directorio_datos_entrenamiento, ruta_modelo_salida)
