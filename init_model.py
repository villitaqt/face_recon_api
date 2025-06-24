# init_model.py
# Script de inicialización para entrenar el modelo PCA si no existe

import os
import sys

def init_model():
    """
    Inicializa el modelo PCA si no existe.
    """
    model_path = 'models/pca_model.pkl'
    
    if os.path.exists(model_path):
        print("✅ Modelo PCA ya existe")
        return True
    
    print("🔄 Modelo PCA no encontrado. Entrenando modelo...")
    
    try:
        # Importar y ejecutar el entrenador PCA estándar
        from entrenador_pca import entrenar_modelo_pca
        
        # Entrenar con 33 componentes (versión estable)
        success = entrenar_modelo_pca(
            directorio_datos='data/initial_enrollment/',
            ruta_modelo_salida='models/pca_model.pkl',
            n_componentes=33
        )
        
        if success:
            print("✅ Modelo PCA entrenado exitosamente")
            return True
        else:
            print("❌ Error entrenando modelo PCA")
            return False
            
    except Exception as e:
        print(f"❌ Error durante inicialización: {e}")
        return False

if __name__ == "__main__":
    init_model() 