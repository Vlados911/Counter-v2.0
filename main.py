"""
Проект Counter.

Counter - удобное приложение для подсчёта ваших трат.
"""

import tkinter as tk
import os
import sqlite3

from config import *
from add_category import *
from edit_category import *
from add_target import *
from edit_target import *
from show_info import *


class MainWindow(tk.Tk):
    """Класс главного окна программы."""

    def __init__(self, title, db_name='data.db', width=None, height=None):
        """
        Конструктор принимает заголовок окна, имя файла базы данных.

        Можно передать ширину и высоту окна (опционально).
        """
        super().__init__()
        if width and height:
            self.geometry(f'{width}x{height}')
        self._check_database(db_name)
        self.title(title)
        self.add_widgets()
        # self.mainloop()

    def _check_database(self, name):
        """Метод для проверки базы данных."""
        files = os.listdir()
        if name in files:
            # Если файл уже содержится в папке проекта, то просто подключаем базу данных.
            self.db_connection = sqlite3.connect(DB_NAME)
        else:
            # Иначе создаём новую и создаём в ней необходимые таблицы.
            self.db_connection = sqlite3.connect(DB_NAME)
            cursor = self.db_connection.cursor()
            # Создаём необходимые таблицы в базе данных.
            cursor.execute('CREATE TABLE categories(name text, value integer)')
            cursor.execute('CREATE TABLE targets(name text, current_value integer, target integer)')
            self.db_connection.commit()

    def add_widgets(self):
        """Метод, добавляющий виджеты на главный экран."""
        # Создаём виджеты.
        self.add_category_button = tk.Button(text='Добавить новую категорию расходов')
        self.edit_category_button = tk.Button(text='Изменить категорию')
        self.add_target_button = tk.Button(text='Добавить новую цель')
        self.edit_target_button = tk.Button(text='Изменить цель')
        self.show_info_button = tk.Button(text='Показать информацию')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR, command=self.quit)

        # Привязываем обработчики.
        self.add_category_button.bind('<Button-1>', lambda _: AddCategory(self.db_connection))
        self.edit_category_button.bind('<Button-1>', lambda _: EditCategory(self.db_connection))
        self.add_target_button.bind('<Button-1>', lambda _: AddTarget(self.db_connection))
        self.edit_target_button.bind('<Button-1>', lambda _: EditTarget(self.db_connection))
        self.show_info_button.bind('<Button-1>', lambda _: ShowInfo(self.db_connection))

        # Пакуем виджеты.
        self.add_category_button.pack(expand=3)
        self.edit_category_button.pack(expand=3)
        self.add_target_button.pack(expand=3)
        self.edit_target_button.pack(expand=3)
        self.show_info_button.pack(expand=3)
        self.exit_button.pack(expand=3)


def main():
    """Функция, запускающая весь код."""
    MainWindow('Главное окно').mainloop()


if __name__ == '__main__':
    main()
else:
    print('Спасибо, что решили использовать наш проект Counter в своей'
          ' программе.')
