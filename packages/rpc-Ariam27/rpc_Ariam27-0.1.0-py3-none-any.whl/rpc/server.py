from typing import Callable
import socket
import select
import struct
import json


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.address = (self.host, self.port)
        self.registered = {}
        self.clients = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, timeout: int = 3) -> None:
        self.socket.bind(self.address)
        self.socket.listen()

        while True:
            while True:
                accept, __, _ = select.select([self.socket], [], [], timeout)
                if not len(accept):
                    break
                conn, addr = self.socket.accept()
                self.clients.append(conn)

            read, write, _ = select.select(self.clients, self.clients, [], timeout)
            if len(read):
                for sock in read:
                    if sock in write:
                        size = sock.recv(4)
                        if len(size) == 4:
                            size = struct.unpack(">I", size)[0]
                            request = json.loads(sock.recv(size).decode("utf-8"))

                            response = {}

                            if request["command"] == "/":
                                response["code"] = 1
                                response["result"] = list(self.registered.keys())
                            elif request["command"] in self.registered.keys():
                                try:
                                    result = self.registered[request["command"]](
                                        *request["args"], **request["kwargs"]
                                    )
                                    response["code"] = 1
                                    response["result"] = result
                                except Exception as e:
                                    response["code"] = 0
                                    response["error"] = type(e).__name__
                            else:
                                response["code"] = 0
                                response["error"] = "FunctionNotFoundError"

                            response = json.dumps(response)
                            sock.send(
                                struct.pack(">I", len(response))
                                + response.encode("utf-8")
                            )
                        else:
                            sock.close()
                            self.clients.remove(sock)

    def register(self, name: str) -> Callable:
        def _(func: Callable) -> Callable:
            self.registered[name] = func
            return func

        return _
