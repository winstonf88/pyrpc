import functools

from pyrpc.exceptions import DuplicatedMethodError
from pyrpc.exceptions import DuplicatedServiceError

__SERVICES = {}


def get_service(name):
    return __SERVICES.get(name)


def add_service(service):
    if service.name in __SERVICES:
        raise DuplicatedServiceError('%s already registered' % service.name)
    __SERVICES[service.name] = service


class Service(object):
    """Remote Procedure Call Service."""

    def __init__(self, name):
        """Create new .. class:RPCService instance

        :param name: service name
        """
        self.name = name
        self.methods = {}
        add_service(self)

    def add_method(self, method, func, **kw):
        """Add new method.

        :param method: name of the method
        :param func: callable object
        """
        if method in self.methods:
            msg = 'method %s already register for %s' % (method, self.name)
            raise DuplicatedMethodError(msg)

        if 'klass' in kw and not callable(func):
            func = UnboundMethod(kw['klass'], func)

        self.methods[method] = func

    def async_method(self, method):
        """Decorator for registering new service method.

        :param method: name of the method
        """
        def wrapper(func):
            self.add_method(method, func)
            functools.wraps(func)
            return func
        return wrapper

    def execute(self, method, request):
        """Execute a method.

        :param method: name of the method
        :param socket: websocket instance
        :param id_: call id
        :param params: method parameters
        """
        func = self.methods[method]
        return func(request)


class UnboundMethod(object):

    def __init__(self, klass, method):
        self.klass = klass
        self.method = method
        self.__name__ = method

    def __call__(self, request):
        obj = self.klass(request)
        method = getattr(obj, self.method)
        return method()
