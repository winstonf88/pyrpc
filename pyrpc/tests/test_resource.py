import mock
import unittest2 as unittest

from pyrpc.resource import resource, method
from pyrpc.service import get_service


@resource('messages')
class MessagesResource(object):

    def __init__(self, request):
        self.request = request

    @method('sayHello')
    def say_hello(self):
        return 'Hello World'

    dummy = lambda self: ''  # this is for test coverage only



class TestResource(unittest.TestCase):

    def test_add_resource_class(self):
        self.assertTrue(get_service('messages'))

    def test_add_method(self):
        service = get_service('messages')
        self.assertTrue(service.methods.get('sayHello'))

    def test_execute(self):
        service = get_service('messages')
        result = service.execute('sayHello', mock.MagicMock())
        self.assertEqual(result, 'Hello World')