"""Модуль для проверки пользовательского ввода."""

from config import ERROR_COLOR


def check(check_type, label=None, entry=None, lbox=None):
    """Функция для проверки пользовательского ввода.

    label_widget - объект типа tkinter.Label, в который будут передаваться сообщения об ошибках.
    entry_widget - объект типа tkinter.Entry, из которого будет считываться ввод.
    type - тип проверки. 'name' - для названий, 'value' - для числовых значений.
    """
    if check_type == 'value':
        # Проверка числового значения.
        if len(entry.get()) == 0:
            # Если строка пустая, то возвращаем None.
            label.config(text='Вы не ввели значение', bg=ERROR_COLOR)
            return

        try:
            return int(entry.get())
        except ValueError:
            label.config(text='Вы ввели не число', bg=ERROR_COLOR)

        # Если всё хорошо, то возвращаем пользовательский ввод, приведённый к числу.
    elif check_type == 'name':
        # Проверка строкового значения.
        if len(entry.get()) == 0:
            # Если строка пустая, то возвращаем None.
            label.config(text='Вы не ввели название', bg=ERROR_COLOR)
            return

        if not entry.get().replace(' ', '').isalpha():
            # Если строка не состоит из букв и пробелов, то возвращаем None.
            label.config(text='Вы ввели название в неправильном формате',
                                bg=ERROR_COLOR)
            return

        # Если всё хорошо, то возвращаем строку, введённую пользователем.
        return entry.get()
    elif check_type == 'selection':
        selection = lbox.curselection()
        if selection:
            return selection[0]
        else:
            label.config(text='Вы не выбрали ничего в списке ниже!', bg=ERROR_COLOR)
            return
