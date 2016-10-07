from contacts import Contact
import threading
import os
import pickle
import csv


class LocalDataManager:
    def __init__(self, _file_name='phone_book'):
        self.file_name = '{}.%s'.format(_file_name)
        self.contacts = self.get_contacts()

    def get_contacts(self):
        try:
            file_name = self.file_name % 'pickle'
            with open(file_name, 'rb') as base_file:
                return pickle.load(base_file)
        except (EOFError, FileNotFoundError):
            return [Contact('Arnold', 'Schwarzenegger', '0101'), Contact('Bruce', 'Willis', '102'),
                    Contact('Sylvester', 'Stallone', '103')]

    def save_pickle(self):
        file_name = self.file_name % 'pickle'
        with open(file_name, 'wb') as f:
            pickle.dump(self.contacts, f)

    def save_file(self, extension, conn):
        if isinstance(self.contacts, list):
            file_name = self.file_name % extension
            if extension == 'txt':
                save_txt(file_name, self.contacts)
            elif extension == 'csv':
                save_csv(file_name, self.contacts)
            return 'Phone Book data was successfully saved to .{} file.'.format(extension)
        else:
            return 'Phone Book is empty.'


class NetworkDataManager:
    def __init__(self, _file_name='phone_book'):
        self.file_name = '{}_{}.%s'.format(str(threading.current_thread().ident), _file_name)
        self.contacts = self.get_contacts()

    def get_contacts(self):
        return [Contact('Arnold', 'Schwarzenegger', '0101'), Contact('Bruce', 'Willis', '102'),
                Contact('Sylvester', 'Stallone', '103')]

    def save_file(self, extension, conn):
        if isinstance(self.contacts, list):
            file_name = self.file_name % extension
            if extension == 'txt':
                save_txt(file_name, self.contacts)
            elif extension == 'csv':
                save_csv(file_name, self.contacts)
            self.send_file(conn, file_name)
            return 'Phone Book data was successfully saved to .{} file.'.format(extension)
        else:
            return 'Phone Book is empty.'

    @staticmethod
    def send_file(conn, file_name):
        file_size = b'%i' % os.stat(file_name).st_size
        conn.send(file_size)
        with open(file_name, 'rb') as file:
            data = file.read(int(file_size))
            conn.send(data)
        os.remove(file_name)


def save_txt(file_name, contacts):
    with open(file_name, 'w') as file:
        for contact in contacts:
            file.write('{}\n'.format(str(contact)))


def save_csv(file_name, contacts):
    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['first_name', 'last_name', 'phone_number'])
        for i in contacts:
            writer.writerow([i.first_name, i.last_name, i.phone_number])
