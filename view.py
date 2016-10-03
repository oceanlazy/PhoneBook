import socket
import yaml


class View:
    ERROR_FORMAT = "Error: {}"

    def __init__(self, _conn):
        self.conn = _conn

    def pb_output(self, res):
        if isinstance(res, (list, tuple)):
            send = '\n'.join(res)
            self.conn.sendall(bytes(send, 'utf-8'))
        elif isinstance(res, str):
            self.conn.sendall(bytes(res, 'utf-8'))
        elif isinstance(res, Exception):
            print(4)
            self.conn.sendall(bytes(self.ERROR_FORMAT.format(res), 'utf-8'))

    def pb_input(self, msg):
        self.conn.sendall(bytes(msg, 'utf-8'))
        data = self.conn.recv(1024)
        return data.decode('utf-8')
