from typing import Any, Dict, Tuple
import socket
import struct
import json


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        self.socket.connect(self.address)

    def close(self) -> None:
        self.socket.close()

    def execute(self, command: str, *args: Tuple, **kwargs: Dict) -> Any:
        request = {}
        request["command"] = command
        request["args"] = list(args)
        request["kwargs"] = kwargs
        request = json.dumps(request)

        self.socket.send(struct.pack(">I", len(request)) + request.encode("utf-8"))

        size = self.socket.recv(4)
        size = struct.unpack(">I", size)[0]
        response = self.socket.recv(size).decode("utf-8")
        response = json.loads(response)

        if response["code"]:
            return response["result"]
        else:
            raise Exception(response["error"])
