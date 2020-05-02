from settings import ERROR_COLOR

def check(label_widget, entry_widget, check_type):
    if check_type == 'value':
        if len(entry_widget.get()) == 0:
            label_widget.config(text='Вы не ввели название', bg=ERROR_COLOR)
            return
        
        if not entry_widget.get().isdigit():
            label_widget.config(text='Значение должно состоять только из цифр',
                                bg=ERROR_COLOR)
            return

        return int(entry_widget.get())
    elif check_type == 'name':
        if len(entry_widget.get()) == 0:
            label_widget.config(text='Вы не ввели название', bg=ERROR_COLOR)
            return

        if not entry_widget.get().replace(' ', '').isalpha():
            label_widget.config(text='Вы ввели название в неправильном формате',
                                bg=ERROR_COLOR)
            return

        return entry_widget.get()
