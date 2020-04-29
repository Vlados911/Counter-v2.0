"""Модуль для отображения списка и информации о созданных категориях."""

import tkinter as tk
from settings import ERROR_COLOR

class ShowCategories(tk.Toplevel):
    """Класс для отображения списка и информации о созданных категориях."""
    def __init__(self, db_connection, width=None, height=None):
        """
        Конструктор класса ShowCategories.

        Принимает подключение базы данных, широту и высоту окна (необяз).
        """
        super().__init__()
        if width and height:
            self.geometry(f'{width}x{height}')
        self.title('Окно просмотра категорий')
        self.db_connection = db_connection
        self._add_widgets()
        self._fill_list(self.list)

    def _fill_list(self, list_widget):
        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()

        # Получаем названия текущих категорий.
        elements = cursor.execute('SELECT name FROM categories').fetchall()
        elements = [element[0] for element in elements]
        
        # Заполняем список.
        for element in elements:
            list_widget.insert(tk.END, element)

    def _key_pressed(self, label_widget, list_widget, text_widget):
        """
        Метод, проверяющий выбрана ли категория в ListBox.

        Принимает объекты типа Label, Listbox, Text.
        """
        # Создаём курсор для взаимодействия с базой данных
        cursor = self.db_connection.cursor()
        # Получаем список названий текущих элементов.
        elements = cursor.execute('SELECT * FROM categories').fetchall()
        if list_widget.curselection():
            # Выводим информацию о категории в текстовое поле.
            index = list_widget.curselection()[0]
            text_widget.insert(1.0, f'Имя категории: {elements[index][0]}')
            text_widget.insert(2.0, f'\nЗначение категории: {elements[index][1]}')
        else:
            label_widget.config(text='Выберите что-нибудь в поле ниже',
                                bg=ERROR_COLOR)

    def _add_widgets(self):
        """Метод, который создаёт виджеты на главном экране."""
        # Создаём виджеты
        self.list_label = tk.Label(self, text='Выберите категорию из списка '
                                              'ниже и нажмите Enter.')
        self.list = tk.Listbox(self)
        # TODO: запаковать этот виджет в дальнейшем.
        self.list_text = tk.Text(self)
        self.enter_button = tk.Button(self, text='Ввод!')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR,
                                     command=self.destroy)

        # Привязываем обработчики
        self.enter_button.bind('<Button-1>', lambda event: self._key_pressed(self.list_label, 
                                                                             self.list,
                                                                             self.list_text))

        # Пакуем виджеты
        self.list_label.pack()
        self.list.pack()
        self.enter_button.pack()
        self.list_text.pack()
        self.exit_button.pack()
