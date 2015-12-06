import unittest2 as unittest

from pyrpc.exceptions import RPCError


class TestExceptions(unittest.TestCase):

    def test_rpc_error_init(self):
        error = RPCError('test error', -32701, 'this is an error')
        self.assertEqual(error.code, -32701)
        self.assertEqual(error.message, 'test error')
        self.assertEqual(error.data, 'this is an error')

    def test_as_dict(self):
        error = RPCError(data='dummy data')
        expected = {
            'code': error.code,
            'message': error.message,
            'data': error.data,
        }
        self.assertDictEqual(error.as_dict(), expected)
