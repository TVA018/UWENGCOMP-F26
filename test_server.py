import json
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 8800))
    server.listen()

    while True:
        (clientsocket, address) = server.accept()
        with clientsocket:
            print(f"Connected by {address}")
            while True:
                data = clientsocket.recv(1024)
                data_str = data.decode("utf-8")
                data_dict = json.loads(data_str)
                print(f"Data received from client: {data_str}")
                data_dict["from_server"] = "Matthew is the goat"
                if not data:
                    break
                clientsocket.sendall(json.dumps(data_dict).encode("utf-8"))