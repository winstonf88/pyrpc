import unittest2 as unittest
import mock

from pyrpc.service import Service, get_service, remove_service
from pyrpc.exceptions import DuplicatedServiceError
from pyrpc.exceptions import RPCMethodNotFound
from pyrpc.exceptions import DuplicatedMethodError

test_service = Service('test')

@test_service.method('sayHello')
def say_hello(request):
    return 'Hello World'


class TestService(unittest.TestCase):

    def test_new_service_instance(self):
        self.assertIsInstance(test_service, Service)

    def test_duplicated_service_name_raises_error(self):
        with self.assertRaises(DuplicatedServiceError):
            service = Service('test')

    def test_get_service(self):
        service = get_service('test')
        self.assertIs(service, test_service)

    def test_get_unregistered_service_raises_error(self):
        with self.assertRaises(RPCMethodNotFound):
            get_service('unregistered')

    def test_remove_service(self):
        service_name = 'testremove'
        service = Service(service_name)

        remove_service(service)
        with self.assertRaises(RPCMethodNotFound):
            get_service(service_name)

    def test_add_method(self):
        method = test_service.methods.get('sayHello')
        self.assertIs(method, say_hello)

    def test_add_duplicated_method_name_raises_error(self):
        dummy = lambda req: ''
        with self.assertRaises(DuplicatedMethodError):
            test_service.add_method('sayHello', dummy)

    def test_execute(self):
        req = mock.MagicMock()
        result = test_service.execute('sayHello', req)
        self.assertEqual(result, 'Hello World')

    def test_execute_unknown_method_raises_error(self):
        with self.assertRaises(RPCMethodNotFound):
            test_service.execute('404method', mock.MagicMock())

    def test_class_service(self):
        class DummyService(object):
            def __init__(self, request):
                self.request = request

            def say_hello(self):
                return 'Hello World'

        service = Service('classservice')
        service.add_method('sayHello', 'say_hello', klass=DummyService)
        self.assertTrue(service.methods.get('sayHello'))

        result = service.execute('sayHello', mock.MagicMock())
        self.assertEqual(result, 'Hello World')


