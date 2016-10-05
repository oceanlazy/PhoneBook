import pickle
import csv
import os
import threading
from contacts import Contact


class DataManager:
    def __init__(self, _file_name='phone_book'):
        self.file_name = _file_name
        self.contacts = [Contact('Arnold', 'Schwarzenegger', '0101'), Contact('Bruce', 'Willis', '102'),
                         Contact('Sylvester', 'Stallone', '103')]

    def check_filename(self, conn):
        return '%s_{t}.{e}' % self.file_name if conn else '%s.{e}' % self.file_name

    def get_contacts(self):
        try:
            file_name = self.file_name.format(t=str(threading.current_thread().ident), e='pickle')
            with open(file_name, 'rb') as base_file:
                return pickle.load(base_file)
        except (EOFError, FileNotFoundError):
            return list()

    def save_pickle(self):
        file_name = self.check_filename(False).format(t=str(threading.current_thread().ident), e='pickle')
        with open(file_name, 'wb') as f:
            pickle.dump(self.contacts, f)

    def save_file(self, extension, conn=False):
        if type(self.contacts) is list:
            file_name = self.check_filename(conn).format(t=str(threading.current_thread().ident), e=extension)
            if extension == 'txt':
                with open(file_name, 'w') as file:
                    for contact in self.contacts:
                        file.write('{}\n'.format(str(contact)))
            elif extension == 'csv':
                with open(file_name, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file, delimiter=';')
                    writer.writerow(['first_name', 'last_name', 'phone_number'])
                    for i in self.contacts:
                        writer.writerow([i.first_name, i.last_name, i.phone_number])
            if conn:
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
