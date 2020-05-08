import tkinter as tk
from config import ERROR_COLOR
from checker import check


class EditTarget(tk.Toplevel):
    def __init__(self, db_connection, width=None, height=None):
        super().__init__()
        self.title('Экран изменения цели')
        if width and height:
            self.geometry(f'{width}x{height}')
        self.db_connection = db_connection
        self._add_widgets()

    def _update_value(self):
        # Создаём объект типа Cursor для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()

    def _update_target(self):
        # Получаем значение, введённое пользователем.
        value = check('value', self.value_label, self.value_entry)
        selection = check('selection', label=self.list_label, lbox=self.targets_list)
        if value is None or selection is None:
            return

        # Создаём курсор для взаимодействия с базой данных.
        cursor = self.db_connection.cursor()
        # Получаем название категории и её значение из базы данных.
        element = cursor.execute('SELECT * FROM targets').fetchall()[selection]
        name, current_value, target = element
        current_value += value
        cursor.execute('UPDATE targets SET current_value = ? WHERE name = ?', (current_value, name))

        # Записываем изменения в базу данных.
        self.db_connection.commit()
        self.destroy()

    def _add_widgets(self):
        # Создаём виджеты
        self.list_label = tk.Label(self, text='Выберите цель из списка ниже')
        self.targets_list = tk.Listbox(self)
        self._fill_list(self.targets_list)
        self.value_label = tk.Label(self, text='Введите значение, которое хотите прибавить/отнять у цели')
        self.value_entry = tk.Entry(self)
        self.enter_button = tk.Button(self, text='Ввод!')
        self.exit_button = tk.Button(self, text='ВЫХОД', bg=ERROR_COLOR, command=self.destroy)

        # Привязываем обработчики событий
        self.enter_button.bind('<Button-1>', lambda event: self._update_target())

        # Пакуем виджеты
        self.list_label.pack()
        self.targets_list.pack()
        self.value_label.pack()
        self.value_entry.pack()
        self.enter_button.pack()
        self.exit_button.pack()

    def _fill_list(self, listbox):
        # Создаём курсор для взаимодействия с базой данных
        cursor = self.db_connection.cursor()

        # Получаем названия текущих целей
        elements = cursor.execute('SELECT name FROM targets').fetchall()
        elements = [element[0] for element in elements]

        # Вставляем названия в Listbox
        for element in elements:
            listbox.insert(tk.END, element)
