FROM python:3.8-slim
WORKDIR /app
COPY client.py .
COPY service.proto .
RUN pip install grpcio grpcio-tools
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto
CMD ["python", "client.py"]
