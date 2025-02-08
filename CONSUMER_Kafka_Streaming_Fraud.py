from kafka import KafkaConsumer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import json

# Crea un consumidor
consumer = KafkaConsumer(
    'streaming-datos',  # Nombre del tópico
    bootstrap_servers='localhost:9092',  # Dirección de Kafka
    group_id='grupo-consumidor',  # ID de grupo de consumidores
    auto_offset_reset='earliest'  # Comienza a leer desde el primer mensaje disponible
)

# Inicializamos el modelo y el vectorizador
vectorizer = TfidfVectorizer(stop_words='english')
model = MultinomialNB()

# Variables para entrenamiento incremental
X_train = []
y_train = []

# Lee los mensajes
for message in consumer:
    # Deserializamos el mensaje recibido
    mensaje = json.loads(message.value.decode('utf-8'))
    texto = mensaje['texto']
    sentimiento = mensaje['sentimiento']  # Aquí obtenemos la etiqueta de sentimiento
    
    # Agregar el texto y la etiqueta a los datos de entrenamiento
    X_train.append(texto)
    y_train.append(sentimiento)

    # Entrenamiento incremental (usamos un modelo simple de Naive Bayes)
    if len(X_train) > 10:  # Entrenamos cuando tenemos suficientes datos
        X_tfidf = vectorizer.fit_transform(X_train)
        model.fit(X_tfidf, y_train)
        print(f"Modelo entrenado con {len(X_train)} mensajes.")
    
    # Aquí podrías agregar lógica adicional para predecir el sentimiento de nuevos mensajes
    # o realizar acciones de evaluación en el modelo.
