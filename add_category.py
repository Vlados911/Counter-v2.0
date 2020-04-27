"""Модуль для добавления категорий в базу данных."""

import tkinter as tk
from settings import ERROR_COLOR


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
        self.add_widgets()

    def _get_name(self, label_widget, entry_widget):
        """
        Метод, который проверяет поле ввода для названия категории.

        Принимает Label (для вывода ошибок) и Entry (для получения вводных данных).
        Если название введено в корректном формате, то возвращает название.
        Иначе возвращает False.
        """
        if len(entry_widget.get()) == 0:
            # Не пустая ли строка ввода?
            label_widget.config(text='Введите название категории!',
                                bg=ERROR_COLOR)
            return False

        if not entry_widget.get().replace(' ', '').isalpha():
            # Содержит ли строка только буквы?
            label_widget.config(text='Название категории должно содержать'
                                     ' только буквы и пробелы.',
                                bg=ERROR_COLOR)
            return False

        # Подключаем базу данных и получаем список названий существующих категорий.
        cursor = self.db_connection.cursor()
        names = cursor.execute('SELECT name FROM categories').fetchall()
        names = [name[0] for name in names]

        # Проверяем, не существует ли уже категория с таким именем
        if entry_widget.get() in names:
            label_widget.config(text='Такая категория уже существует,'
                                     ' попробуйте изменить название.',
                                bg=ERROR_COLOR)
            return False

        # Возвращаем содержимое строки ввода, если ни одно из условий не выполнилось.
        return entry_widget.get()

    def _get_value(self, label_widget, entry_widget):
        """
        Метод, который проверяет поле ввода для начального значения категории.

        Принимает Label (для вывода ошибок) и Entry (для получения вводных данных).
        Если значение введено в корректном формате, то возвращает числовое значение.
        Иначе возвращает False.
        """
        if len(entry_widget.get()) == 0:
            # Не пустая ли строка ввода?
            label_widget.config(text='Введите начальное значение для категории!',
                                bg=ERROR_COLOR)
            return False

        if not entry_widget.get().isdigit():
            # Содержит ли строка только цифры?
            label_widget.config(text='Значение может быть только числовым!',
                                bg=ERROR_COLOR)
            return False

        # Возвращаем содержимое строки ввода, если ни одно из условий не выполнилось.
        # Перед этим превращаем содержимое в число.
        return int(entry_widget.get())

    def _add_category(self, name_label, name_entry, value_label, value_entry):
        # Получаем пользовательские значения
        name = self._get_name(name_label, name_entry)
        value = self._get_value(value_label, value_entry)

        if not name or not value:
            # Если название или значение введено в неправильном формате,
            # то прерываем выполнение.
            return

        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()

        cursor.execute(f'INSERT INTO categories VALUES("{name}", {value})')
        self.db_connection.commit()
        self.destroy()

    def add_widgets(self):
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
        self.enter_button.bind('<Button-1>', lambda event: self._add_category(self.name_label,
                                                                              self.name_entry,
                                                                              self.value_label,
                                                                              self.value_entry))

        # Пакуем виджеты
        self.name_label.pack(expand=3, side=tk.TOP)
        self.name_entry.pack(expand=3, side=tk.TOP)
        self.value_label.pack(expand=3, side=tk.TOP)
        self.value_entry.pack(expand=3, side=tk.TOP)
        self.enter_button.pack(expand=3, side=tk.TOP)
        self.exit_button.pack(expand=3, side=tk.BOTTOM)