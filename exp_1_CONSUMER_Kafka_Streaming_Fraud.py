from kafka import KafkaConsumer

# Crea un consumidor
consumer = KafkaConsumer(
    'streaming-datos',  # Nombre del tópico
    bootstrap_servers='localhost:9092',  # Dirección de Kafka
    group_id='grupo-consumidor',  # ID de grupo de consumidores
    auto_offset_reset='earliest'  # Comienza a leer desde el primer mensaje disponible
)

# Lee los mensajes
for message in consumer:
    print(f"Mensaje recibido: {message.value}")
