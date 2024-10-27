import csv
import grpc
import json
import service_pb2
import service_pb2_grpc

def enviar_compra_json(datos_compra):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.MyServiceStub(channel)
        
        mensaje_json = json.dumps(datos_compra)
        
        response = stub.SendMessage(service_pb2.MessageRequest(message=mensaje_json))
        print(f"Respuesta del servidor: {response.response}")

def leer_dataset_y_enviar_compras(archivo_csv, num_consultas=1000):
    with open(archivo_csv, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if i >= num_consultas:
                break

            datos_compra = {
                "nombre_producto": row['NombreProducto'],
                "precio": float(row['Precio']),
                "pasarela_pago": row['PasarelaPago'],
                "marca_tarjeta": row['MarcaTarjeta'],
                "banco": row['Banco'],
                "region": row['Region'],
                "direccion": row['Direccion'],
                "correo": row['Correo']
            }
            enviar_compra_json(datos_compra)

if __name__ == '__main__':
    leer_dataset_y_enviar_compras('compras_dataset.csv', num_consultas=1000)
