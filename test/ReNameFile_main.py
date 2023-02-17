import os
from tkinter import *
from tkinter import filedialog as fd
from ReNameFileInDir import startRename as re_name


def selectDir():
    global d
    d = fd.askdirectory() + '/'
    ent1.insert(0, d)
    return d


root = Tk()
root.geometry('530x100')
root.title = 'Замінити імена усіх файлів'

b1 = Button(text='Выбрать папку', command=lambda: selectDir())
b1.grid(row=0, column=1)

b2 = Button(text='Перейменувати', command=lambda: re_name(d, ent2.get(), ent3.get()))
b2.grid(row=3, column=1)

ent1 = Entry()
ent1.grid(row=0, column=2)
ent1.configure(width=70)

l2 = Label(text='Що замінити')
l2.grid(row=1, column=1)

ent2 = Entry()
ent2.grid(row=1, column=2)
ent2.configure(width=70)

l3 = Label(text='Чим замінити')
l3.grid(row=2, column=1)

ent3 = Entry()
ent3.grid(row=2, column=2)
ent3.configure(width=70)

root.mainloop()
