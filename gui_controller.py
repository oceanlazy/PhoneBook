import csv
import pickle
from tkinter.filedialog import *
from model import Model
from view import LocalView, NetworkView
from data_manager import LocalDataManager, NetworkDataManager


class App:
    FILE_FORMATS = [('TXT file format', '*.txt'), ('Comma Separated Values file format', '*.csv'),
                    ('PICKLE file format', '*.pickle'), ('All files', '.*')]

    def __init__(self, _win):
        self.win = _win
        self.win.title('Phone Book')
        self.contacts = self.pickle_open('phonebook.pickle')

        menu_bar = Menu(self.win)
        menu_bar.add_command(label="Open", command=self.opener)
        menu_bar.add_command(label="Save", command=self.saver)
        menu_bar.add_command(label="Exit", command=self.win.quit)
        self.win.config(menu=menu_bar)

        self.status_bar = Label(text='Ready', relief="sunken", anchor=W)
        self.status_bar.pack(side="bottom", fill="x")

        frame_entries = Frame(self.win)
        frame_entries.pack()

        Label(frame_entries, text="First name").grid(row=0, column=0, sticky=W)
        self.first_name_var = StringVar()
        name = Entry(frame_entries, textvariable=self.first_name_var)
        name.grid(row=0, column=1, sticky=W)

        Label(frame_entries, text="Last name").grid(row=1, column=0, sticky=W)
        self.last_name_var = StringVar()
        name = Entry(frame_entries, textvariable=self.last_name_var)
        name.grid(row=1, column=1, sticky=W)

        Label(frame_entries, text="   Phone").grid(row=2, column=0, sticky=W)
        self.phone_var = StringVar()
        phone = Entry(frame_entries, textvariable=self.phone_var)
        phone.grid(row=2, column=1, sticky=W)

        frame_crud = Frame(self.win)
        frame_crud.pack()
        Button(frame_crud, text="Create", command=self.create).grid(row=1, column=1)
        Button(frame_crud, text=" Read ", command=self.read).grid(row=1, column=2)
        Button(frame_crud, text="Update", command=self.update).grid(row=1, column=3)
        Button(frame_crud, text="Delete", command=self.delete).grid(row=1, column=4)

        frame_contacts = Frame(self.win)
        frame_contacts.pack()
        scroll = Scrollbar(frame_contacts, orient=VERTICAL)
        self.select = Listbox(frame_contacts, yscrollcommand=scroll.set, height=6, width=32)
        scroll.config(command=self.select.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.select.pack(side=LEFT, fill=BOTH, expand=True)
        self.read()

    def create(self):
        if self.check_fields():
            self.contacts.append((self.first_name_var.get(), self.last_name_var.get(), self.phone_var.get()))
            self.finish_action()

    def read(self):
        self.select.delete(0, END)
        for contact in self.contacts:
            if (self.first_name_var.get() or self.last_name_var.get() or self.phone_var.get()) in contact \
                    or not (self.first_name_var.get() or self.last_name_var.get() or self.phone_var.get()):
                self.select.insert(END, contact)
        self.status_bar['text'] = 'Ready'

    def update(self):
        contact_inx = self.which_selected()
        if contact_inx is not None and self.check_fields():
            self.contacts[contact_inx] = (self.first_name_var.get(), self.last_name_var.get(), self.phone_var.get())
            self.finish_action()

    def delete(self):
        contact_inx = self.which_selected()
        if contact_inx is not None:
            del self.contacts[contact_inx]
            self.finish_action()

    def which_selected(self):
        try:
            return int(self.contacts.index(self.select.get(self.select.curselection()[0])))
        except IndexError:
            self.status_bar['text'] = 'Not found item'

    def finish_action(self, status='Ready'):
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.phone_var.set('')
        self.pickle_save('phonebook.pickle')
        self.read()
        self.status_bar['text'] = status

    def check_fields(self):
        if self.first_name_var.get() and self.last_name_var.get() and self.phone_var.get():
            return True
        else:
            self.status_bar['text'] = 'Empty contact fields'

    def opener(self):
        file_path = askopenfilename(parent=self.win, filetypes=self.FILE_FORMATS)
        if file_path:
            file_name, file_extension = os.path.splitext(file_path)
            try:
                if file_extension == '.txt':
                    self.contacts = self.txt_open(file_path)
                if file_extension == '.csv':
                    self.contacts = self.csv_open(file_path)
                if file_extension == '.pickle':
                    self.contacts = self.pickle_open(file_path)
            except (EOFError, UnicodeDecodeError, IndexError):
                self.status_bar['text'] = 'Wrong file'
            else:
                self.finish_action('File is loaded')

    def saver(self):
        file_path = asksaveasfilename(parent=self.win, filetypes=self.FILE_FORMATS)
        if file_path:
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension == '.txt':
                self.txt_save(file_path)
            if file_extension == '.csv':
                self.csv_save(file_path)
            if file_extension == '.pickle':
                self.pickle_save(file_path)
            self.status_bar['text'] = 'File is saved'

    @staticmethod
    def txt_open(file_path):
        with open(file_path, 'r') as file:
            return [(x.split()[0], x.split()[1], x.split()[2]) for x in file.read().splitlines()]

    @staticmethod
    def csv_open(file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            reader.__next__()
            return [(row[0], row[1], row[2]) for row in reader]

    @staticmethod
    def pickle_open(file_path):
        try:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return list()

    def txt_save(self, file_path):
        with open(file_path, 'w') as file:
            for contact in self.contacts:
                file.write('{}\n'.format(' '.join(contact)))

    def csv_save(self, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['First name', 'Last name', 'Phone number'])
            for contact in self.contacts:
                writer.writerow([*contact])

    def pickle_save(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.contacts, file)


if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()