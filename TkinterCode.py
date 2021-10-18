import tkinter as tk
from random import sample
from tkinter.messagebox import showinfo, showerror
from COLORS import COLORS
from CustomButton import MyButton


class MineSweeper:
    window = tk.Tk()
    ROW = 5
    COLUMNS = 5
    MINES = 10
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
                btn.bind('<Button-3>', self.right_click)
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '🚩'
        elif cur_btn['text'] == '🚩':
            cur_btn['state'] = 'normal'
            cur_btn['text'] = ''

    def click(self, clicked_button: MyButton):
        print(clicked_button.__repr__())

        if MineSweeper.IS_GAME_OVER:
            return

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            self.count_mines_in_buttons()
            self.print_button()
            MineSweeper.IS_FIRST_CLICK = False
        if clicked_button.is_mine:
            clicked_button.config(text='*', background='red', disabledforeground='black')
            MineSweeper.IS_GAME_OVER = True
            showinfo('Game over', 'Поражение')
            for i in range(MineSweeper.ROW):
                for j in range(MineSweeper.COLUMNS):
                    btn = self.buttons[i][j]
                    if btn.is_mine:
                        btn['text'] = '*'
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

    def reload(self):
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def create_setting_win(self):
        win_settings = tk.Toplevel(self.window)
        win_settings.wm_title('Настройки')
        tk.Label(win_settings, text='Кол-во строк').grid(row=0, column=0)
        tk.Label(win_settings, text='Кол-во колонок').grid(row=1, column=0)
        tk.Label(win_settings, text='Кол-во мин').grid(row=2, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, MineSweeper.ROW)
        row_entry.grid(row=0, column=1, padx=20, pady=20)
        col_entry = tk.Entry(win_settings)
        col_entry.insert(0, MineSweeper.COLUMNS)
        col_entry.grid(row=1, column=1, padx=20, pady=20)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, MineSweeper.MINES)
        mines_entry.grid(row=2, column=1, padx=20, pady=20)
        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, col_entry, mines_entry))
        save_btn.grid(row=3, column=0, columnspan=2)

    def change_settings(self, row: tk.Entry, column: tk.Entry, mines: tk.Entry):
        try:
            if int(row.get()) * int(column.get()) <= int(mines.get()):
                raise ArithmeticError
        except ValueError:
            showerror('Ошибка', 'Требуется ввести целые числа')
            return
        except ArithmeticError:
            showerror('Ошибка', 'Мин должно быть меньше, чем ячеек')
            return
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):

        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='Играть', command=self.reload)
        settings_menu.add_command(label='Настройки', command=self.create_setting_win)
        settings_menu.add_command(label='Выход', command=self.window.destroy)
        menubar.add_cascade(label='Файл', menu=settings_menu)
        for i in range(MineSweeper.ROW):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j, stick='NWES')

        for i in range(MineSweeper.ROW):
            tk.Grid.rowconfigure(self.window, i, weight=1)
        for j in range(MineSweeper.COLUMNS):
            tk.Grid.columnconfigure(self.window, j, weight=1)

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
