"""

© Copyright 2023 Kalmyk1902
Распространяется по лицензии Apache 2.0


"""
# импортируем нужные библиотеки
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from homework import homework

# функция выдачи домашки
def search():
    def func(): # основная функция
        result = homework(login.get(), password.get()) # ищем домашку (см. homework.py)
        output.configure(state='normal') # временно включаем окно результатов
        output.delete('1.0', tk.END) # очищаем его
        output.insert(tk.END, result) # вставляем результат
        output.configure(state='disabled') # обратно выключаем окно
        message.configure(text='Готово') # сообщаем пользователю о завершении поиска
        btn.configure(state='enabled') # включаем кнопку обратно

    btn.configure(state='disabled') # временно выключаем кнопку
    message.configure(text='Ищем дз...') # сообщаем о начале поиска домашки
    threading.Thread(target=func).start() # запускаем поток с основной функцией

root = tk.Tk() # объявляем корневую переменную окна программы

root.geometry('600x700') # задаем размер программы
root.iconbitmap('etc/icon.ico') # задаем иконку
root.title('Homeworks') # задаем название программе

# настраиваем интерфейс программы
title = ttk.Label(root, text='Получить Д/З', font=('Arial Bold', '15', 'bold')) # имя программы
title.place(relx=0.36, rely=0.13) # размещаем
instr = ttk.Label(root, text='Введите логин и пароль от вашего аккаунта.\nЗатем войдите и ждите загрузки вашего Д/З') # инструкции
instr.place(relx=0.24, rely=0.2) # размещаем
login = ttk.Entry(root) # поле ввода логина
login.place(relx=0.35, rely=0.33) # размещаем
password = ttk.Entry(root, show='●') # поле ввода пароля
password.place(relx=0.35, rely=0.38) # размещаем
btn = ttk.Button(root, text='ВОЙТИ', command=search) # кнопка поиска
btn.place(relx=0.41, rely=0.45) # размещаем
today = ttk.Label(root, text=f'Сегодня: {datetime.now().strftime("%d.%m.%y / %a")}') # сегодняшняя дата и день недели
today.place(relx=0.05) # размещаем
message = ttk.Label(root, font='Georgia') # сообщения о начале и конце поиска
message.place(relx=0.43, rely=0.9) # размещаем
output = tk.Text(root, width=48, height=10, state='disabled') # окно результатов
output.place(relx=0.1, rely=0.57) # размещаем

root.mainloop() # запускаем программу