import logging

from pyrpc.exceptions import RPCError, RPCInvalidRequest
from pyrpc.service import get_service

log = logging.getLogger('pyrpc')

_marker = object()


def parse_procedure(procedure, renderer, **kw):
    """Execute a procedure.

    :param procedure: rpc procedure data
    :param renderer: procedure parser
    :param kw: arguments are passed into the request object
    :return: rpc response
    """
    # TODO: add support for batch requests
    response = {'jsonrpc': '2.0', 'id': None}
    try:
        procedure = renderer.deserialize(procedure)
        request = make_request(procedure, **kw)
        response['id'] = request.rpc_id
        service_name, method = request.rpc_method.split('.')
        service = get_service(service_name)
        result = service.execute(method, request)
    except RPCError as err:
        response['error'] = err.as_dict()
    except Exception as err:
        log.error(str(err))
        raise
        response['error'] = RPCError().as_dict()
    else:
        response['result'] = result

    return renderer.serialize(response)


def make_request(procedure, **kw):
    """Make new request object based on the procedure.

    :param procedure: rpc procedure
    :param kw: arguments are passed into the request object
    :return: RPCRequest instance
    :raises RPCInvalidRequest: if the procedure does not specify all the
        necessary data
    """
    method = procedure.get('method')
    params = procedure.get('params', _marker)
    if not method or params is _marker:
        raise RPCInvalidRequest

    id_ = procedure.get('id')
    request = RPCRequest(method, params, id_, **kw)
    return request


class RPCRequest(object):
    """RPC Request"""

    def __init__(self, method, params, id_=None, **kw):
        """Create request instance.

        :param method: rpc method
        :param params: rpc params
        :param id_: rpc id
        :param kw: keyword args
        """
        self.rpc_method = method
        self.rpc_params = params
        self.rpc_id = id_
        self.__dict__.update(kw)
