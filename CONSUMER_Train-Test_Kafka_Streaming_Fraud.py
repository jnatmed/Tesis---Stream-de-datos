from kafka import KafkaConsumer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_fscore_support
import json
import numpy as np

# Crea un consumidor
consumer = KafkaConsumer(
    'streaming-datos',  # Nombre del tópico
    bootstrap_servers='localhost:9092',  # Dirección de Kafka
    group_id='grupo-consumidor',  # ID de grupo de consumidores
    auto_offset_reset='earliest'  # Comienza a leer desde el primer mensaje disponible
)

# Inicializamos el vectorizador y el modelo
vectorizer = TfidfVectorizer(stop_words='english')
model = MultinomialNB()

# Variables para entrenamiento incremental y evaluación
X_train = []
y_train = []
predicciones = []
etiquetas_reales = []

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
            X_tfidf = vectorizer.fit_transform(X_train)
            model.fit(X_tfidf, y_train)
            print(f"Modelo entrenado con {len(X_train)} mensajes.")
    
    # Si es una opinión sin etiqueta, hacemos una predicción
    else:
        X_tfidf = vectorizer.transform([texto])
        prediccion = model.predict(X_tfidf)[0]
        predicciones.append(prediccion)
        
        # Almacenar las etiquetas reales para la evaluación
        # Aquí puedes tener un conjunto de pruebas con etiquetas reales
        etiquetas_reales.append('positivo')  # Etiqueta simulada para evaluación

        # Evaluar cuando tengamos suficientes predicciones
        if len(predicciones) == len(etiquetas_reales):
            precision, recall, f1, _ = precision_recall_fscore_support(
                etiquetas_reales, predicciones, average='binary', pos_label='positivo'
            )
            
            print(f"Precisión: {precision}")
            print(f"Recall: {recall}")
            print(f"F1-score: {f1}")
            break  # Terminamos después de evaluar el primer ciclo
