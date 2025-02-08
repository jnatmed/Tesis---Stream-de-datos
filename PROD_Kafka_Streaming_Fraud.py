from kafka import KafkaProducer
import json
import time

# Crea un productor
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializa el mensaje como JSON
)

# Ejemplo de mensajes con etiquetas de sentimiento
sentimientos = ['positivo', 'negativo']
textos = [
    "Este producto es excelente",  # Positivo
    "Muy malo, no lo recomiendo",  # Negativo
    "El mejor producto que he comprado",  # Positivo
    "No sirve para nada",  # Negativo
    "Me encanta este artículo",  # Positivo
    "Totalmente decepcionado con la compra",  # Negativo
]

# Enviar mensajes con etiquetas de sentimiento
for i in range(1000):  # Aquí puedes enviar más mensajes si quieres
    texto = textos[i % len(textos)]  # Ciclo de ejemplo de textos
    sentimiento = sentimientos[i % len(sentimientos)]  # Etiqueta alternada para el ejemplo
    
    mensaje = {
        'id': i,
        'texto': texto,
        'sentimiento': sentimiento  # Etiqueta de sentimiento
    }
    
    producer.send('streaming-datos', mensaje)
    print(f"Enviado: {mensaje['texto']} | Sentimiento: {mensaje['sentimiento']}")
    time.sleep(0.001)  # Intervalo de 0.001 segundos entre cada mensaje
