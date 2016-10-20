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

    def pb_output(self, res):
        if isinstance(res, str):
            self.conn.sendall(bytes(res, 'utf-8'))
        elif isinstance(res, Exception):
            self.conn.sendall(bytes(ERROR_FORMAT.format(res), 'utf-8'))
        else:
            self.conn.sendall(bytes('\n'.join([STR_ID_FORMAT.format(*x.values()) for x in res]), 'utf-8'))

    def pb_input(self, msg):
        self.conn.sendall(bytes(msg, 'utf-8'))
        data = self.conn.recv(1024)
        return data.decode('utf-8')


def web_output(res):
    if isinstance(res, str):
        return res
    elif isinstance(res, Exception):
        return "Error: {}".format(res)
    return '<br/>'.join([STR_ID_FORMAT.format(*x.values()) for x in res])

