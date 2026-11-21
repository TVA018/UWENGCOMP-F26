import json
import socket
from schema import InputPayload

def generate_test_data_for_hour() -> InputPayload:
    pass

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 8800))
    server.listen()

    while True:
        (clientsocket, address) = server.accept()
        with clientsocket:
            print(f"Connected by {address}")
            while True:
                hour_info: InputPayload = generate_test_data_for_hour() # Generate test data to store in this dictionary
                clientsocket.sendall(json.dumps(hour_info).encode("utf-8"))