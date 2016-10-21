from collections import OrderedDict
from pymongo import MongoClient


class Model:
    STR_FORMAT = 'Name: {} {} Phone: {}'
    STR_ID_FORMAT = 'ID - {} Name: {} {} Phone: {}'

    def __init__(self, _data_manager=None):
        self.data_manager = _data_manager
        self.database_conn = MongoClient(document_class=OrderedDict).phonebook.contacts

    def create(self, first_name, last_name, phone_number):
        if self.check_fields(first_name, last_name, phone_number):
            return self.check_fields(first_name, last_name, phone_number)
        if self.contact_check(first_name, last_name, phone_number):
            return self.contact_check(first_name, last_name, phone_number)
        self.database_conn.insert(OrderedDict([('_id', self.create_id()), ('first_name', first_name),
                                               ('last_name', last_name), ('phone_number', phone_number)]))
        return 'Contact was successfully created.'

    def read(self, first_name, last_name, phone_number):
        if not (first_name or last_name or phone_number):
            res = self.database_conn.find()
        else:
            res = self.database_conn.find({'$or': [{'first_name': first_name}, {'last_name': last_name},
                                                   {'phone_number': phone_number}]})
        return list(res) if res.count() > 0 else 'Nothing found.'

    def update(self, _id, first_name, last_name, phone_number):
        if self.check_fields(first_name, last_name, phone_number):
            return self.check_fields(first_name, last_name, phone_number)
        self.database_conn.update_one({'_id': int(_id)}, {'$set': {'first_name': first_name,
                                                                   'last_name': last_name,
                                                                   'phone_number': phone_number}})
        return 'Contact was successfully updated.'

    def delete(self, _id):
        if not isinstance(_id, int) or self.database_conn.find({"_id": _id}).count() == 0:
            return 'Wrong ID.'
        self.database_conn.delete_one({"_id": int(_id)})
        return "Contact was successfully deleted."

    def contact_check(self, first_name, last_name, phone_number):
        if self.database_conn.find({"first_name": first_name, "last_name": last_name,
                                    "phone_number": phone_number}).count() > 0:
            return 'This contact is already in Phone Book.'

    @staticmethod
    def check_fields(first_name, last_name, phone_number):
        if not (first_name and last_name and phone_number):
            return 'All fields must be filled.'
        if not first_name.isalpha() or not last_name.isalpha():
            return 'Name must be a string.'
        if not phone_number.isdigit():
            return 'Phone number must be an integer.'

    def create_id(self):
        return [x['_id'] for x in list(self.database_conn.find())].pop() + 1

    @staticmethod
    def select_id(chose_id, res):
        get_ids = [x['_id'] for x in res]
        if int(chose_id) in get_ids:
            return int(chose_id)
        else:
            return 'ID "{}" is not in the search result.'.format(chose_id)

    def get_csv_str_format(self):
        res = 'First name;Last name;Phone number\n'
        for contact in self.database_conn.find({}, {'_id': False}):
            res += '{}\n'.format(';'.join(contact.values()))
        return res

    def get_txt_str_format(self):
        res = ''
        for contact in self.database_conn.find({}, {'_id': False}):
            res += '{}\n'.format(' '.join(contact.values()))
        return res
