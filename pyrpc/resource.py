from pyrpc.service import Service


def resource(name):
    """Class decorator to register a resource.

    :param name: resource name
    """
    def wrapper(klass):
        return add_resource(klass, name)
    return wrapper


def add_resource(klass, name):
    """Register a resource class.

    :param klass: the class to register the service
    :param name: name of the service
    """
    service = Service(name)
    for name in dir(klass):
        if name.startswith('__'):
            continue

        meth = getattr(klass, name)
        rcpmethod = getattr(meth, '__rpcmethod__', None)
        if rcpmethod is None:
            continue
        
        service.add_method(rcpmethod, name, klass=klass)
    return klass


def method(name):
    """Method decorator to register a register a remote method.

    :param name: name of the remote method
    """
    def wrapper(func):
        return add_method(func, name)
    return wrapper


def add_method(func, name):
    """Register a remote method.

    :param func: method object
    :param name: name of the method
    """
    if hasattr(func, '__func__'):  # py2
        func = func.__func__
    func.__rpcmethod__ = name
    return func