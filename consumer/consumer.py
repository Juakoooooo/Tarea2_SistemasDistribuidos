#Este apartado de código maneja las cargas y guarda las métricas

from confluent_kafka import Consumer
from elasticsearch import Elasticsearch
import json
import time
from datetime import datetime

consumer_conf = {
    'bootstrap.servers': 'localhost:9093',
    'group.id': 'grupo-consumidor1',
    'auto.offset.reset': 'earliest' 
}
consumer = Consumer(consumer_conf)
consumer.subscribe(['el-topico1'])

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def registrar_metrica(metrica, valor, compra_id):
    metric_data = {
        "timestamp": datetime.utcnow(),
        "metrica": metrica,
        "valor": valor,
        "compra_id": compra_id
    }
    es.index(index="metrics-index", document=metric_data)

def obtener_tiempo_espera(carga_trabajo):
    if carga_trabajo == "baja":
        return 1 
    elif carga_trabajo == "media":
        return 2  
    elif carga_trabajo == "alta":
        return 5  
    else:
        return 3  

carga_trabajo = "alta"  
tiempo_espera = obtener_tiempo_espera(carga_trabajo)

try:
    start_time = time.time()
    mensajes_procesados = 0

    while True:
        msg = consumer.poll(timeout=1.0) 
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        try:
            processing_start = time.time()
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

            es.index(index="compras-index", document=document)
            print(f"Mensaje recibido e indexado en Elasticsearch: {document}")

            latencia = time.time() - processing_start
            compra_id = msg.key().decode('utf-8')  
            registrar_metrica("latencia", latencia, compra_id)

            mensajes_procesados += 1
            elapsed_time = time.time() - start_time

            throughput = mensajes_procesados / elapsed_time
            registrar_metrica("throughput", throughput, compra_id)

            time.sleep(tiempo_espera)

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
finally:
    consumer.close()


#Este apartado de código realiza el procesamiento de los datos y envíos de correos

#from confluent_kafka import Consumer
#from elasticsearch import Elasticsearch
#import json
#import time
#import random
#import smtplib
#from email.mime.text import MIMEText
#
#consumer_conf = {
#    'bootstrap.servers': 'localhost:9093',
#    'group.id': 'grupo-consumidor1',
#    'auto.offset.reset': 'earliest'  
#}
#consumer = Consumer(consumer_conf)
#consumer.subscribe(['el-topico1'])
#
#es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
#
## Configuración del SMTP para enviar correos
#def enviar_correo(destinatario, estado, compra_id):
#    remitente = "doe933331@gmail.com"  # Tu correo
#    contraseña = "osqc ytkv ewpv yhiv"
#
#    msg = MIMEText(f"El pedido {compra_id} ha cambiado de estado a: {estado}")
#    msg['Subject'] = f'Actualización del estado del pedido {compra_id}: {estado}'
#    msg['From'] = remitente
#    msg['To'] = destinatario
#
#    try:
#        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#            server.login(remitente, contraseña)
#            server.sendmail(remitente, destinatario, msg.as_string())
#            print(f"Correo enviado: {estado} para el pedido {compra_id}")
#    except Exception as e:
#        print(f"Error enviando correo: {e}")
#
#def maquina_estados(compra_id, destinatario):
#    estados = {
#        "Procesando": "Preparación",
#        "Preparación": "Enviado",
#        "Enviado": "Entregado",
#        "Entregado": "Finalizado",
#        "Finalizado": None
#    }
#    
#    estado_actual = "Procesando"
#
#    while estado_actual is not None:
#        print(f"Compra {compra_id} - Estado actual: {estado_actual}")
#        enviar_correo(destinatario, estado_actual, compra_id)
#        
#        # Simular tiempo de procesamiento variable
#        tiempo_espera = random.randint(5, 10)
#        time.sleep(tiempo_espera)
#        
#        # Transición al siguiente estado
#        estado_actual = estados[estado_actual]
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
#        try:
#            message = json.loads(msg.value().decode('utf-8'))
#            document = {
#                "NombreProducto": message["nombre_producto"],
#                "Precio": float(message["precio"]),
#                "PasarelaPago": message["pasarela_pago"],
#                "MarcaTarjeta": message["marca_tarjeta"],
#                "Banco": message["banco"],
#                "Region": message["region"],
#                "Direccion": message["direccion"],
#                "Correo": message["correo"]
#            }
#
#            es.index(index="compras-index", document=document)
#            print(f"Mensaje recibido e indexado en Elasticsearch: {document}")
#
#            compra_id = msg.key().decode('utf-8')  # Utilizar la key como ID de la compra
#            destinatario = "doe933331@gmail.com"
#            maquina_estados(compra_id, destinatario)
#
#        except json.JSONDecodeError as e:
#            print(f"Error decodificando JSON: {e}")
#finally:
#    consumer.close()
#
#