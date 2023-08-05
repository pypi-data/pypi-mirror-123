# RPC

A simple implementation of RPC (Remote Procedural Call) in python.

## Examples:

```python
#server implementation
from rpc import Server

server = Server("localhost", 3000)

@server.register("add")
def add(num1, num2):
    return num1 + num2

@server.register("concat")
def concat(str1, str2):
    return str1 + str2

@server.register("uppercase")
def uppercase(string):
    return string.upper()

server.run()
```

```python
#client implementation
from rpc import Client

client = Client("localhost", 3000)
client.connect()

print(client.execute("/"))
#prints: ["add", "concat", "uppercase"]

print(client.execute("add", 1, 2))
#prints: 3

print(client.execute("concat", "a", "b"))
#prints: ab

print(client.execute("uppercase", "example"))
#prints: EXAMPLE

client.close()
#closes the socket connection
```

## Links:

[Github](https://github.com/Ariam27/rpc)
