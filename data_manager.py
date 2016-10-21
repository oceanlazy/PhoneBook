import csv
import os
import threading
import struct
from pymongo import MongoClient
from collections import OrderedDict


class LocalDataManager:
    def __init__(self):
        self.database_conn = MongoClient(document_class=OrderedDict).phonebook
        self.contacts = self.get_contacts()
        self.file_name = 'phone_book.{}'

    def get_contacts(self):
        return [list(x.values()) for x in list(self.database_conn.contacts.find({}, {'_id': False}))]

    def save_txt(self):
        with open(self.file_name.format('txt'), 'w') as file:
            for contact in self.contacts:
                file.write('{}\n'.format(' '.join(contact)))
        return 'Phone Book data is successfully saved to .txt file.'

    def save_csv(self):
        with open(self.file_name.format('csv'), 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(['First name', 'Last name', 'Phone number'])
            for contact in self.contacts:
                writer.writerow([*contact])
        return 'Phone Book data is successfully saved to .csv file.'

    def check_database(self):
        base_data = (
            OrderedDict([("_id", 1), ('first_name', 'Arnold'), ('last_name', 'Schwarzenegger'), ('phone_number', '0101')]),
            OrderedDict([("_id", 2), ('first_name', 'Bruce'), ('last_name', 'Willis'), ('phone_number', '102')]),
            OrderedDict([("_id", 8), ('first_name', 'Sylvester'), ('last_name', 'Stallone'), ('phone_number', '102')]))
        if 'contacts' not in self.database_conn.collection_names():
            self.database_conn.contacts.insert(base_data)
            return 'Database is successfully created.'
        else:
            return 'Database is successfully loaded.'


class NetworkDataManager(LocalDataManager):
    def __init__(self, _conn):
        LocalDataManager.__init__(self)
        self.file_name = 'phone_book_%s.{}' % str(threading.current_thread().ident)
        self.conn = _conn

    def save_txt(self):
        super().save_txt()
        self.send_file('txt')
        return 'Phone Book data is successfully saved to .txt file.'

    def save_csv(self):
        super().save_csv()
        self.send_file('csv')
        return 'Phone Book data is successfully saved to .csv file.'

    def send_file(self, extension):
        file_name = self.file_name.format(extension)
        file_size = os.stat(file_name).st_size
        self.conn.send(struct.pack('!I', file_size))
        with open(file_name, 'rb') as file:
            data = file.read(file_size)
            self.conn.send(data)
        os.remove(file_name)
