from contacts import Contact
from data_manager import DataManager


class Model(DataManager):
    def add_check(self, phone_number):
        return phone_number in [x.phone_number for x in self.contacts]

    def create_contact(self, first_name, last_name, phone_number):
        if self.add_check(phone_number):
            return "Contact with this phone number is already in Phone Book."
        self.contacts.append(Contact(first_name, last_name, phone_number))
        self.save()
        return "Contact successfully created.\n{}".format(str(self.contacts[-1]))

    def read_contact(self, s):
        r = [x.with_index(self.contacts) for x in self.contacts if s in x]
        return r if r else "Nothing found."

    def read_all(self):
        r = [x for x in sorted(self.contacts)]
        return r if r else "Phone Book is empty."

    def update_contact(self, select_id, first_name, last_name, phone_number):
        self.contacts[int(select_id)] = Contact(first_name, last_name, phone_number)
        self.save()
        return "Contact successfully updated.\n{}".format(str(self.contacts[-1]))

    def delete_contact(self, select_id):
        res = "Contact successfully deleted.\n{}".format(str(self.contacts[-1]))
        del self.contacts[int(select_id)]
        self.save()
        return res

    @staticmethod
    def select_id(selected_id, search_result):
        r = [x for x in search_result if selected_id and selected_id in x[5:7]]
        return selected_id if r else 'ID "{}" is not in the search result.'.format(selected_id)
