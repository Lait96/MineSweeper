import tkinter as tk
from random import sample
from tkinter.messagebox import showinfo

COLORS = {
    0: '#ffffff',
    1: '#9cee90',
    2: '#00ff00',
    3: '#013220',
    4: '#ffff00',
    5: '#ffa500',
    6: '#ffc0cb',
    7: '#ff0000',
    8: '#c41e3a',
}


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


class MineSweeper:
    window = tk.Tk()
    ROW = 3
    COLUMNS = 3
    MINES = 7
    IS_GAME_OVER = False
    IS_FIRST_CLICK = True

    def __init__(self):
        self.buttons = []
        count = 1
        for i in range(MineSweeper.ROW):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                btn = MyButton(MineSweeper.window, x=i, y=j, number=count)
                btn.config(command=lambda button=btn: self.click(button))
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def click(self, clicked_button: MyButton):
        print(clicked_button.__repr__())
        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_button()
            MineSweeper.IS_FIRST_CLICK = False
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Поражение')
        else:
            color = COLORS.get(clicked_button.count_bomb, 'black')
            clicked_button.config(text=clicked_button.count_bomb, disabledforeground=color, background='gray')
            if not clicked_button.count_bomb:
                self.breath_first_search(clicked_button)
        clicked_button.config(is_open=True, state='disabled', relief=tk.SUNKEN)

    def breath_first_search(self, btn: MyButton):
        queue = [btn]
        while queue:
            cur_btn = queue.pop()
            color = COLORS.get(cur_btn.count_bomb, 'black')
            cur_btn.config(is_open=True,
                           text=cur_btn.count_bomb,
                           disabledforeground=color,
                           background='gray',
                           state='disabled',
                           relief=tk.SUNKEN)
            if not cur_btn.count_bomb:
                x, y = cur_btn.x, cur_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        try:
                            if x + dx != -1 and y + dy != -1:
                                next_btn = self.buttons[x + dx][y + dy]
                                if not next_btn.is_open and next_btn not in queue:
                                    queue.append(next_btn)
                            else:
                                raise IndexError
                        except IndexError:
                            pass

    def create_widgets(self):
        for i in range(MineSweeper.ROW):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()

    def print_button(self):
        for row_btn in self.buttons:
            for btn in row_btn:
                print('B' if btn.is_mine else btn.count_bomb, end='')
            print()

    def insert_mines(self, number):
        index_mines = self.get_mines_places(number)
        for row_btn in self.buttons:
            for btn in row_btn:
                if btn.number in index_mines:
                    btn.is_mine = True

    def count_mines_in_buttons(self):
        for i in range(MineSweeper.ROW):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                count_bomb = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            try:
                                irow_dx = i + row_dx
                                jcol_dx = j + col_dx
                                if irow_dx == -1 or jcol_dx == -1:
                                    raise IndexError
                                Neighbor = self.buttons[irow_dx][jcol_dx]
                                if Neighbor.is_mine:
                                    count_bomb += 1
                            except IndexError:
                                pass
                btn.count_bomb = count_bomb

    @staticmethod
    def get_mines_places(exclude_number: int):
        while True:
            mines_places = sample(list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1)), MineSweeper.MINES)
            if exclude_number not in mines_places:
                return mines_places


game = MineSweeper()
game.start()
