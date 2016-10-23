from tkinter import Tk
from model import Model
from data_manager import LocalDataManager
from view import TkView


class GuiController(TkView):
    def create(self):
        self.finish_action(self.model.create(self.first_name_var.get(), self.last_name_var.get(), self.phone_var.get()))

    def update(self):
        self.finish_action(self.model.update(self.which_selected(), self.first_name_var.get(), self.last_name_var.get(),
                                             self.phone_var.get()))

    def delete(self):
        self.finish_action(self.model.delete(self.which_selected()))

    def saver(self):
        self.finish_action(self.model.data_manager.gui_saver(self.ask_for_save()))


if __name__ == '__main__':
    win = Tk()
    controller = GuiController(win, Model(LocalDataManager()))
    win.mainloop()
