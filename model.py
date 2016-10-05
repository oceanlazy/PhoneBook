from data_manager import DataManager
from contacts import Contact


class Model(DataManager):
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
        return "Contact successfully updated.\n{}".format(str(self.contacts[select_id]))

    def delete_contact(self, select_id):
        res = "Contact successfully deleted.\n{}".format(str(self.contacts[select_id]))
        del self.contacts[int(select_id)]
        return res

    @staticmethod
    def select_id(selected_id, search_result):
        r = [x for x in search_result if selected_id and selected_id in x[5:7]]
        return selected_id if r else 'ID "{}" is not in the search result.'.format(selected_id)
