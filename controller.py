from model import Model
from view import LocalView, NetworkView
from data_manager import LocalDataManager, NetworkDataManager, check_database


class Controller:
    INPUT_FIRST_NAME = 'Enter first name?\n'
    INPUT_LAST_NAME = 'Enter last name?\n'
    INPUT_PHONE_NUMBER = 'Enter phone number?\n'

    def __init__(self, _model, _view):
        self.model = _model
        self.view = _view
        self.actions = {'1': self.create,
                        '2': self.read,
                        '3': self.update,
                        '4': self.delete,
                        '5': self.save_txt,
                        '6': self.save_csv,
                        '7': self.exit_program}

    def create(self):
        self.view.pb_output(self.model.create(*self.contact_elements()))

    def read(self):  # TODO socket
        self.view.pb_output(self.model.read(*self.contact_elements()))

    def read_all(self):
        self.view.pb_output(self.model.read_all())

    def update(self):
        self.contacts_modification_search('update')

    def delete(self):
        self.contacts_modification_search('delete')

    def contacts_modification_search(self, mod_type):
        search_result = self.model.read(self.view.pb_input('What contact to {}?\n'.format(mod_type)))
        self.view.pb_output(search_result)
        if search_result != 'Nothing found.':
            self.contacts_modification_id(mod_type, search_result)

    def contacts_modification_id(self, mod_type, search_result):
        selected_id = self.model.select_id(self.view.pb_input('What ID to {}?\n'.format(mod_type)), search_result)
        self.contacts_modification(mod_type, selected_id)

    def contacts_modification(self, mod_type, selected_id):
        if selected_id.isdigit() and mod_type == 'update':
            first_name, last_name, phone_number = self.contact_elements()
            self.view.pb_output(self.model.update(selected_id, first_name, last_name, phone_number))
        elif selected_id.isdigit() and mod_type == 'delete':
            self.view.pb_output(self.model.delete(selected_id))
        else:
            self.view.pb_output(selected_id)

    def contact_elements(self):
        first_name = self.view.pb_input(self.INPUT_FIRST_NAME)
        last_name = self.view.pb_input(self.INPUT_LAST_NAME)
        phone_number = self.view.pb_input(self.INPUT_PHONE_NUMBER)
        return first_name, last_name, phone_number

    def save_txt(self):
        self.view.pb_output(self.model.data_manager.save_file('txt'))

    def save_csv(self):
        self.view.pb_output(self.model.data_manager.save_file('csv'))

    def exit_program(self):
        self.view.pb_output('Program is successfully closed. Have a nice day!')
        exit()

    def do_actions(self, command):
        try:
            self.actions[command]()
        except Exception as e:
            return self.view.pb_output(e)

    def local_session(self):
        self.view.pb_output(check_database())
        while True:
            command = self.view.pb_input('What do you want to do?\n1 - Create\n2 - Read\n3 - Update\n4 - Delete\n'
                                         '5 - Save as txt\n6 - Save as csv\n7 - Exit\n')
            self.do_actions(command)

    def network_session(self):
        self.view.pb_output(check_database())
        while True:
            self.view.conn.sendall(b'What do you want to do?\n1 - Create\n2 - Read\n3 - Update\n4 - Delete\n'
                                   b'5 - Save as txt\n6 - Save as csv\n7 - Exit\n')
            query = self.view.conn.recv(1024)
            self.do_actions(query.decode('utf-8'))


if __name__ == '__main__':
    controller = Controller(Model(LocalDataManager()), LocalView())
    controller.local_session()


def main_network(conn):
    n_controller = Controller(Model(NetworkDataManager(conn)), NetworkView(conn))
    n_controller.network_session()
