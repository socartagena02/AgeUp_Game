import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import plot_tree

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'modelo_cognitivo.pkl')
DATA_PATH = os.path.join(BASE_DIR, '..', '..', 'memorice', 'memorice_data.csv')
# Nueva ruta para guardar gráficos
GRAPHICS_DIR = os.path.join(BASE_DIR, 'graficos_modelo')
os.makedirs(GRAPHICS_DIR, exist_ok=True)

label_encoder = None

def generar_datos_simulados(n_samples=150):

    np.random.seed(42)
    
    clicks_leve = np.random.randint(20, 40, n_samples // 3)
    fallos_leve = np.random.randint(1, 5, n_samples // 3)
    reaccion_leve = np.random.uniform(0.8, 1.5, n_samples // 3)

    clicks_moderado = np.random.randint(35, 60, n_samples // 3)
    fallos_moderado = np.random.randint(4, 10, n_samples // 3)
    reaccion_moderado = np.random.uniform(1.4, 2.2, n_samples // 3)

    clicks_avanzado = np.random.randint(55, 90, n_samples - 2 * (n_samples // 3))
    fallos_avanzado = np.random.randint(8, 20, n_samples - 2 * (n_samples // 3))
    reaccion_avanzado = np.random.uniform(2.0, 3.5, n_samples - 2 * (n_samples // 3))

    data = pd.DataFrame({
        'total_clicks': np.concatenate([clicks_leve, clicks_moderado, clicks_avanzado]),
        'fallos': np.concatenate([fallos_leve, fallos_moderado, fallos_avanzado]),
        'tiempo_reaccion_promedio': np.concatenate([reaccion_leve, reaccion_moderado, reaccion_avanzado]),
        'nivel_cognitivo': ['Leve'] * (n_samples // 3) + ['Moderado'] * (n_samples // 3) + ['Avanzado'] * (n_samples - 2 * (n_samples // 3)),
    })
   
    data['nivel_dificultad'] = data['nivel_cognitivo'].str.lower()
    
    return data

def analisis_exploratorio_datos(data, tiene_nivel_cognitivo=True):

    print("\n" + "="*60)
    print("📊 ANÁLISIS EXPLORATORIO DE DATOS")
    print("="*60)

    print("\n📋 Información del dataset:")
    print(f"• Total de muestras: {len(data)}")
    print(f"• Total de características: {len(data.columns)}")
    print(f"• Columnas disponibles: {list(data.columns)}")

    print("\n📈 Estadísticas descriptivas (columnas numéricas):")
    numeric_data = data.select_dtypes(include=[np.number])
    if not numeric_data.empty:
        print(numeric_data.describe().round(2))
    else:
        print("No hay columnas numéricas en los datos.")

    if tiene_nivel_cognitivo and 'nivel_cognitivo' in data.columns:

        print("\n🎯 Distribución de niveles cognitivos:")
        distribucion = data['nivel_cognitivo'].value_counts()
        print(distribucion)

        if len(distribucion) > 1:
            print(f"\n⚖️ Balance de clases: {distribucion.min() / distribucion.max():.2%}")

    print("\n🔍 Valores nulos por columna:")
    print(data.isnull().sum())

def map_dificultad_a_cognitivo(df):

    print(f"\n🔍 Columnas disponibles en los datos: {list(df.columns)}")
    
    if 'nivel_cognitivo' in df.columns:
        print("✅ Ya existe la columna 'nivel_cognitivo' en los datos.")
        return df

    if 'nivel_dificultad' in df.columns:
        print("🔄 Mapeando 'nivel_dificultad' a 'nivel_cognitivo'...")
        mapeo = {
            'basico': 'Leve',
            'intermedio': 'Moderado',
            'avanzado': 'Avanzado',
            'básico': 'Leve',  
            'Básico': 'Leve',
            'Intermedio': 'Moderado',
            'Avanzado': 'Avanzado'
        }
        
        df['nivel_cognitivo'] = df['nivel_dificultad'].map(mapeo)
        
        print(f"Valores únicos en 'nivel_dificultad': {df['nivel_dificultad'].unique()}")
        print(f"Valores únicos en 'nivel_cognitivo' después del mapeo: {df['nivel_cognitivo'].unique()}")
        
        filas_antes = len(df)
        df.dropna(subset=['nivel_cognitivo'], inplace=True)
        filas_despues = len(df)
        
        if filas_antes != filas_despues:
            print(f"⚠️ Se eliminaron {filas_antes - filas_despues} filas con dificultad no reconocida.")
    else:
        print("⚠️ No se encontró 'nivel_dificultad' en los datos.")
        print("Creando niveles cognitivos basados en el rendimiento...")
        
        df['puntaje'] = (
            (df['total_clicks'] - df['total_clicks'].min()) / (df['total_clicks'].max() - df['total_clicks'].min()) * 0.4 +
            (df['fallos'].max() - df['fallos']) / (df['fallos'].max() - df['fallos'].min()) * 0.3 +
            (df['tiempo_reaccion_promedio'].max() - df['tiempo_reaccion_promedio']) / 
            (df['tiempo_reaccion_promedio'].max() - df['tiempo_reaccion_promedio'].min()) * 0.3
        )
        
        # Asignar niveles basados en percentiles
        df['percentil'] = df['puntaje'].rank(pct=True)
        condiciones = [
            df['percentil'] <= 0.33,
            (df['percentil'] > 0.33) & (df['percentil'] <= 0.66),
            df['percentil'] > 0.66
        ]
        opciones = ['Avanzado', 'Moderado', 'Leve']
        
        df['nivel_cognitivo'] = np.select(condiciones, opciones, default='Moderado')
        print(f"Niveles creados: {df['nivel_cognitivo'].value_counts().to_dict()}")
    
        df.drop(['puntaje', 'percentil'], axis=1, inplace=True)
    
    return df

def preprocesar_datos(data):
   
    print("\n" + "="*60)
    print("⚙️ PREPROCESAMIENTO DE DATOS")
    print("="*60)
    
    if 'nivel_cognitivo' not in data.columns:
        print("⚠️ No se encontró 'nivel_cognitivo'. Aplicando mapeo...")
        data = map_dificultad_a_cognitivo(data)

    if data.isnull().sum().sum() > 0:
        print("⚠️ Se encontraron valores nulos. Rellenando con la mediana...")
        for col in data.select_dtypes(include=[np.number]).columns:
            data[col] = data[col].fillna(data[col].median())
 
    le = LabelEncoder()
    data['nivel_cognitivo_encoded'] = le.fit_transform(data['nivel_cognitivo'])
    mapping = dict(zip(le.classes_, range(len(le.classes_))))
    print(f"🔤 Codificación de clases: {mapping}")
   
    columnas_requeridas = ['total_clicks', 'fallos', 'tiempo_reaccion_promedio']
    for col in columnas_requeridas:
        if col not in data.columns:
            print(f"⚠️ Advertencia: Columna '{col}' no encontrada. Verifica los datos.")
    
    return data, le

def evaluar_modelo(model, X_train, y_train, X_test, y_test, le):
    print("\n" + "="*60)
    print("📊 EVALUACIÓN DEL MODELO")
    print("="*60)
    
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Métricas
    train_accuracy = accuracy_score(y_train, y_pred_train)
    test_accuracy = accuracy_score(y_test, y_pred_test)
    
    print(f"📈 Exactitud en entrenamiento: {train_accuracy:.2%}")
    print(f"📉 Exactitud en prueba: {test_accuracy:.2%}")
    print(f"📊 Diferencia: {abs(train_accuracy - test_accuracy):.2%}")
    
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"🔄 Validación cruzada (5-fold): {cv_scores.mean():.2%} (+/- {cv_scores.std() * 2:.2%})")

    print("\n📋 Reporte de clasificación (conjunto de prueba):")
    print(classification_report(y_test, y_pred_test, target_names=le.classes_))

def crear_graficos_random_forest(model, X_train, y_train, X_test, y_test, feature_names, le):
    
    print("\n" + "="*60)
    print("🌳 GRÁFICOS DEL MODELO RANDOM FOREST")
    print("="*60)
    
    # Predicciones 
    y_pred = model.predict(X_test)

    plt.figure(figsize=(10, 6))
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    bars = plt.bar(range(len(importances)), importances[indices], align='center', color='skyblue', edgecolor='black')

    for bar, importance in zip(bars, importances[indices]):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{importance:.3f}', ha='center', va='bottom')
    
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
    plt.xlabel('Características')
    plt.ylabel('Importancia')
    plt.title('Importancia de Características - Random Forest')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHICS_DIR, 'importancia_caracteristicas.png'), dpi=300)
    print("✅ Gráfico de importancia de características guardado")
    plt.show()

    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=le.classes_, 
                yticklabels=le.classes_,
                cbar_kws={'label': 'Cantidad de muestras'})
    plt.title('Matriz de Confusión')
    plt.ylabel('Etiqueta Real')
    plt.xlabel('Etiqueta Predicha')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHICS_DIR, 'matriz_confusion.png'), dpi=300)
    print("✅ Matriz de confusión guardada")
    plt.show()
 
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    real_counts = pd.Series(y_test).value_counts().sort_index()
    bars_real = plt.bar(range(len(real_counts)), real_counts.values, alpha=0.7, 
                       color='green', edgecolor='black')
    plt.xticks(range(len(real_counts)), le.classes_, rotation=45)
    plt.title('Distribución Real de Clases')
    plt.ylabel('Frecuencia')
    for bar, count in zip(bars_real, real_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom')
    
    plt.subplot(1, 2, 2)
    pred_counts = pd.Series(y_pred).value_counts().sort_index()
    bars_pred = plt.bar(range(len(pred_counts)), pred_counts.values, alpha=0.7, 
                       color='orange', edgecolor='black')
    plt.xticks(range(len(pred_counts)), le.classes_, rotation=45)
    plt.title('Distribución Predicha de Clases')
    plt.ylabel('Frecuencia')
    for bar, count in zip(bars_pred, pred_counts.values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom')
    
    plt.suptitle('Comparación: Valores Reales vs Predichos')
    plt.tight_layout()
    plt.savefig(os.path.join(GRAPHICS_DIR, 'distribucion_predicciones.png'), dpi=300)
    print("✅ Gráfico de distribución de predicciones guardado")
    plt.show()
    try:
        plt.figure(figsize=(20, 10))
        plot_tree(model.estimators_[0], 
                  feature_names=feature_names,
                  class_names=le.classes_,
                  filled=True, 
                  rounded=True,
                  max_depth=2,  # Limitamos aún más para mejor visualización
                  fontsize=10)
        plt.title('Ejemplo de Árbol de Decisión (primer árbol del Random Forest)')
        plt.tight_layout()
        plt.savefig(os.path.join(GRAPHICS_DIR, 'arbol_decision.png'), dpi=300, bbox_inches='tight')
        print("✅ Gráfico de árbol de decisión guardado")
        plt.show()
    except Exception as e:
        print(f"⚠️ No se pudo generar el gráfico del árbol: {str(e)}")
        print("Generando gráfico simplificado...")
        
        # Gráfico alternativo: scores por clase
        plt.figure(figsize=(10, 6))
        class_names = le.classes_
        
        # Obtener probabilidades por clase
        y_proba = model.predict_proba(X_test)
        
        plt.boxplot([y_proba[:, i] for i in range(len(class_names))])
        plt.xticks(range(1, len(class_names) + 1), class_names)
        plt.title('Distribución de Probabilidades por Clase')
        plt.ylabel('Probabilidad')
        plt.xlabel('Clase')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(GRAPHICS_DIR, 'probabilidades_clases.png'), dpi=300)
        print("✅ Gráfico de probabilidades por clase guardado")
        plt.show()

def entrenar_modelo(usar_datos_simulados=False):
    global label_encoder  
    
    print("\n" + "="*60)
    print("🚀 ENTRENAMIENTO DEL MODELO DE CLASIFICACIÓN")
    print("="*60)
    
    if usar_datos_simulados:
        print("🔥 Usando datos simulados para el entrenamiento.")
        data = generar_datos_simulados(n_samples=150)
    else:
        print("📦 Usando datos reales desde `memorice_data.csv`.")
        if not os.path.exists(DATA_PATH):
            print(f"⚠️ No se encontró el archivo de datos en '{DATA_PATH}'.")
            print("🔧 Usando datos simulados en su lugar...")
            data = generar_datos_simulados(n_samples=150)
        else:
            try:
                data = pd.read_csv(DATA_PATH)
                print(f"✅ Datos cargados: {len(data)} filas, {len(data.columns)} columnas")
                
                print("\n🔍 Primeras 5 filas del dataset:")
                print(data.head())
                
            except Exception as e:
                print(f"❌ Error al leer el archivo CSV: {str(e)}")
                print("🔧 Usando datos simulados en su lugar...")
                data = generar_datos_simulados(n_samples=150)
    
    # 1. Análisis exploratorio
    tiene_nivel_cognitivo = 'nivel_cognitivo' in data.columns
    analisis_exploratorio_datos(data, tiene_nivel_cognitivo)
    
    # 2. Preprocesamiento 
    data, label_encoder = preprocesar_datos(data)
    
    # 3. Preparación de características
    columnas_disponibles = data.columns.tolist()
    print(f"\n🔍 Columnas disponibles después del preprocesamiento: {columnas_disponibles}")

    columnas_candidatas = ['total_clicks', 'fallos', 'tiempo_reaccion_promedio']
    columnas_finales = [col for col in columnas_candidatas if col in data.columns]
    
    if not columnas_finales:
        raise ValueError("❌ No se encontraron columnas numéricas para entrenar el modelo.")
    
    print(f"📊 Usando las siguientes características: {columnas_finales}")
    
    X = data[columnas_finales]
    y = data['nivel_cognitivo_encoded']
    
    print(f"\n🎯 Variable objetivo transformada:")
    print(f"• Valores únicos: {np.unique(y)}")
    print(f"• Distribución: {pd.Series(y).value_counts().to_dict()}")
    print(f"• Clases originales: {label_encoder.classes_}")
    
    # 4. División de datos
    if len(np.unique(y)) < 2:
        print("❌ Error: Se necesita al menos 2 clases diferentes en los datos.")
        print("🔧 Agregando datos simulados para crear más clases...")
        data_simulada = generar_datos_simulados(n_samples=50)
        data = pd.concat([data, data_simulada], ignore_index=True)
        data, label_encoder = preprocesar_datos(data)
        X = data[columnas_finales]
        y = data['nivel_cognitivo_encoded']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    
    print(f"\n📊 División de datos:")
    print(f"• Entrenamiento: {len(X_train)} muestras ({len(X_train)/len(data):.1%})")
    print(f"• Prueba: {len(X_test)} muestras ({len(X_test)/len(data):.1%})")

    print("\n" + "="*60)
    print("🌳 ENTRENANDO RANDOM FOREST CLASSIFIER")
    print("="*60)
    
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)

    evaluar_modelo(model, X_train, y_train, X_test, y_test, label_encoder)

    crear_graficos_random_forest(model, X_train, y_train, X_test, y_test, 
                                columnas_finales, label_encoder)

    model_data = {
        'model': model,
        'label_encoder': label_encoder,
        'feature_names': columnas_finales,
        'data_info': {
            'samples': len(data),
            'features': columnas_finales,
            'classes': list(label_encoder.classes_),
            'class_distribution': data['nivel_cognitivo'].value_counts().to_dict()
        }
    }
    
    joblib.dump(model_data, MODEL_PATH)
    
    print(f"\n✅ Modelo entrenado y guardado en: {MODEL_PATH}")
    print(f"✅ Gráficos guardados en: {GRAPHICS_DIR}")
    print(f"✅ Clases reconocidas: {list(label_encoder.classes_)}")
    
    return model

def predecir_nivel(total_clicks, fallos, tiempo_reaccion_promedio):
 
    global label_encoder
    
    if not os.path.exists(MODEL_PATH):
        print("El modelo no ha sido entrenado. Ejecutando entrenamiento...")
        model = entrenar_modelo(usar_datos_simulados=True)
        if model is None:
            raise ValueError("No se pudo entrenar el modelo.")
    
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    label_encoder = model_data['label_encoder']
    feature_names = model_data['feature_names']

    X_pred = []
    for feature in feature_names:
        if feature == 'total_clicks':
            X_pred.append(total_clicks)
        elif feature == 'fallos':
            X_pred.append(fallos)
        elif feature == 'tiempo_reaccion_promedio':
            X_pred.append(tiempo_reaccion_promedio)
    
    X_pred = [X_pred] 
    
    encoded_pred = model.predict(X_pred)[0]
    nivel_predicho = label_encoder.inverse_transform([encoded_pred])[0]
    
    return nivel_predicho

def main():
 
    try:
        print("🧠 INICIO DEL SISTEMA DE CLASIFICACIÓN COGNITIVA")
        print("="*60)
        usar_simulados = True  
        
        if os.path.exists(DATA_PATH):
            try:
                data_real = pd.read_csv(DATA_PATH)
                if len(data_real) > 5:  
                    print(f"\n📊 Se encontraron {len(data_real)} filas de datos reales.")
                    respuesta = input("¿Quieres usar datos reales? (s/n): ").lower()
                    if respuesta == 's':
                        usar_simulados = False
            except:
                pass

        model = entrenar_modelo(usar_datos_simulados=usar_simulados)
        
        if model is not None:
            print("\n" + "="*60)
            print("🔮 EJEMPLO DE PREDICCIÓN")
            print("="*60)
            
            casos_prueba = [
                (30, 3, 1.2, "Leve (esperado)"),
                (45, 7, 1.8, "Moderado (esperado)"),
                (70, 15, 2.8, "Avanzado (esperado)")
            ]
            
            for clicks, fallos, tiempo, esperado in casos_prueba:
                try:
                    nivel = predecir_nivel(clicks, fallos, tiempo)
                    print(f"\n📊 Partida: {clicks} clics, {fallos} fallos, {tiempo}s")
                    print(f"   → Predicción: {nivel}")
                    print(f"   → {esperado}")
                except Exception as e:
                    print(f"\n❌ Error en predicción: {str(e)}")
            
            print("\n" + "="*60)
            print("✅ PROCESO COMPLETADO EXITOSAMENTE")
            print("="*60)
            print(f"\n📁 Modelo guardado en: {MODEL_PATH}")
            print(f"📁 Gráficos guardados en: {GRAPHICS_DIR}")
            
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n💡 SUGERENCIA: Verifica que tu archivo CSV tenga las columnas necesarias:")
        print("   - total_clicks")
        print("   - fallos") 
        print("   - tiempo_reaccion_promedio")
        print("   - nivel_dificultad (opcional, pero recomendado)")

if __name__ == "__main__":
    main()