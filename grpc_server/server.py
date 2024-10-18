from concurrent import futures
import grpc
import service_pb2_grpc
import service_pb2
from producer import produce_message  # Importa la función del producer.py

# Implementa el servicio gRPC
class MyService(service_pb2_grpc.MyServiceServicer):
    def SendMessage(self, request, context):
        # Envía el mensaje recibido al productor Kafka
        print(f"Recibido mensaje gRPC: {request.message}")
        produce_message(request.message)  # Aquí llamas al producer de Kafka
        return service_pb2.MessageResponse(response="Mensaje enviado a Kafka")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')  # Asegura que escuche en el puerto 50051
    server.start()
    print("gRPC server corriendo en localhost:50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
