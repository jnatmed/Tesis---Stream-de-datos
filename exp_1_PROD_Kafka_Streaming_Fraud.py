from kafka import KafkaProducer
import time
import json
import random

# Conexión al servidor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  # Asegúrate de que tu Kafka esté en este puerto
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialización de los datos en JSON
)

# Enviar datos cada 0.001 segundo
while True:
    dato = {
        "timestamp": time.time(),  # Hora en formato Unix
        "sensor_value": random.randint(1, 100)  # Valor aleatorio para simular datos
    }
    
    # Enviar el mensaje al tópico 'streaming-datos'
    producer.send('streaming-datos', dato)
    print(f"Mensaje enviado: {dato}")
    
    # Esperar 1 milisegundo antes de enviar el siguiente mensaje
    time.sleep(1)
