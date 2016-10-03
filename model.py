import csv
import os
import threading

from contacts import Contact


class Model:
    def __init__(self, file_name_template='phone_book_{}.{}'):
        self.file = file_name_template
        self.contacts = [Contact('Arnold', 'Schwarzenegger', '0101'), Contact('Bruce', 'Willis', '102'),
                         Contact('Sylvester', 'Stallone', '103')]

    def add_check(self, phone_number):
        return phone_number in [x.phone_number for x in self.contacts]

    def create_contact(self, first_name, last_name, phone_number):
        if self.add_check(phone_number):
            return "Contact with this phone number is already in Phone Book."
        self.contacts.append(Contact(first_name, last_name, phone_number))
        return "Contact successfully created.\n{}".format(str(self.contacts[-1]))

    def read(self, s):
        r = [x.with_index(self.contacts) for x in self.contacts if s in x]
        return r if r else "Nothing found."

    def read_all(self):
        r = [str(x) for x in sorted(self.contacts)]
        return r if r else "Phone Book is empty."

    def update_contact(self, select_id, first_name, last_name, phone_number):
        self.contacts[int(select_id)] = Contact(first_name, last_name, phone_number)
        return "Contact successfully updated.\n{}".format(str(self.contacts[-1]))

    def delete_contact(self, select_id):
        res = "Contact successfully deleted.\n{}".format(str(self.contacts[-1]))
        del self.contacts[int(select_id)]
        return res

    @staticmethod
    def select_id(selected_id, search_result):
        r = [x for x in search_result if selected_id and selected_id in x[5:7]]
        return selected_id if r else 'ID "{}" is not in the search result.'.format(selected_id)

    def save_csv(self, conn):
        if type(self.contacts) is list:
            file_name = self.file.format(str(threading.current_thread().ident), 'csv')
            with open(file_name, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(['first_name', 'last_name', 'phone_number'])
                for k in self.contacts:
                    writer.writerow([k.first_name, k.last_name, k.phone_number])
            with open(file_name, 'rb') as file:
                file_part = file.read(1024)
                while file_part:
                    conn.send(file_part)
                    file_part = file.read(1024)
            os.remove(file_name)
            return 'Phone Book data was successfully saved to .csv file.'
        else:
            return 'Phone Book is empty.'
