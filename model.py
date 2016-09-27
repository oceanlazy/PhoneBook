from contacts import PhoneBookContact
import pickle


class PhoneBookModel:
    def __init__(self, base_file="phone_book.pickle"):
        self.file = base_file
        self.contacts = self.load_data()

    def load_data(self):
        try:
            with open(self.file, "rb") as base_file:
                return pickle.load(base_file)
        except (EOFError, FileNotFoundError):
            return [PhoneBookContact('Arnold', 'Schwarzenegger', '0101'), PhoneBookContact('Bruce', 'Willis', '102'),
                    PhoneBookContact('Sylvester', 'Stallone', '103')]
            # return list()

    def save_data(self):
        with open(self.file, "wb") as f:
            pickle.dump(self.contacts, f)

    def add_check(self, phone_number):
        return phone_number in [x.phone_number for x in self.contacts]

    def show_all(self):
        r = [x for x in sorted(self.contacts)]
        return r if r else "Phone Book is empty."

    def search_contact(self, s):
        r = [x.with_index(self.contacts) for x in self.contacts if s in x]
        return r if r else "Nothing found."

    def add_contact(self, first_name, last_name, phone_number):
        if self.add_check(phone_number):
            return "Contact with this phone number is already in Phone Book."
        self.contacts.append(PhoneBookContact(first_name, last_name, phone_number))
        self.save_data()
        return self.contacts[-1].msg("New contact.\n")

    def update_contact(self, select_id, first_name, last_name, phone_number):
        self.contacts[int(select_id)] = PhoneBookContact(first_name, last_name, phone_number)
        self.save_data()
        return self.contacts[int(select_id)].msg("Contact updated.\n")

    def delete_contact(self, select_id):
        res = self.contacts[int(select_id)].msg("Contact deleted.\n")
        del self.contacts[int(select_id)]
        self.save_data()
        return res
