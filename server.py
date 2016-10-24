import controller
import threading
import socket

sock = socket.socket()
sock.bind(('localhost', 5000))
sock.listen(5)
print('Server waiting')
while True:
    conn, adr = sock.accept()
    print('Connected: {}'.format(adr))
    t = threading.Thread(target=controller.main_socket, args=(conn,))
    t.start()
