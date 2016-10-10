import csv
import os
import threading
import psycopg2


class LocalDataManager:
    def __init__(self, _file_name='phone_book'):
        self.file_name = '{}.%s'.format(_file_name)
        self.database_conn = psycopg2.connect(database="postgres", user="postgres", password=" ", port=5432)
        self.cursor = self.database_conn.cursor()

    def get_contacts(self):
        self.cursor.execute("SELECT * FROM phonebook")
        return self.cursor.fetchall()

    def save_file(self, extension):
        if extension == 'txt':
            save_txt(self.file_name % extension, self.get_contacts())
        elif extension == 'csv':
            save_csv(self.file_name % extension, self.get_contacts())
        return 'Phone Book data is successfully saved to .{} file.'.format(extension)


class NetworkDataManager:
    def __init__(self, _conn, _file_name='phone_book'):
        self.file_name = '{}_{}.%s'.format(_file_name, str(threading.current_thread().ident))
        self.client_conn = _conn
        self.database_conn = psycopg2.connect(database="postgres", user="postgres", password=" ", port=5432)
        self.cursor = self.database_conn.cursor()

    def get_contacts(self):
        self.cursor.execute("SELECT * FROM phonebook")
        return self.cursor.fetchall()

    def save_file(self, extension):
        if extension == 'txt':
            save_txt(self.file_name % extension, self.get_contacts())
        elif extension == 'csv':
            save_csv(self.file_name % extension, self.get_contacts())
        self.send_file(extension)
        return 'Phone Book data is successfully saved to .{} file.'.format(extension)

    def send_file(self, extension):
        file_name = self.file_name % extension
        file_size = b'%i' % os.stat(file_name).st_size
        self.client_conn.send(file_size)
        with open(file_name, 'rb') as file:
            data = file.read(int(file_size))
            self.client_conn.send(data)
        os.remove(file_name)


def save_txt(file_name, contacts):
    with open(file_name, 'w') as file:
        for contact in contacts:
            file.write('{}\n'.format(' '.join(contact[1:])))


def save_csv(file_name, contacts):
    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['first_name', 'last_name', 'phone_number'])
        for contact in contacts:
            writer.writerow([*contact[1:]])


def check_database():
    base_data = ({'first_name': 'Arnold', 'last_name': 'Schwarzenegger', 'phone_number': '0101'},
                 {'first_name': 'Bruce', 'last_name': 'Willis', 'phone_number': '102'},
                 {'first_name': 'Sylvester', 'last_name': 'Stallone', 'phone_number': '103'})
    conn = psycopg2.connect(database="postgres", user="postgres", password=" ", port=5432)
    cur = conn.cursor()
    try:
        cur.execute(
            '''CREATE TABLE phonebook (id serial, first_name text, last_name text, phone_number text)''')
        cur.executemany('INSERT INTO phonebook(first_name,last_name,phone_number) '
                        'VALUES (%(first_name)s, %(last_name)s, %(phone_number)s)', base_data)
        conn.commit()
    except psycopg2.ProgrammingError:
        return 'Database is successfully loaded.'
    else:
        return 'New database is successfully created.'
