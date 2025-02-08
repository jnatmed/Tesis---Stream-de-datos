# Proyecto de Streaming y Entrenamiento en Tiempo Real con Kafka

Este proyecto consiste en un sistema de procesamiento de datos en tiempo real utilizando Kafka y un modelo de clasificación para predecir el sentimiento de mensajes. Los datos son procesados y el modelo se entrena de manera incremental utilizando el algoritmo Naive Bayes y sobremuestreo con SMOTE para abordar el desbalance de clases. Además, el sistema evalúa el modelo utilizando métricas de precisión, recall y F1-score.

## Requisitos

- Python 3.x
- Kafka
- Librerías de Python necesarias:
  - `kafka-python`
  - `sklearn`
  - `imblearn`
  - `joblib`
  - `json`
  
Puedes instalar las librerías necesarias utilizando `pip`:

```bash
pip install kafka-python scikit-learn imbalanced-learn joblib
```

# Instalacion de Kafka

## Para correr Apache Kafka en windows 

1. Iniciar Zookeeper, ya que depende de Zookeeper. 

```powershell
PS c:\windows\system32> .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

2. Iniciar el servidor de Kafka
```powershell
PS c:\windows\system32> .\bin\windows\kafka-server-start.bat .\config\server.properties
```

o si se prefiere, se pude ejecutar directamente 

```powershell
.\start-kafka.bat
```
Que tiene los comando antes mencionados para ejecutar zookeeper y kafka. 