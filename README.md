# Python Remote Procedure Call Library

**PyRPC** provides helpers to build and execute RPC applications.

This library is an implementation of the new 2.0 specifications.

> Currently, only JSON is supported.


Usage
-----

Function based methods.
```python
from pyrpc.service import Service

service = Service('messages')

@service.method('sendMessage')
def send_message(request):
    request.rpc_params
    {'to': 'chat', 'message': 'Hello World!'}
    # do something ...
```

Class based methods.
```python
from pyrpc.resource import resource, method

@resource('messages')
class MessageService(object):

    def __init__(self, request):
        self.request = request

    @method('sendMessage')
    def send_message(self):
        self.request.rpc_params
        {'to': 'chat', 'message': 'Hello World!'}
        # do something ...
```

Execute a remote method.
```python
from pyrpc.request import parse_procedure
from pyrpc.jsonrpc import JsonRenderer

json_procedure = '{"id":1,"method":"messages.sendMessage","params":{"to":"chat","message":"Hello World!"}}'
renderer = JsonRenderer()
parse_procedure(json_procedure, renderer)
'{"id": 1, "result": null, "jsonrpc": "2.0"}'
```


To Do List
----------
* Add method parameter specifications
* Add support for batch requests
* Add support for batch responses
