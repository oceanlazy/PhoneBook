import csv
import pickle


class DataManager:
    def __init__(self, file_name='phone_book{}'):
        self.file = file_name
        self.contacts = self.get_contacts()

    def get_contacts(self):
        try:
            with open(self.file.format('.pickle'), 'rb') as base_file:
                return pickle.load(base_file)
        except (EOFError, FileNotFoundError):
            return list()

    def save(self):
        with open(self.file.format('.pickle'), 'wb') as f:
            pickle.dump(self.contacts, f)

    def csv(self):
        if type(self.contacts) is list:
            with open(self.file.format('.csv'), 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(['first_name', 'last_name', 'phone_number'])
                for k in self.contacts:
                    writer.writerow([k.first_name, k.last_name, k.phone_number])
            return 'Phone Book data was successfully saved to .csv file.'
        else:
            return 'Phone Book is empty.'

    def txt(self):
        with open(self.file.format('.txt'), 'w') as file:
            for contact in self.contacts:
                file.write('{}\n'.format(str(contact)))
        return 'Phone Book data was successfully saved to .txt file.'
