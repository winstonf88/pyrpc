import json
import unittest2 as unittest

from pyrpc.jsonrpc import JsonRenderer
from pyrpc.exceptions import RPCParseError


class TestJSONRPC(unittest.TestCase):

    def test_new_json_renderer_instance(self):
        renderer = JsonRenderer()
        self.assertIsInstance(renderer, JsonRenderer)

    def test_serialize(self):
        renderer = JsonRenderer()
        procedure = {
            'id':1,
            'method': 'messages.sendMessage',
            'params': {'to':'chat','message':'Hello World!'},
        }

        json_procedure = json.dumps(procedure)
        self.assertEqual(renderer.serialize(procedure), json_procedure)

    def test_deserialize(self):
        renderer = JsonRenderer()
        procedure = {
            'id':1,
            'method': 'messages.sendMessage',
            'params': {'to':'chat','message':'Hello World!'},
        }
        json_procedure = json.dumps(procedure)
        self.assertDictEqual(renderer.deserialize(json_procedure), procedure)

    def test_deserialize_invalid_json_raises_error(self):
        renderer = JsonRenderer()
        json_procedure = '{"id":1,"method":to":"chat","message":"Hello Wor'
        with self.assertRaises(RPCParseError):
            renderer.deserialize(json_procedure)
