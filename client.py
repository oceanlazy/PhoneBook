import socket
import struct


class Client:
    FILE_NAME = 'phone_book_net.{}'

    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(('localhost', 5000))

    def recv_one(self):
        size, = struct.unpack('!I', self.sock.recv(4))
        return self.sock.recv(size)

    def send_one(self, data):
        self.sock.sendall(struct.pack('!I', len(data)))
        self.sock.sendall(data)

    def get_file(self):
        file_size, = struct.unpack('!I', self.sock.recv(4))
        file_data = self.sock.recv(file_size)
        if file_data.startswith(b'First name;'):
            file_name = self.FILE_NAME.format('csv')
        else:
            file_name = self.FILE_NAME.format('txt')
        with open(file_name, 'wb') as file:
            file.write(file_data)

client = Client()
while True:
    answer = client.recv_one()
    if b'atabase' in answer:
        print(answer.decode('utf-8'))
        answer = client.recv_one()
    inp = input(answer.decode('utf-8'))
    client.send_one(bytes(inp, 'utf-8'))
    if int(inp) == 5 or int(inp) == 6:
        client.get_file()
    answer = client.recv_one()
    while answer.endswith(b'?\n'):
        inp = input(answer.decode('utf-8'))
        client.send_one(bytes(inp, 'utf-8'))
        answer = client.recv_one()
    if b'closed' in answer:
        client.sock.close()
        exit()
    print(answer.decode('utf-8'))
