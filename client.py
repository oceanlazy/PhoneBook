import socket

sock = socket.socket()
sock.connect(('localhost', 5000))
while True:
    answer = sock.recv(1024)
    inp = input(answer.decode('utf-8'))
    sock.sendall(bytes(inp, 'utf-8'))
    answer = sock.recv(1024)
    while answer.endswith(b'?\n'):
        inp = input(answer.decode('utf-8'))
        sock.sendall(bytes(inp, 'utf-8'))
        answer = sock.recv(1024)
    if answer.startswith(b'first_name;'):
        with open('phone_book_data_2.csv', 'wb') as file:
            while b'saved' not in answer:
                file.write(answer)
                answer = sock.recv(1024)
    print(answer.decode('utf-8'))
    if inp == '7':
        sock.close()
        exit()
