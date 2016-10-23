import struct
from tkinter.filedialog import *

STR_FORMAT = 'Name: {} {} Phone: {}'
STR_ID_FORMAT = 'ID - {} Name: {} {} Phone: {}'
ERROR_FORMAT = "Error: {}"


class LocalView:
    @staticmethod
    def pb_output(res):
        if isinstance(res, str):
            print(res)
        elif isinstance(res, Exception):
            print(ERROR_FORMAT.format(res))
            raise res
        else:
            print('\n'.join([STR_ID_FORMAT.format(*x.values()) for x in res]))

    @staticmethod
    def pb_input(msg):
        res = input(msg)
        return res


class NetworkView:
    def __init__(self, _conn):
        self.conn = _conn

    def pb_output(self, data):
        if isinstance(data, str):
            res = bytes(data, 'utf-8')
        elif isinstance(data, bytes):
            res = data
        elif isinstance(data, Exception):
            res = bytes(ERROR_FORMAT.format(data), 'utf-8')
        else:
            res = bytes('\n'.join([STR_ID_FORMAT.format(*x.values()) for x in data]), 'utf-8')
        self.conn.sendall(struct.pack('!I', len(res)))
        self.conn.sendall(res)

    def pb_input(self, msg):
        self.pb_output(msg)
        data = self.recv_one()
        return data.decode('utf-8')

    def recv_one(self):
        size, = struct.unpack('!I', self.conn.recv(4))
        return self.conn.recv(size)


def web_output(res):
    if isinstance(res, str):
        return res
    elif isinstance(res, Exception):
        return "Error: {}".format(res)
    return '<br/>'.join([STR_ID_FORMAT.format(*x.values()) for x in res])


class TkView:
    FILE_FORMATS = [('TXT file format', '*.txt'), ('Comma Separated Values file format', '*.csv'), ('All files', '.*')]

    def __init__(self, _win, _model):
        self.win = _win
        self.model = _model
        self.win.title('Phone Book')

        menu_bar = Menu(self.win)
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
        return

    def read(self):
        self.select.delete(0, END)
        try:
            self.select.insert(END, *[(x['first_name'], x['last_name'], x['phone_number']) for x in self.model.read(
                self.first_name_var.get(), self.last_name_var.get(), self.phone_var.get())])
        except TypeError:
            self.status_bar['text'] = 'Phone Book is empty.'
        else:
            self.status_bar['text'] = 'Ready.'

    def update(self):
        return

    def delete(self):
        return

    def saver(self):
        return

    def which_selected(self):
        try:
            cur_select = self.select.get(self.select.curselection()[0])
            full_data = [(x['first_name'], x['last_name'], x['phone_number']) for x in self.model.read()]
            return self.model.read()[full_data.index(cur_select)]['_id']
        except IndexError:
            self.status_bar['text'] = 'Not found item.'

    def finish_action(self, status='Ready'):
        self.first_name_var.set('')
        self.last_name_var.set('')
        self.phone_var.set('')
        self.read()
        self.status_bar['text'] = status

    def ask_for_save(self):
        return asksaveasfilename(parent=self.win, defaultextension='.txt', filetypes=self.FILE_FORMATS)
