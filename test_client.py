import socket
import json

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect(("127.0.0.1", 8800))
    test_json = {
        "hello": "world"
    }
    client.sendall(json.dumps(test_json).encode("utf-8"))
    data = client.recv(1024)

print(f"Received {data!r}")