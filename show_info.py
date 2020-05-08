import tkinter as tk
from config import ERROR_COLOR
from checker import *


class ShowInfo(tk.Toplevel):
    def __init__(self, db_connection, width=None, height=None):
        super().__init__()
        self.db_connection = db_connection
        if width and height:
            self.geometry(f'{width}x{height}')
        self.title('Экран просмотра информации.')
        self._add_widgets()

    def _show_info(self):
        selection = check('selection', label=self.list_label, lbox=self.listbox)
        if selection is None:
            return

        cursor = self.db_connection.cursor()
        elements = cursor.execute('SELECT * FROM categories').fetchall()
        elements += cursor.execute('SELECT * FROM targets').fetchall()
        self.info_text.delete(0.0, tk.END)
        el = elements[selection]
        # Todo: улучшить проверку.
        if len(el) == 2:
            self.info_text.insert(tk.INSERT, f'Название: {el[0]}\nЗначение: {el[1]}')
        elif len(el) == 3:
            info_string = f'Название: {el[0]}\nТекущее значение: {el[1]}\nЦель: {el[2]}'
            self.info_text.insert(tk.INSERT, info_string)

    def _add_widgets(self):
        # Создаём виджеты.
        self.list_label = tk.Label(self, text='Выберите элемент из поля ниже')
        self.listbox = tk.Listbox(self)
        self._fill_listbox()
        self.info_text = tk.Text(self)
        self.enter_button = tk.Button(self, text='Ввод!')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR, command=self.destroy)

        # Привязываем обработчики.
        self.enter_button.bind('<Button-1>', lambda _: self._show_info())

        # Пакуем виджеты.
        self.list_label.pack()
        self.listbox.pack()
        self.info_text.pack()
        self.enter_button.pack()
        self.exit_button.pack()

    def _fill_listbox(self):
        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()

        elements = cursor.execute('SELECT name FROM categories').fetchall()
        for element in [el[0] for el in elements]:
            self.listbox.insert(tk.END, f'{element} (категория)')
        elements = cursor.execute('SELECT name FROM targets').fetchall()
        for element in [el[0] for el in elements]:
            self.listbox.insert(tk.END, f'{element} (цель)')
