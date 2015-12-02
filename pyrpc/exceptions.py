class DuplicatedServiceError(Exception):
    pass


class DuplicatedMethodError(Exception):
    pass


class RPCError(Exception):
    code = -32603
    message = 'internal error'
    data = None

    def __init__(self, message=None, code=None, data=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if data is not None:
            self.data = data

    def as_dict(self):
        error = {'code': self.code, 'message': self.message}
        if self.data is not None:
            error['data'] = self.data
        return error


class RPCInvalidRequest(RPCError):
    code = -32600
    message = 'invalid request'


class RPCMethodNotFound(RPCError):
    code = -32601
    message = 'method not found'


class RPCInvalidParams(RPCError):
    code = -32602
    message = 'invalid params'


class RPCParseError(RPCError):
    code = -32700
    message = 'parse error'
