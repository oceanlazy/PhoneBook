from model import PhoneBookModel
from view import View
from utility import save_csv


class Controller:
    def __init__(self, _model, _view, _save):
        self.model = _model
        self.view = _view
        self.save = _save
        self.actions = {"1": self.add,
                        "2": self.update,
                        "3": self.delete,
                        "4": self.search,
                        "5": self.show_all,
                        "6": self.save_file,
                        "7": exit_program}

    def show_all(self):
        self.view.pb_print(self.model.show_all())

    def search(self):
        self.view.pb_print(self.model.search_contact(input("What contact to find?\n")))

    def add(self):
        self.view.pb_print(self.model.add_contact(*self.view.new_elements()))

    def update(self):
        search_result = self.model.search_contact(input("What contact to update?\n"))
        self.view.pb_print(search_result)
        if type(search_result) is list:
            selected_id = self.view.choose_id("Choose ID for update.\n", search_result)
            if selected_id.isdigit():
                first_name, last_name, phone_number = self.view.new_elements()
                self.view.pb_print(self.model.update_contact(selected_id, first_name, last_name, phone_number))
            else:
                self.view.pb_print(selected_id)

    def delete(self):
        search_result = self.model.search_contact(input("What contact to delete?\n"))
        self.view.pb_print(search_result)
        if type(search_result) is list:
            selected_id = self.view.choose_id("Choose ID for delete.\n", search_result)
            if selected_id.isdigit():
                self.view.pb_print(self.model.delete_contact(selected_id))
            else:
                self.view.pb_print(selected_id)

    def save_file(self):
        self.view.pb_print(self.save(self.model.show_all()))

    def do_actions(self, command):
        try:
            self.actions[command]()
        except Exception as e:
            return self.view.pb_print(e)

    def run(self):
        while True:
            command = input("What do you want to do? \n1 - Create\n2 - Update\n"
                            "3 - Delete\n4 - Search\n5 - Show all\n6 - Save file\n7 - Exit\n")
            self.do_actions(command)


def exit_program():
    exit("Have a nice day!")


def main():
    controller = Controller(PhoneBookModel(), View(), save_csv)
    controller.run()


if __name__ == '__main__':
    main()
