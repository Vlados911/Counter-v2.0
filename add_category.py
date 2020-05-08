"""Модуль для добавления категорий в базу данных."""

import tkinter as tk
from config import ERROR_COLOR
from checker import *


class AddCategory(tk.Toplevel):
    """Класс для добавления категорий в базу данных."""

    def __init__(self, db_connection, width=None, height=None):
        """
        Конструктор класса AddCategory.

        Принимает подключение базы данных, ширину и высоту окна (опционально)
        """
        super().__init__()
        if width and height:
            self.geometry(f'{width}x{height}')
        self.title('Экран добавления категории')
        self.db_connection = db_connection
        self._add_widgets()

    def _add_category(self):
        # Получаем пользовательские значения с помощью функции check,
        # описанной в checker.py
        name = check('name', self.name_label, self.name_entry)
        value = check('value', self.value_label, self.value_entry)

        if not name or not value:
            # Если название или значение введено в неправильном формате,
            # то прерываем выполнение.
            return

        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()

        elements = cursor.execute('SELECT name FROM categories').fetchall()
        elements = [element[0] for element in elements]

        if name in elements:
            self.name_label.config(text='Такое имя уже существует, попробуйте другое',
                              bg=ERROR_COLOR)
            return

        cursor.execute(f'INSERT INTO categories VALUES("{name}", {value})')
        self.db_connection.commit()
        self.destroy()

    def _add_widgets(self):
        """Метод, добавляющий все необходимые виджеты на экран."""
        # Создаём виджеты.
        self.name_label = tk.Label(self, text='Введите название'
                                              ' категории ниже.')
        self.name_entry = tk.Entry(self)
        self.value_label = tk.Label(self, text='Введите начальное значение '
                                               'для категории ниже.')
        self.value_entry = tk.Entry(self)
        self.enter_button = tk.Button(self, text='Ввод!')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR,
                                     command=self.destroy)

        # Привязываем обработчики.
        self.enter_button.bind('<Button-1>', lambda event: self._add_category())

        # Пакуем виджеты.
        self.name_label.pack(expand=3, side=tk.TOP)
        self.name_entry.pack(expand=3, side=tk.TOP)
        self.value_label.pack(expand=3, side=tk.TOP)
        self.value_entry.pack(expand=3, side=tk.TOP)
        self.enter_button.pack(expand=3, side=tk.TOP)
        self.exit_button.pack(expand=3, side=tk.BOTTOM)
