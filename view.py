import struct

STR_FORMAT = 'Name: {} {} Phone: {}'
STR_ID_FORMAT = 'ID - {} Name: {} {} Phone: {}'
ERROR_FORMAT = "Error: {}"


class LocalView:
    @staticmethod
    def pb_output(res):
        if isinstance(res, str):
            print(res)
        elif isinstance(res, Exception):
            print(ERROR_FORMAT.format(res))
            raise res
        else:
            print('\n'.join([STR_ID_FORMAT.format(*x.values()) for x in res]))

    @staticmethod
    def pb_input(msg):
        res = input(msg)
        return res


class NetworkView:

    def __init__(self, _conn):
        self.conn = _conn

    def pb_output(self, data):
        if isinstance(data, str):
            res = bytes(data, 'utf-8')
        elif isinstance(data, bytes):
            res = data
        elif isinstance(data, Exception):
            res = bytes(ERROR_FORMAT.format(data), 'utf-8')
            raise data
        else:
            res = bytes('\n'.join([STR_ID_FORMAT.format(*x.values()) for x in data]), 'utf-8')
        self.conn.sendall(struct.pack('!I', len(res)))
        self.conn.sendall(res)

    def pb_input(self, msg):
        self.pb_output(msg)
        data = self.recv_one()
        return data.decode('utf-8')

    def recv_one(self):
        size, = struct.unpack('!I', self.conn.recv(4))
        return self.conn.recv(size)


def web_output(res):
    if isinstance(res, str):
        return res
    elif isinstance(res, Exception):
        return "Error: {}".format(res)
    return '<br/>'.join([STR_ID_FORMAT.format(*x.values()) for x in res])

