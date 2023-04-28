import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from homework import homework

def search():
    def func():
        result = homework(login.get(), password.get())
        output.configure(state='normal')
        output.delete('1.0', tk.END)
        output.insert(tk.END, result)
        output.configure(state='disabled')
        message.configure(text='Готово')
        btn.configure(state='enabled')

    btn.configure(state='disabled')
    message.configure(text='Ищем дз...')
    threading.Thread(target=func).start()


root = tk.Tk()

root.geometry('600x700')
root.iconbitmap('etc/icon.ico')
root.title('Homeworks')

title = ttk.Label(root, text='Получить Д/З', font=('Arial Bold', '15', 'bold'))
title.place(relx=0.36, rely=0.13)
instr = ttk.Label(root, text='Введите логин и пароль от вашего аккаунта.\nЗатем войдите и ждите загрузки вашего Д/З')
instr.place(relx=0.24, rely=0.2)
login = ttk.Entry(root)
login.place(relx=0.35, rely=0.33)
password = ttk.Entry(root, show='●')
password.place(relx=0.35, rely=0.38)
btn = ttk.Button(root, text='ВОЙТИ', command=search)
btn.place(relx=0.41, rely=0.45)
today = ttk.Label(root, text=f'Сегодня: {datetime.now().strftime("%d.%m.%y / %a")}')
today.place(relx=0.05)
message = ttk.Label(root, font='Georgia')
message.place(relx=0.43, rely=0.9)
output = tk.Text(root, width=48, height=10, state='disabled')
output.place(relx=0.1, rely=0.57)

root.mainloop()