"""Модуль для добавления новой цели в базу данных."""

import tkinter as tk
from settings import ERROR_COLOR


class AddTarget(tk.Toplevel):
    """Класс для добавления новой цели в базу данных."""
    def __init__(self, db_connection, width=None, height=None):
        super().__init__()
        self.db_connection = db_connection
        self.title('Экран добавления цели')
        if width and height:
            self.geometry(f'{width}x{height}')
        self._add_widgets()

    def _get_name(self, name_label, name_entry):
        if len(name_entry.get()) == 0:
            name_label.config(text='Вы не ввели название',
                              bg=ERROR_COLOR)
            return
        
        if not name_entry.get().replace(' ', '').isalpha():
            name_label.config(text='Вы ввели название в неправильно формате',
                              bg=ERROR_COLOR)
            return

        return name_entry.get()

    def _get_value(self, value_label, value_entry):
        if len(value_entry.get()) == 0:
            value_label.config(text='Вы не ввели значение',
                               bg=ERROR_COLOR)

            return

        if not value_entry.get().isdigit():
            value_label.config(text='Значение должно состоять только из цифр',
                               bg=ERROR_COLOR)
            return

        return int(value_entry.get())

    def _add_target(self, name_label, name_entry, value_label, value_entry):
        # Получаем данные, введённые пользователем.
        name = self._get_name(name_label, name_entry)
        value = self._get_value(value_label, value_entry)

        if not name or not value:
            # Если название или значение введено в неправильном формате,
            # то прерываем выполнение.
            return

        # Создаём объект типа Cursor для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()
        # Получаем названия уже созданных целей.
        names = cursor.execute('SELECT name FROM targets').fetchall()
        names = [name[0] for name in names]
        
        if name in names:
            name_label.config(text='Цель с таким названием уще существует.',
                              bg=ERROR_COLOR)
            return
        
        cursor.execute(f'INSERT INTO targets VALUES ("{name}", {0}, {value})')
        # Сохраняем изменения.
        self.db_connection.commit()
        self.destroy()

    def _add_widgets(self):
        # Создаём виджеты.
        self.name_label = tk.Label(self, text='Введите ниже название цели')
        self.name_entry = tk.Entry(self)
        self.target_label = tk.Label(self, text='Введите ниже значение для цели')
        self.target_entry = tk.Entry(self)
        self.enter_button = tk.Button(self, text='Ввод!')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR,
                                     command=self.destroy)

        # Привязываем обработчкики событий.
        self.enter_button.bind('<Button-1>', lambda event: self._add_target(self.name_label,
                                                                            self.name_entry,
                                                                            self.target_label,
                                                                            self.target_entry))

        # Пакуем виджеты.
        self.name_label.pack()
        self.name_entry.pack()
        self.target_label.pack()
        self.target_entry.pack()
        self.enter_button.pack()
        self.exit_button.pack()
