#from confluent_kafka import Consumer
#from elasticsearch import Elasticsearch
#import json
#
## Configura el Consumer para conectarse a los brokers
#consumer_conf = {
#    'bootstrap.servers': 'localhost:9093',
#    'group.id': 'grupo-consumidor1',
#    'auto.offset.reset': 'earliest'  # Empieza desde el principio si no hay un offset guardado
#}
#consumer = Consumer(consumer_conf)
#consumer.subscribe(['el-topico1'])
#
## Configura la conexión a Elasticsearch
#es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
#
#try:
#    while True:
#        msg = consumer.poll(timeout=1.0)  # Espera 1 segundo por mensajes
#        if msg is None:
#            continue
#        if msg.error():
#            print(f"Consumer error: {msg.error()}")
#            continue
#        
#        # Deserializamos el mensaje y lo indexamos en Elasticsearch
#        message = json.loads(msg.value().decode('utf-8'))
#        document = {
#            "NombreProducto": message["nombre_producto"],
#            "Precio": float(message["precio"]),
#            "PasarelaPago": message["pasarela_pago"],
#            "MarcaTarjeta": message["marca_tarjeta"],
#            "Banco": message["banco"],
#            "Region": message["region"],
#            "Direccion": message["direccion"],
#            "Correo": message["correo"]
#        }
#
#        # Indexamos el documento en Elasticsearch con un índice específico
#        es.index(index="compras-index", document=document)
#        print(f"Mensaje recibido e indexado en Elasticsearch: {document}")
#finally:
#    consumer.close()

from confluent_kafka import Consumer
from elasticsearch import Elasticsearch
import json
import time
import random
import smtplib
from email.mime.text import MIMEText

# Configura el Consumer para conectarse a los brokers
consumer_conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'grupo-consumidor1',
    'auto.offset.reset': 'earliest'  # Empieza desde el principio si no hay un offset guardado
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['el-topico1'])

# Configura la conexión a Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Configuración del SMTP para enviar correos
def enviar_correo(destinatario, estado, compra_id):
    remitente = "doe933331@gmail.com"  # Tu correo
    contraseña = "osqc ytkv ewpv yhiv"

    msg = MIMEText(f"El pedido {compra_id} ha cambiado de estado a: {estado}")
    msg['Subject'] = f'Actualización del estado del pedido {compra_id}: {estado}'
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(remitente, contraseña)
            server.sendmail(remitente, destinatario, msg.as_string())
            print(f"Correo enviado: {estado} para el pedido {compra_id}")
    except Exception as e:
        print(f"Error enviando correo: {e}")

# Máquina de estados con un diccionario
def maquina_estados(compra_id, destinatario):
    estados = {
        "Procesando": "Preparación",
        "Preparación": "Enviado",
        "Enviado": "Entregado",
        "Entregado": "Finalizado",
        "Finalizado": None
    }
    
    estado_actual = "Procesando"

    while estado_actual is not None:
        print(f"Compra {compra_id} - Estado actual: {estado_actual}")
        enviar_correo(destinatario, estado_actual, compra_id)
        
        # Simular tiempo de procesamiento variable
        tiempo_espera = random.randint(5, 10)
        time.sleep(tiempo_espera)
        
        # Transición al siguiente estado
        estado_actual = estados[estado_actual]

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Espera 1 segundo por mensajes
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        # Deserializamos el mensaje y lo indexamos en Elasticsearch
        try:
            message = json.loads(msg.value().decode('utf-8'))
            document = {
                "NombreProducto": message["nombre_producto"],
                "Precio": float(message["precio"]),
                "PasarelaPago": message["pasarela_pago"],
                "MarcaTarjeta": message["marca_tarjeta"],
                "Banco": message["banco"],
                "Region": message["region"],
                "Direccion": message["direccion"],
                "Correo": message["correo"]
            }

            # Indexamos el documento en Elasticsearch con un índice específico
            es.index(index="compras-index", document=document)
            print(f"Mensaje recibido e indexado en Elasticsearch: {document}")

            # Ejecutar la máquina de estados para la compra recibida
            compra_id = msg.key().decode('utf-8')  # Utilizar la key como ID de la compra
            destinatario = "doe933331@gmail.com"
            maquina_estados(compra_id, destinatario)

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
finally:
    consumer.close()

