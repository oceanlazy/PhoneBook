import socket


sock = socket.socket()
sock.connect(('localhost', 5000))
while True:
    answer = sock.recv(140)
    if b'atabase' in answer:
        answer = sock.recv(65)
    inp = input(answer.decode('utf-8'))
    sock.sendall(bytes(inp, 'utf-8'))
    answer = sock.recv(1024)
    while answer.endswith(b'?\n'):
        inp = input(answer.decode('utf-8'))
        sock.sendall(bytes(inp, 'utf-8'))
        answer = sock.recv(1024)
    if answer.isdigit():
        file_size = int(answer)
        answer = sock.recv(file_size)
        if answer.startswith(b'first_name;'):
            file_name = 'phone_book_data_2.csv'
        else:
            file_name = 'phone_book_data_2.txt'
        with open(file_name, 'wb') as file:
            file.write(answer)
        answer = sock.recv(51)  # 85-68=17
    print(answer.decode('utf-8'))
    if b'closed' in answer:
        sock.close()
        exit()
