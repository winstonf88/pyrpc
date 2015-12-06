import unittest2 as unittest

from pyrpc.jsonrpc import JsonRenderer
from pyrpc.request import RPCRequest, make_request, parse_procedure
from pyrpc.service import Service
from pyrpc.exceptions import RPCInvalidRequest

renderer = JsonRenderer()
service = Service('testparse')

@service.method('sayHello')
def say_hello(request):
    return request.rpc_params['message']


class TestRequest(unittest.TestCase):

    def test_new_request_instance(self):
        request = RPCRequest('test', {})
        self.assertIsInstance(request, RPCRequest)

    def test_make_request(self):
        procedure = {
            'id':1,
            'method': 'messages.sendMessage',
            'params': {'to':'chat','message':'Hello World!'},
        }
        request = make_request(procedure)
        self.assertIsInstance(request, RPCRequest)
        self.assertEqual(request.rpc_id, procedure['id'])
        self.assertEqual(request.rpc_method, procedure['method'])
        self.assertEqual(request.rpc_params, procedure['params'])

    def test_make_invalid_request_raises_error(self):
        procedure = {
            'id':1,
            'method': 'messages.sendMessage',
        }
        with self.assertRaises(RPCInvalidRequest):
            make_request(procedure)

    def test_parse_procedure(self):
        procedure = {
            'id': 1,
            'method': 'testparse.sayHello',
            'params': {'to':'chat','message':'Hello World!'},
        }
        expected = {'jsonrpc': '2.0', 'id': 1, 'result': 'Hello World!'}
        result = parse_procedure(renderer.serialize(procedure), renderer)
        self.assertEqual(result, renderer.serialize(expected))

    def test_parse_procedure_raises_rpcerror(self):
        procedure = {
            'id': 1,
            'method': 'invalid.method',
            'params': {},
        }
        expected = {
            'jsonrpc': '2.0',
            'id': 1,
            'error': {'code': -32601, 'message': 'method not found'}
        }
        result = parse_procedure(renderer.serialize(procedure), renderer)
        self.assertEqual(result, renderer.serialize(expected))

    def test_parse_procedure_raises_unknown_error(self):
        @service.method('error')
        def raise_error(request):
            raise ValueError

        procedure = {
            'id': 1,
            'method': 'testparse.error',
            'params': {},
        }
        expected = {
            'jsonrpc': '2.0',
            'id': 1,
            'error': {'code': -32603, 'message': 'internal error'}
        }
        result = parse_procedure(renderer.serialize(procedure), renderer)
        self.assertEqual(result, renderer.serialize(expected))
