import socket

sock = socket.socket()
sock.connect(('localhost', 5000))
while True:
    answer = sock.recv(140)
    inp = input(answer.decode('utf-8'))
    sock.sendall(bytes(inp, 'utf-8'))
    answer = sock.recv(1024)
    while answer.endswith(b'?\n'):
        inp = input(answer.decode('utf-8'))
        sock.sendall(bytes(inp, 'utf-8'))
        answer = sock.recv(1024)
    if answer.decode('utf-8').isdigit():
        file_size = int(answer)
        answer = sock.recv(file_size)
        if answer.startswith(b'first_name;'):
            file_name = 'phone_book_data_2.csv'
        else:
            file_name = 'phone_book_data_2.txt'
        with open(file_name, 'wb') as file:
            file.write(answer)
        answer = sock.recv(69)
    print(answer.decode('utf-8'))
    if inp == '8':
        sock.close()
        exit()
