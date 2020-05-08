import tkinter as tk
from config import ERROR_COLOR
from checker import *


class EditCategory(tk.Toplevel):
    def __init__(self, db_connection, width=None, height=None):
        super().__init__()
        self.db_connection = db_connection
        if width and height:
            self.geometry(f'{width}x{height}')
        self.title('Экран изменения категории')
        self._add_widgets()

    def _add_widgets(self):
        # Создаём виджеты.
        self.list_label = tk.Label(self, text='Выберите категорию из поля ниже')
        self.categories_list = tk.Listbox(self)
        self._fill_listbox()
        self.value_label = tk.Label(self, text='Введите сумму изменения в поле ниже')
        self.value_entry = tk.Entry(self)
        self.enter_button = tk.Button(self, text='Ввод!')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR, command=self.destroy)

        # Привязываем обработчики.
        self.enter_button.bind('<Button-1>', lambda _: self._update_category())

        # Пакуем виджеты.
        self.list_label.pack()
        self.categories_list.pack()
        self.value_label.pack()
        self.value_entry.pack()
        self.enter_button.pack()
        self.exit_button.pack()

    def _update_category(self):
        value = check('value', self.value_label, self.value_entry)
        selection = check('selection', label=self.list_label, lbox=self.categories_list)

        if value is None or selection is None:
            return

        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()
        # Получаем информацию о текущих категориях.
        elements = cursor.execute('SELECT * FROM categories').fetchall()
        name, current_value = elements[selection]
        # Изменяем текущее значение
        current_value += value
        cursor.execute('UPDATE categories SET value=? WHERE name=?', (current_value, name))
        # Сохраняем изменения.
        self.db_connection.commit()
        self.destroy()

    def _fill_listbox(self):
        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()
        elements = cursor.execute('SELECT name FROM categories').fetchall()
        elements = [element[0] for element in elements]

        # Вставляем названия категорий в Listbox.
        for element in elements:
            self.categories_list.insert(tk.END, element)
