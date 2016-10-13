from collections import OrderedDict


class Model:
    STR_FORMAT = 'Name: {} {} Phone: {}'
    STR_ID_FORMAT = 'ID: {} Name: {} {} Phone: {}'

    def __init__(self, _data_manager):
        self.data_manager = _data_manager

    def create_check(self, first_name, last_name, phone_number):
        return self.data_manager.database_conn.contacts.find(
            {"first_name": first_name, "last_name": last_name, "phone_number": phone_number}).count() > 0

    def create_id(self):
        return [x['_id'] for x in list(self.data_manager.database_conn.contacts.find())].pop() + 1

    def create_contact(self, first_name, last_name, phone_number):
        if self.create_check(first_name, last_name, phone_number):
            return "Contact with this phone number is already in Phone Book."
        self.data_manager.database_conn.contacts.insert(OrderedDict([('_id', self.create_id()),
                                                                     ('first_name', first_name),
                                                                     ('last_name', last_name),
                                                                     ('phone_number', phone_number)]))
        return 'Contact was successfully created.'

    def read(self, query):
        if query.isdigit():
            res = self.data_manager.database_conn.contacts.find(
                {"$or": [{"pb_id": int(query)}, {"phone_number": query}]})
        elif query.isalpha():
            res = self.data_manager.database_conn.contacts.find({'$or': [{'first_name': query}, {'last_name': query}]})
        return [self.STR_ID_FORMAT.format(*x.values()) for x in res] if res.count() > 0 else "Nothing found."

    def read_all(self):
        return [self.STR_FORMAT.format(*x.values()) for x in
                self.data_manager.database_conn.contacts.find({}, {'_id': False})]

    def update(self, _id, first_name, last_name, phone_number):
        self.data_manager.database_conn.contacts.update_one({"_id": _id}, {'$set': {"first_name": first_name,
                                                                                    "last_name": last_name,
                                                                                    "phone_number": phone_number}})
        return 'Contact was successfully updated.'

    def delete(self, _id):
        self.data_manager.database_conn.contacts.delete_one({"_id": _id})
        return "Contact was successfully deleted."

    @staticmethod
    def select_id(_id, res):
        _id = int(_id)
        get_ids = [int(x[4:6]) for x in res]
        if _id in get_ids:
            return _id
        else:
            return 'ID "{}" is not in the search result.'.format(_id)
