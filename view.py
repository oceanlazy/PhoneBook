class View:
    ERROR_FORMAT = "Error: {}"
    INPUT_FIRST_NAME = "Enter first name.\n"
    INPUT_LAST_NAME = "Enter last name.\n"
    INPUT_PHONE_NUMBER = "Enter phone number.\n"

    def pb_print(self, res):
        if isinstance(res, (list, tuple)):
            for i in res:
                print(i)
        elif isinstance(res, str):
            print(res)
        elif isinstance(res, Exception):
            print(self.ERROR_FORMAT.format(res))
            raise res

    def new_elements(self):
        first_name = input(self.INPUT_FIRST_NAME)
        last_name = input(self.INPUT_LAST_NAME)
        phone_number = input(self.INPUT_PHONE_NUMBER)
        if not first_name.isalpha() or not last_name.isalpha():
            raise TypeError("Name must be a string.")
        if not phone_number.isdigit():
            raise TypeError("Phone number must be a integer.")
        return first_name, last_name, phone_number

    @staticmethod
    def choose_id(msg, res):
        selected_id = input(msg)
        r = [x for x in res if selected_id and selected_id in x[5:7]]
        return selected_id if r else 'ID "{}" is not in the search result.'.format(selected_id)
