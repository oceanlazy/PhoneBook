class Model:
    STR_FORMAT = 'Name: {} {} Phone: {}'
    STR_ID_FORMAT = 'ID: {} Name: {} {} Phone: {}'

    def __init__(self, _data_manager):
        self.data_manager = _data_manager

    def create_check(self, first_name, last_name, phone_number):
        self.data_manager.cursor.execute('SELECT * FROM phonebook '
                                         'WHERE first_name=%s AND last_name=%s AND phone_number=%s',
                                         (first_name, last_name, phone_number))
        return self.data_manager.cursor.fetchone()

    def create_contact(self, first_name, last_name, phone_number):
        if self.create_check(first_name, last_name, phone_number):
            return "Contact with this phone number is already in Phone Book."
        self.data_manager.cursor.execute(
            'INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s,%s,%s)',
            (first_name, last_name, phone_number))
        self.data_manager.database_conn.commit()
        return 'Contact was successfully created.'

    def read(self, query, show_id=False):
        if query.isdigit():
            self.data_manager.cursor.execute('SELECT * FROM phonebook WHERE id=%s OR phone_number=%s', (query, query))
        elif query.isalpha():
            self.data_manager.cursor.execute('SELECT * FROM phonebook WHERE first_name=%s OR last_name=%s',
                                             (query, query))
        res = self.data_manager.cursor.fetchone()
        if show_id:
            return self.STR_ID_FORMAT.format(*res) if res else "Nothing found."
        else:
            return self.STR_FORMAT.format(*res[1:]) if res else "Nothing found."

    def read_all(self):
        self.data_manager.cursor.execute('SELECT * FROM phonebook')
        res = self.data_manager.cursor.fetchall()
        return [self.STR_FORMAT.format(*x[1:]) for x in res]

    def update(self, pb_id, first_name, last_name, phone_number):
        self.data_manager.cursor.execute('''UPDATE phonebook SET first_name=%s, last_name=%s, phone_number=%s
                                        WHERE id=%s''', (first_name, last_name, phone_number, pb_id))
        self.data_manager.cursor.execute('SELECT * FROM phonebook WHERE id=%s', (pb_id,))
        self.data_manager.database_conn.commit()
        return 'Contact was successfully updated.'

    def delete(self, pb_id):
        self.data_manager.cursor.execute('''DELETE FROM phonebook WHERE id=%s''', (pb_id,))
        return "Contact was successfully deleted."

    @staticmethod
    def select_id(pb_id, res):
        if pb_id.isdigit() and int(res[4:6]) == int(pb_id):
            return pb_id
        else:
            return 'ID "{}" is not in the search result.'.format(pb_id)
