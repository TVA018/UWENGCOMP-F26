from schema import InputPayload, ReturnPayload
import socket
import socketconfig
import json

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((socketconfig.HOST, socketconfig.PORT))

        # RECEIVING PAYLOAD FROM SOCKET
        payloads_str = ""
        data = client.recv(5)

        while data:
            payloads_str += data.decode("utf-8")
            data = client.recv(5)

        payloads = [json.loads(payload) for payload in payloads_str.replace("}{", "}|,|{").split("|,|")]

        # SEND CORRESPONDING PAYLOAD

if __name__ == "__main__":
    run_client()