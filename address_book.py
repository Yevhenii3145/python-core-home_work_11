from collections import UserDict
from datetime import datetime


class Field():
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name: str):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone: str):
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, birthday: str):
        super().__init__(birthday)


class Record():
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.__birthday = None
        self.__phone = None

        self.name = Name(name)

        self.phones = []
        if phone:
            self.add_phone(phone)

        self.birthday = birthday
        self.phone = Phone(phone)

    def days_to_birthday(self, birthday):
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        today = datetime.now()
        birthday = birthday.replace(year=today.year)
        days_to_date = birthday - today
        if days_to_date.days < 0:
            return f'was {days_to_date.days} days ago'
        return f'{days_to_date.days} days to birthday'

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday=None):
        if type(birthday) == tuple:
            raise ValueError(f'Birthday can not be in 2 dates')
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Data must be yyyy-mm-dd')
        self.__birthday = birthday

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        if not phone.isnumeric():
            raise ValueError('Phone contains unsupported characters')
        self.__phone = phone

    def add_phone(self, phone: str):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone: str):
        index = self.find_phone_index(phone)
        if index is not None:
            self.phones.pop(index)

    def edit_phone(self, old_phone: str, new_phone: str):
        index = self.find_phone_index(old_phone)
        if index is not None:
            self.phones[index] = Phone(new_phone)

    def find_phone_index(self, old_phone: str):
        for index, phone in enumerate(self.phones):
            if phone.value == old_phone:
                return index
        return None

    def __repr__(self) -> str:
        return f"{self.name} : {', '.join([str(p.value) for p in self.phones])} : {self.birthday} ({self.days_to_birthday(self.birthday)})"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, N=None):
        start = 0
        while True:
            if N:
                result = list(self.data.values())[start:start+N]
            else:
                result = list(self.data.values())[start:]
                return result
            if not result:
                break
            yield result
            start += N

    def __repr__(self):
        return str(self.data)


if __name__ == '__main__':
    new_contact_1 = Record("Nina", 322223322)
    new_contact_2 = Record("Olga", 1488322)
    new_contact_3 = Record("Kizaru", 666)
    new_phone_book = AddressBook()
    new_phone_book.add_record(new_contact_1)
    new_phone_book.add_record(new_contact_2)
    new_phone_book.add_record(new_contact_3)
    print(new_phone_book)
