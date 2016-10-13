class LocalView:
    ERROR_FORMAT = "Error: {}"

    def pb_output(self, res):
        if isinstance(res, (list, tuple)):
            print('\n'.join(res))
        elif isinstance(res, str):
            print(res)
        elif isinstance(res, Exception):
            print(self.ERROR_FORMAT.format(res))
            raise res

    @staticmethod
    def pb_input(msg):
        res = input(msg)
        return res


class NetworkView:
    ERROR_FORMAT = "Error: {}"

    def __init__(self, _conn):
        self.conn = _conn

    def pb_output(self, res):
        if isinstance(res, (list, tuple)):
            output = '\n'.join(res)
            self.conn.sendall(bytes(output, 'utf-8'))
        elif isinstance(res, str):
            self.conn.sendall(bytes(res, 'utf-8'))
        elif isinstance(res, Exception):
            self.conn.sendall(bytes(self.ERROR_FORMAT.format(res), 'utf-8'))

    def pb_input(self, msg):
        self.conn.sendall(bytes(msg, 'utf-8'))
        data = self.conn.recv(1024)
        return data.decode('utf-8')
