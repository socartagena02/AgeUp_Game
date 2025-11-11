import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'modelo_cognitivo.pkl')
DATA_PATH = os.path.join(BASE_DIR, '..', '..', 'memorice', 'memorice_data.csv')

# --- NUEVO: Función para generar datos simulados ---
def generar_datos_simulados(n_samples=150):
    """
    Genera un DataFrame con datos simulados para el entrenamiento del modelo.
    """
    np.random.seed(42)
    
    # Leve: buen rendimiento (pocos clics, pocos fallos, reacción rápida)
    clicks_leve = np.random.randint(20, 40, n_samples // 3)
    fallos_leve = np.random.randint(1, 5, n_samples // 3)
    reaccion_leve = np.random.uniform(0.8, 1.5, n_samples // 3)
    
    # Moderado: rendimiento intermedio
    clicks_moderado = np.random.randint(35, 60, n_samples // 3)
    fallos_moderado = np.random.randint(4, 10, n_samples // 3)
    reaccion_moderado = np.random.uniform(1.4, 2.2, n_samples // 3)

    # Avanzado: rendimiento bajo (más clics, más fallos, reacción lenta)
    clicks_avanzado = np.random.randint(55, 90, n_samples - 2 * (n_samples // 3))
    fallos_avanzado = np.random.randint(8, 20, n_samples - 2 * (n_samples // 3))
    reaccion_avanzado = np.random.uniform(2.0, 3.5, n_samples - 2 * (n_samples // 3))

    data = pd.DataFrame({
        'total_clicks': np.concatenate([clicks_leve, clicks_moderado, clicks_avanzado]),
        'fallos': np.concatenate([fallos_leve, fallos_moderado, fallos_avanzado]),
        'tiempo_reaccion_promedio': np.concatenate([reaccion_leve, reaccion_moderado, reaccion_avanzado]),
        'nivel_cognitivo': ['Leve'] * (n_samples // 3) + ['Moderado'] * (n_samples // 3) + ['Avanzado'] * (n_samples - 2 * (n_samples // 3)),
    })
    return data

def map_dificultad_a_cognitivo(df):
    """
    Convierte la dificultad del juego a un nivel cognitivo esperado.
    Esta es una suposición inicial que puedes ajustar.
    """
    mapeo = {
        'basico': 'Leve',
        'intermedio': 'Moderado',
        'avanzado': 'Avanzado'
    }
    df['nivel_cognitivo'] = df['nivel_dificultad'].map(mapeo)
    # Eliminar filas donde la dificultad no se pudo mapear (si las hubiera)
    df.dropna(subset=['nivel_cognitivo'], inplace=True)
    return df

def entrenar_modelo(usar_datos_simulados=False):
    """
    Entrena un modelo de clasificación.
    - Si usar_datos_simulados es True, genera datos de prueba.
    - Si es False, intenta leer los datos reales del juego desde un CSV.
    """
    if usar_datos_simulados:
        print("🔥 Usando datos simulados para el entrenamiento.")
        data = generar_datos_simulados(n_samples=150)
        data['nivel_dificultad'] = data['nivel_cognitivo'].str.lower()
    else:
        print("📦 Usando datos reales desde `memorice_data.csv`.")
        if not os.path.exists(DATA_PATH):
            raise FileNotFoundError(f"No se encontró el archivo de datos en '{DATA_PATH}'. Juega algunas partidas en 'memorice.py' para generarlo.")
        data = pd.read_csv(DATA_PATH)
    # Verificar si hay suficientes datos
    if len(data) < 10:
        print("⚠️ Advertencia: Tienes muy pocos datos. El modelo puede no ser preciso.")
        print("Juega más partidas para mejorar la calidad del entrenamiento.")
        if len(data) == 0:
            print("❌ Error: El archivo de datos está vacío. No se puede entrenar.")
            return
        data = pd.read_csv(DATA_PATH)

    # Mapear la dificultad del juego a la etiqueta que queremos predecir
    data = map_dificultad_a_cognitivo(data)
        # Verificar si hay suficientes datos
    if len(data) < 10:
        print("⚠️ Advertencia: Tienes muy pocos datos. El modelo puede no ser preciso.")
        print("Juega más partidas para mejorar la calidad del entrenamiento.")
        if len(data) == 0:
            print("❌ Error: El archivo de datos está vacío. No se puede entrenar.")
            return

        # Mapear la dificultad del juego a la etiqueta que queremos predecir
        data = map_dificultad_a_cognitivo(data)

    print(f"📊 Datos cargados: {len(data)} partidas encontradas.")
    print("Distribución de niveles cognitivos (etiquetas):")
    print(data['nivel_cognitivo'].value_counts())
    
    # Características para entrenar (las que guardamos desde el juego)
    X = data[['total_clicks', 'fallos', 'tiempo_reaccion_promedio']] 
    y = data['nivel_cognitivo'] # Lo que queremos predecir

    # Asegurarse de que haya al menos una muestra de cada clase para 'stratify'
    if y.nunique() < 2:
        print("❌ Error: Se necesita al menos 2 clases diferentes en los datos para entrenar.")
        print("Juega partidas en diferentes niveles de dificultad (básico, intermedio, avanzado).")
        print("Juega partidas en diferentes niveles de dificultad o usa datos simulados.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Guardar el modelo
    joblib.dump(model, MODEL_PATH)

    print("\n✅ Modelo entrenado con datos reales y guardado en:", MODEL_PATH)
    print(f"\n✅ Modelo entrenado y guardado en: {MODEL_PATH}")
    
    # --- Reporte de predicciones ---
    y_pred = model.predict(X_test)
    
    resultados_df = data.loc[X_test.index].copy()
    resultados_df['nivel_predicho'] = y_pred
    resultados_df['prediccion_correcta'] = np.where(resultados_df['nivel_cognitivo'] == resultados_df['nivel_predicho'], '✔️ Correcta', '❌ Incorrecta')
    resultados_df['prediccion_correcta'] = np.where(resultados_df['nivel_cognitivo'] == resultados_df['nivel_predicho'], '✔️', '❌')

    print("\n--- 📋 Reporte Detallado de Predicciones (Datos Reales de Prueba) ---")
    print(resultados_df[[
        'nivel_dificultad', 
        'nivel_cognitivo', 
        'nivel_predicho', 
        'prediccion_correcta'
    ]].to_string(index=False))
    print("------------------------------------------------------------------\n")

    print("\n--- 📊 Reporte Técnico de Clasificación ---")
    print(classification_report(y_test, y_pred, zero_division=0))


def predecir_nivel(total_clicks, fallos, tiempo_reaccion_promedio):
    """
    Carga el modelo entrenado y predice el nivel cognitivo basado en las métricas de una partida.
    """
    if not os.path.exists(MODEL_PATH):
        print("El modelo no ha sido entrenado. Ejecutando entrenamiento...")
        entrenar_modelo()
        entrenar_modelo(usar_datos_simulados=True) # Entrenar con datos simulados si no existe
        if not os.path.exists(MODEL_PATH):
             raise FileNotFoundError("Falló el entrenamiento del modelo. Revisa los datos.")


    model = joblib.load(MODEL_PATH)
    X_pred = [[total_clicks, fallos, tiempo_reaccion_promedio]]
    return model.predict(X_pred)[0]

# Este bloque se ejecuta solo cuando corres el script directamente
if __name__ == "__main__":
    entrenar_modelo()
    # --- MODIFICADO: Llamar al entrenamiento con datos simulados ---
    entrenar_modelo(usar_datos_simulados=True)
    
    # Ejemplo de cómo usar la predicción después de entrenar
    if os.path.exists(MODEL_PATH):
        print("\n--- 🔮 Ejemplo de Predicción ---")
        # Simulemos una nueva partida
        clicks_partida = 30
        fallos_partida = 3
        reaccion_partida = 1.2
        
        nivel_predicho = predecir_nivel(clicks_partida, fallos_partida, reaccion_partida)
        print(f"Para una partida con {clicks_partida} clics, {fallos_partida} fallos y {reaccion_partida}s de reacción:")
        print(f"El nivel cognitivo predicho es: ✨ {nivel_predicho} ✨")

