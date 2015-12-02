import logging

from pyrpc.exceptions import RPCError
from pyrpc.service import get_service

log = logging.getLogger('pyrpc')


def parse_procedure(procedure, renderer, **kw):
    """Execute a procedure.

    :param procedure: rpc procedure data
    :param renderer: procedure parser
    :param kw: arguments are passed into the request object
    :return: rpc response
    """
    response = {'jsonrpc': '2.0', 'id': None}
    try:
        procedure = renderer.deserialize(procedure)
        request = RPCRequest(
            method=procedure.get('method'),
            params=procedure.get('params'),
            id_=procedure.get('id'),
            **kw
        )
        response['id'] = request.rpc_id
        service_name, method = request.rpc_method.split('.')
        service = get_service(service_name)
        result = service.execute(method, request)
    except RPCError as err:
        response['error'] = err.as_dict()
    except Exception as err:
        log.error(str(err))
        response['error'] = RPCError().as_dict()
    else:
        response['result'] = result

    return renderer.serialize(response)


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
