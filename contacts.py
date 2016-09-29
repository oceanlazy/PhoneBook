from functools import total_ordering


@total_ordering
class Contact:
    STR_FORMAT = "Name: {} {} Phone: {}"
    STR_WITH_ID_FORMAT = "ID - {} Name: {} {} Phone: {}"

    def __init__(self, first_name, last_name, phone_number):
        self._first_name = first_name
        self._last_name = last_name
        self._phone_number = phone_number
        self.contact = (first_name, last_name, phone_number,)

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def phone_number(self):
        return self._phone_number

    def with_index(self, out_list):
        return self.STR_WITH_ID_FORMAT.format(out_list.index(self), self.first_name, self.last_name, self.phone_number)

    def __contains__(self, a):
        return a in self.contact

    def __repr__(self):
        return self.STR_FORMAT.format(self.first_name, self.last_name, self.phone_number)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.contact == other.contact
        return False

    def __lt__(self, other):
        return self.phone_number < other.phone_number
