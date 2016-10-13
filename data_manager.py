import csv
import os
import threading
from pymongo import MongoClient
from collections import OrderedDict


class LocalDataManager:
    def __init__(self, _file_name='phone_book'):
        self.file_name = '{}.%s'.format(_file_name)
        self.database_conn = MongoClient(document_class=OrderedDict).phonebook

    def get_contacts(self):
        return [list(x.values()) for x in list(self.database_conn.contacts.find({}, {'_id': False}))]

    def save_file(self, extension):
        if extension == 'txt':
            save_txt(self.file_name % extension, get_contacts(self.database_conn))
        elif extension == 'csv':
            save_csv(self.file_name % extension, get_contacts(self.database_conn))
        return 'Phone Book data is successfully saved to .{} file.'.format(extension)


class NetworkDataManager:
    def __init__(self, _conn, _file_name='phone_book'):
        self.file_name = '{}_{}.%s'.format(_file_name, str(threading.current_thread().ident))
        self.client_conn = _conn
        self.database_conn = MongoClient(document_class=OrderedDict).phonebook

    def save_file(self, extension):
        if extension == 'txt':
            save_txt(self.file_name % extension, get_contacts(self.database_conn))
        elif extension == 'csv':
            save_csv(self.file_name % extension, get_contacts(self.database_conn))
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


def get_contacts(conn):
    return [list(x.values()) for x in list(conn.contacts.find({}, {'_id': False}))]


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
    client = MongoClient(document_class=OrderedDict)
    db = client.phonebook
    base_data = (
        OrderedDict([("_id", 1), ('first_name', 'Arnold'), ('last_name', 'Schwarzenegger'), ('phone_number', '0101')]),
        OrderedDict([("_id", 2), ('first_name', 'Bruce'), ('last_name', 'Willis'), ('phone_number', '102')]),
        OrderedDict([("_id", 3), ('first_name', 'Sylvester'), ('last_name', 'Stallone'), ('phone_number', '102')]))
    if 'contacts' not in db.collection_names():
        db.contacts.insert(base_data)
    return 'Database is successfully loaded.'
