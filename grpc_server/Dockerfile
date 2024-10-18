# Usamos la imagen slim de Python 3.8
FROM python:3.8-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY server.py .
COPY producer.py . 
COPY service.proto .

# Instala las dependencias necesarias para gRPC y confluent_kafka
RUN pip install grpcio grpcio-tools confluent_kafka

# Genera los archivos Python desde el archivo .proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

# Comando por defecto para correr el servidor gRPC
CMD ["python", "server.py"]
