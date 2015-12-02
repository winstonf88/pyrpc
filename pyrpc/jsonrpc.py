from pyrpc.exceptions import RPCParseError
try:
    import simplejson as json
except ImportError:
    import json


class JsonRenderer(object):
    """JSON Renderer"""

    def serialize(self, struct):
        """Parse Python objects to JSON string.

        :param struct: python objects
        :return: json string
        """
        return json.dumps(struct)

    def deserialize(self, string):
        """Parse JSON string to Python objects.

        :param string: json string
        :return: Python objects
        :raises RPCParseError: if invalid json string
        """
        try:
            return json.loads(string)
        except:
            raise RPCParseError('invalid json')
