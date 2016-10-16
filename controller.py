from tkinter.filedialog import *
import pickle
import csv
import os


class App:
    FILE_FORMATS = [('TXT file format', '*.txt'), ('Comma Separated Values file format', '*.csv'),
                    ('PICKLE file format', '*.pickle'), ('All files', '.*')]

    def __init__(self, _win):
        self.win = _win
        self.win.title('Phone Book')
        self.contacts = self.pickle_open('phonebook.pickle')

        menu_bar = Menu(self.win)
        menu_bar.add_command(label="Open", command=self.open_file)
        menu_bar.add_command(label="Save", command=self.save_file)
        menu_bar.add_command(label="Exit", command=self.win.quit)
        self.win.config(menu=menu_bar)

        frame1 = Frame(self.win)
        frame1.pack()

        Label(frame1, text="First name").grid(row=0, column=0, sticky=W)
        self.first_name_var = StringVar()
        name = Entry(frame1, textvariable=self.first_name_var)
        name.grid(row=0, column=1, sticky=W)

        Label(frame1, text="Last name").grid(row=1, column=0, sticky=W)
        self.last_name_var = StringVar()
        name = Entry(frame1, textvariable=self.last_name_var)
        name.grid(row=1, column=1, sticky=W)

        Label(frame1, text="   Phone").grid(row=2, column=0, sticky=W)
        self.phone_var = StringVar()
        phone = Entry(frame1, textvariable=self.phone_var)
        phone.grid(row=2, column=1, sticky=W)

        frame2 = Frame(self.win)
        frame2.pack()
        Button(frame2, text="Create", command=self.create).grid(row=1, column=1)
        Button(frame2, text=" Read ", command=self.read).grid(row=1, column=2)
        Button(frame2, text="Update", command=self.update).grid(row=1, column=3)
        Button(frame2, text="Delete", command=self.delete).grid(row=1, column=4)

        frame4 = Frame(self.win)
        frame4.pack()
        scroll = Scrollbar(frame4, orient=VERTICAL)
        self.select = Listbox(frame4, yscrollcommand=scroll.set, height=6)
        scroll.config(command=self.select.yview)
        scroll.pack(side=RIGHT, fill=Y)
        self.select.pack(side=LEFT, fill=BOTH, expand=1)
        self.contacts_select()

    def open_file(self):
        file_path = askopenfilename(parent=self.win, filetypes=self.FILE_FORMATS)
        if file_path:
            try:
                file_name, file_extension = os.path.splitext(file_path)
                if file_extension == '.txt':
                    self.contacts = self.txt_open(file_path)
                if file_extension == '.csv':
                    self.contacts = self.csv_open(file_path)
                if file_extension == '.pickle':
                    self.contacts = self.pickle_open(file_path)
                self.contacts_select()
            except (EOFError, FileNotFoundError, IndexError):
                pass

    def save_file(self):
        file_path = asksaveasfilename(parent=self.win, filetypes=self.FILE_FORMATS)
        if file_path:
            file_name, file_extension = os.path.splitext(file_path)
            if file_extension == '.txt':
                self.txt_save(file_path)
            if file_extension == '.csv':
                self.csv_save(file_path)
            if file_extension == '.pickle':
                self.pickle_save(file_path)

    def after_action(self):
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.phone_var.set('')
        self.pickle_save('phonebook.pickle')
        self.contacts_select()

    def which_selected(self):
        try:
            return int(self.contacts.index(self.select.get(self.select.curselection()[0])))
        except IndexError:
            return

    def create(self):
        if self.first_name_var.get() and self.last_name_var.get() and self.phone_var.get():
            self.contacts.append((self.first_name_var.get(), self.last_name_var.get(), self.phone_var.get()))
            self.after_action()

    def read(self):
        self.select.delete(0, END)
        for contact in self.contacts:
            if (self.first_name_var.get() or self.last_name_var.get() or self.phone_var.get()) in contact \
                    or not (self.first_name_var.get() or self.last_name_var.get() or self.phone_var.get()):
                self.select.insert(END, contact)

    def update(self):
        contact_inx = self.which_selected()
        if contact_inx is not None and self.first_name_var.get() and self.last_name_var.get() and self.phone_var.get():
            self.contacts[contact_inx] = (self.first_name_var.get(), self.last_name_var.get(), self.phone_var.get())
            self.after_action()

    def delete(self):
        contact_inx = self.which_selected()
        if contact_inx is not None:
            del self.contacts[contact_inx]
            self.after_action()

    def contacts_select(self):
        self.select.delete(0, END)
        for first_name, last_name, phone in self.contacts:
            self.select.insert(END, [first_name, last_name, phone])

    @staticmethod
    def txt_open(file_path):
        with open(file_path, 'r') as file:
            return [tuple(x.split()) for x in file.read().splitlines()]

    @staticmethod
    def csv_open(file_path):
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=';')
            reader.__next__()
            contacts = list()
            for row in reader:
                contacts.append((*row,))
            return contacts

    @staticmethod
    def pickle_open(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)

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
