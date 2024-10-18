from confluent_kafka import Producer
from uuid import uuid4

# Configura el Producer para conectarse a los brokers
producer_conf = {
    'bootstrap.servers': 'localhost:9093',
    'client.id': 'productor1'
}
producer = Producer(producer_conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Error al entregar mensaje: {err}")
    else:
        print(f"Mensaje enviado a {msg.topic()} [{msg.partition()}]")

# Función para producir mensaje
def produce_message(message):
    key = str(uuid4())
    print(f"Key: {key} Produciendo mensaje: {message}")
    producer.produce('el-topico1', key=key, value=message, callback=delivery_report)
    producer.poll(0)  # Procesa las colas del Producer
    producer.flush()  # Espera a que todos los mensajes pendientes sean entregados
