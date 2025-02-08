Quiero entrenar un modelo para en un ambiente de streaming de datos, usando un servidor kafka
- para ello, instalo un servidor kafka version: 3.6.0, el mismo va a correr en el puerto 0.0.0.0:9092
- ahora quiero procesar por lotes datos en tiempo real desde kafka con River. 

```python
from kafka import KafkaConsumer
import json
from river import linear_model, preprocessing

# Inicializar el modelo
model = preprocessing.StandardScaler() | linear_model.LogisticRegression()

# Conectar a Kafka
consumer = KafkaConsumer(
    'transacciones',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Esperando transacciones en tiempo real...")

for message in consumer:
    transaction = message.value
    X = {"monto": transaction["monto"]}
    y = transaction["es_fraude"]

    # Predecimos
    prediction = model.predict_one(X)
    print(f"Transacción de {X['monto']}: Predicción = {prediction}")

    # Aprendemos del dato en tiempo real
    model.learn_one(X, y)
```

# Para correr Apache Kafka en windows 

1. Iniciar Zookeeper, ya que depende de Zookeeper. 

```powershell
PS c:\windows\system32> .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

2. Iniciar el servidor de Kafka
```powershell
PS c:\windows\system32> .\bin\windows\kafka-server-start.bat .\config\server.properties
```

