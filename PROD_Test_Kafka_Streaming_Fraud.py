from kafka import KafkaProducer
import json
import time

# Crea un productor
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializa el mensaje como JSON
)

# Ejemplo de opiniones sin etiquetas
opiniones_sin_etiqueta = [
    "Me encanta este producto", 
    "Muy malo, no lo recomiendo",
    "El servicio fue excelente",
    "No lo volvería a comprar",
    "La experiencia fue fantástica",
    "No sirve para nada",
]

# Enviar opiniones sin etiquetas de sentimiento
for i in range(1000):  # Enviar 1000 opiniones
    opinion = opiniones_sin_etiqueta[i % len(opiniones_sin_etiqueta)]  # Ciclo de ejemplo de opiniones
    
    mensaje = {
        'id': i,
        'texto': opinion,
    }
    
    producer.send('streaming-datos', mensaje)
    print(f"Enviado: {mensaje['texto']}")
    
    # Hacemos flush para asegurarnos que el mensaje se envíe
    producer.flush()

    time.sleep(0.001)  # Intervalo de 0.001 segundos entre cada mensaje
