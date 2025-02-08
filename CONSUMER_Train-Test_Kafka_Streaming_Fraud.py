from kafka import KafkaConsumer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_fscore_support
from imblearn.over_sampling import SMOTE  # Importamos SMOTE
import json
import joblib  # Para guardar y cargar el modelo entrenado
import os

# Función para cargar las etiquetas reales desde un archivo
def cargar_etiquetas():
    if os.path.exists('etiquetas_reales.json'):
        with open('etiquetas_reales.json', 'r') as file:
            etiquetas = json.load(file)
        return etiquetas
    else:
        return []

# Función para guardar las etiquetas reales en un archivo
def guardar_etiquetas(etiquetas):
    with open('etiquetas_reales.json', 'w') as file:
        json.dump(etiquetas, file)

# Crea un consumidor
consumer = KafkaConsumer(
    'streaming-datos',  # Nombre del tópico
    bootstrap_servers='localhost:9092',  # Dirección de Kafka
    group_id='grupo-consumidor',  # ID de grupo de consumidores
    auto_offset_reset='earliest'  # Comienza a leer desde el primer mensaje disponible
)

# Inicializamos el vectorizador y el modelo
vectorizer = TfidfVectorizer(stop_words='english')

# Intentamos cargar el modelo entrenado previamente
try:
    model = joblib.load('modelo_entrenado.pkl')  # Intentamos cargar el modelo existente
    print("Modelo cargado exitosamente.")
except:
    model = MultinomialNB()
    print("No se encontró modelo previo. Se creará uno nuevo.")

# Inicializamos SMOTE para el sobremuestreo
smote = SMOTE(random_state=42, k_neighbors=3)  

# Variables para entrenamiento incremental y evaluación
X_train = []
y_train = []
predicciones = []
etiquetas_reales = cargar_etiquetas()  # Cargamos las etiquetas reales desde el archivo
evaluation_interval = 100  # Evaluar después de procesar 100 opiniones

# Lee los mensajes
for message in consumer:
    # Deserializamos el mensaje recibido
    mensaje = json.loads(message.value.decode('utf-8'))
    texto = mensaje['texto']
    
    # Si el mensaje tiene una etiqueta (de entrenamiento)
    if 'sentimiento' in mensaje:
        sentimiento = mensaje['sentimiento']
        X_train.append(texto)
        y_train.append(sentimiento)

        # Entrenamiento incremental
        if len(X_train) > 10:  # Entrenamos cuando tenemos suficientes datos
            # Ajustamos el vectorizador solo una vez con los datos de entrenamiento
            X_tfidf = vectorizer.fit_transform(X_train)
            
            # Convertir las etiquetas en binario (positivo = 1, negativo = 0)
            y_train_bin = [1 if s == 'positivo' else 0 for s in y_train]
            
            # Sobremuestreo con SMOTE en las características de texto
            X_resampled, y_resampled = smote.fit_resample(X_tfidf.toarray(), y_train_bin)  # Convertimos a denso
            
            # Entrenar el modelo con los datos sobremuestreados
            model.fit(X_resampled, y_resampled)
            print(f"Modelo entrenado con {len(X_train)} mensajes.")
            joblib.dump(model, 'modelo_entrenado.pkl')  # Guardamos el modelo entrenado

        # Guardar las primeras 500 etiquetas reales
        if len(etiquetas_reales) < 500:
            etiquetas_reales.append(sentimiento)  # Guardamos la etiqueta real
            guardar_etiquetas(etiquetas_reales)  # Guardamos las etiquetas en el archivo

    # Si es una opinión sin etiqueta, hacemos una predicción
    else:
        # Aquí usamos el vectorizador ya ajustado con los datos anteriores
        if len(X_train) > 0:  # Solo transformamos si el vectorizador ha sido ajustado
            X_tfidf = vectorizer.transform([texto])
            prediccion = model.predict(X_tfidf)[0]
            predicciones.append(prediccion)
        
            # Evaluar cada cierto número de opiniones procesadas
            if len(predicciones) >= evaluation_interval:
                # Si ya tenemos 500 etiquetas, las cargamos para la evaluación
                if len(etiquetas_reales) >= 100:  # Asegurarnos de que ya tenemos al menos 100 etiquetas
                    # Convertir etiquetas reales a valores numéricos (1 para 'positivo', 0 para 'negativo')
                    etiquetas_reales_bin = [1 if etiqueta == 'positivo' else 0 for etiqueta in etiquetas_reales[:100]]
                    
                    precision, recall, f1, _ = precision_recall_fscore_support(
                        etiquetas_reales_bin, predicciones, average='binary', pos_label=1  # Usar 1 como etiqueta positiva
                    )
                    print(f"Precisión: {precision}")
                    print(f"Recall: {recall}")
                    print(f"F1-score: {f1}")
                
                # Resetear predicciones para la próxima evaluación
                predicciones = []

