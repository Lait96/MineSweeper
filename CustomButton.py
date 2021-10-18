import tkinter as tk


class MyButton(tk.Button):

    def __init__(self, master, x, y, number, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x
        self.y = y
        self.number = number
        self.is_mine = False
        self.count_bomb = 0
        self.is_open = False

    def config(self, is_open=False, *args, **kwargs):
        if is_open:
            self.is_open = is_open
        super(MyButton, self).config(*args, **kwargs)

    def __repr__(self):
        return f'|{"Mine" if self.is_mine else "NotMine"}_Button{self.number} - coord({self.x} {self.y})|'