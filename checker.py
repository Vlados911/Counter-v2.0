"""Модуль для проверки пользовательского ввода."""

from settings import ERROR_COLOR

def check(label_widget, entry_widget, check_type):
    """Функция для проверки пользовательского ввода.

    label_widget - объект типа tkinter.Label, в который будут передаваться сообщения об ошибках.
    entry_widget - объект типа tkinter.Entry, из которого будет считываться ввод.
    type - тип проверки. 'name' - для названий, 'value' - для числовых значений.
    """
    if check_type == 'value':
        # Проверка числового значения.
        if len(entry_widget.get()) == 0:
            # Если строка пустая, то возвращаем None.
            label_widget.config(text='Вы не ввели название', bg=ERROR_COLOR)
            return

        if not entry_widget.get().isdigit():
            # Если строка не состоит только из цифр, то возвращаем None.
            label_widget.config(text='Значение должно состоять только из цифр',
                                bg=ERROR_COLOR)
            return

        # Если всё хорошо, то возвращаем пользовательский ввод, приведённый к числу.
        return int(entry_widget.get())
    elif check_type == 'name':
        # Проверка строкового значения.
        if len(entry_widget.get()) == 0:
            # Если строка пустая, то возвращаем None.
            label_widget.config(text='Вы не ввели название', bg=ERROR_COLOR)
            return

        if not entry_widget.get().replace(' ', '').isalpha():
            # Если строка не состоит из букв и пробелов, то возвращаем None.
            label_widget.config(text='Вы ввели название в неправильном формате',
                                bg=ERROR_COLOR)
            return

        # Если всё хорошо, то возвращаем строку, введённую пользователем.
        return entry_widget.get()
