import tkinter
from tkinter import *
from tkinter import filedialog as fd
from tkinter.ttk import *
import sqlite3
import time

# Создание БД
def new_base():
    global file_name
    global root
    global isNew
    isNew = True
    file_name = fd.asksaveasfilename(filetypes=(('PowerLiftingDB Files', '*.pldb'),), defaultextension='.pldb')
    if not file_name == '':
        start_main()



# Открытие БД
def open_base():
    global file_name
    file_name = fd.askopenfilename(
        filetypes=(('PowerLiftingDB Files', '*.pldb'),))
    if not file_name == '':
        start_main()

def save_base(pldb,data):
    global isNew
    conn = sqlite3.connect(pldb)
    cursor = conn.cursor()
    if isNew:
        cursor.execute('CREATE TABLE "Men" ("ID"	INTEGER,\
	        "Name"	TEXT,\
	        "Birth"	NUMERIC,\
	        "Wieght"	REAL,\
	        "Category"	INTEGER,\
	        "Height"	INTEGER,\
	        "Try1"	REAL,\
	"Done1"	INTEGER DEFAULT 0,\
	"Try2"	REAL,\
	"Done2"	INTEGER DEFAULT 0,\
	"Try3"	REAL,\
	"Done3"	INTEGER DEFAULT 0,\
	"Result"	INTEGER,\
	"Place"	INTEGER,\
	"Razryad"	TEXT,\
	"City"	TEXT,\
	"Organization"	TEXT,\
	"Trainer"	TEXT\
);')
        isNew = False
    else:
        cursor.execute('Delete FROM Men')
    conn.commit()
    cursor.executemany('INSERT INTO Men VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', data)
    conn.commit()
    conn.close()
    bSave.configure(state=DISABLED)

# Чтение из БД
def que(pldb):
    conn = sqlite3.connect(pldb)
    cursor = conn.cursor()

    cursor.execute('Select * FROM Men')

    res = cursor.fetchall()

    conn.close()
    return res

def add_widget(sel):
    global widget
    global entries
    global num
    global headersParticipants
    global bAdd
    global bDel
    global bSave
    global bEdit
    global fDataP

    if widget == W_MAIN:
        bAdd.configure(text='ОК')
        bDel.configure(text='Отмена', state=ACTIVE)
        bEdit.configure(state=DISABLED)
        bGo.configure(state=DISABLED)
        bSave.configure(state=DISABLED)
        widget = W_ADD
        for k in fDataP.children.values():
            k.grid_forget()

        # Виджет добавления
        entries = []
        for k, cell in enumerate(headersParticipants[1:]):
            Label(fDataP, text=cell[0], borderwidth=3, relief=GROOVE, width=20, anchor='e').grid(row=k, column=0)
            if cell[0] in {'Р1', 'Р2', 'Р3'}:
                entries.append(Combobox(fDataP, values=['Обнулить', 'Удачно', 'Неудачно', 'Отказ'], width=36))
                if sel != -1:
                    entries[k].insert(0, data[sel][k+1])
            elif cell[0] =='Весовая категория':
                entries.append(Combobox(fDataP, values=['59', '66', '74', '83', '93', '93+'], width=36))
                if sel != -1:
                    entries[k].insert(0, data[sel][k+1])
            elif cell[0] == 'Разряд':
                entries.append(Combobox(fDataP, values=['Б/Р', '3Ю', '2Ю', '1Ю', '3', '2', '1', 'КМС', 'МС', 'МСМК'], width=36))
                if sel != -1:
                    entries[k].insert(0, data[sel][k + 1])
                else:
                    entries[k].current(0)
            else:
                entries.append(Entry(fDataP, width=36))
                if sel != -1:
                    entries[k].insert(0, data[sel][k+1])
            entries[k].grid(row=k, column=1, columnspan=2)
    elif widget == W_ADD:
        bAdd.configure(text='Добавить')
        widget = W_MAIN
        if sel == -1:
            num += 1
            row = [num]
            for k, ent in enumerate(entries):
                if k in {6, 8, 10}:
                    row.append((RES[ent.get()]))
                else:
                    row.append(ent.get())
            data.append(row)
        else:
            row = [data[sel][0]]
            for k, ent in enumerate(entries):
                if k in {6, 8, 10}:
                    row.append(RES[ent.get()])
                else:
                    row.append(ent.get())
            data[sel] = row

        update_table(data)

# Виджет Попытка
def att_widget():
    global widget
    global entries
    global num
    global headersParticipants
    global bAdd
    global bDel
    global bSave
    global bEdit
    global bGo
    global fDataP
    global rowsAtt
    global clock
    global currentAtt
    global atts

    clock = False

    if widget == W_TIMER:
        update_table(data)
    else:
        bAdd.configure(state=DISABLED)
        bGo.configure(text='Вернуться')
        bEdit.configure(state=DISABLED)
        bSave.configure(state=DISABLED)
        bDel.configure(state=DISABLED)
        widget = W_TIMER
        for k in fDataP.children.values():
            k.grid_forget()

        att = 1
        for i, row in enumerate(rowsAtt):
            Label(fDataP, text=row[0], font='bold').grid(row=i, column=0)
            if i == 0:
                Label(fDataP, text=data[atts[currentAtt][0]][1], font='bold').grid(row=i, column=1)
            elif i == 2:
                Label(fDataP, text=atts[currentAtt][1]).grid(row=i, column=1)
                rowsAtt[i+1][1] = 6 + 2 * (atts[currentAtt][1] - 1)
            else:
                Label(fDataP, text=data[atts[currentAtt][0]][row[1]]).grid(row=i, column=1)
        lTimer = Label(fDataP, text=60, font=('Arial', 24, 'bold'))
        lTimer.grid(row=0, column=2)
        bStart = Button(fDataP, text = 'Старт/Сброс', command=lambda: set_timer(lTimer, True))
        bUd = tkinter.Button(fDataP, text='Удачно', bg='green', command=lambda: next(1))
        bNeud = tkinter.Button(fDataP, text='Неудачно', bg='red', command=lambda: next(2))
        bOtk = tkinter.Button(fDataP, text='Отказ', bg='gray', command=lambda: next(3))
        bStart.grid(row=1, column=2)
        bUd.grid(row=2, column=2)
        bNeud.grid(row=3, column=2)
        bOtk.grid(row=4, column=2)

def set_timer(lab,flag):
    global clock
    if flag:
        clock = not clock
    if clock:
        if int(lab['text']) > 0:
            lab.configure(text=int(lab['text']) - 1)
            root.after(1000, lambda: set_timer(lab, False))
    else:
        lab.configure(text=60)

def next(res):
    global data
    global currentAtt
    global atts

    i = atts[currentAtt][0]
    j = atts[currentAtt][1]*2 + 5
    data[i] = list(data[i])
    data[i][j] = res

    update_table(data)
    att_widget()


def cancel():
    global widget
    global select
    global bAdd
    if widget == W_MAIN:
        if len(data) > 0:
            data.pop(select)
            print(data)
            select = -1
            update_table(data)
    elif widget == W_ADD:
        bAdd.configure(text='Добавить')
        bDel.configure(text='Удалить')
        widget = W_MAIN
        update_table(data)




# Выбор строки для редактирования или удаления
def col_cell(ev, row):
    global select
    if not row == select:
        if not select == -1:
            for i in dataCells[select]:
                i.configure(relief=GROOVE)
        for i in dataCells[row]:
            i.configure(relief=SUNKEN)
        select = row
        bEdit.configure(state=NORMAL)
        bDel.configure(state=NORMAL)

# Обновление главного экрана, виджеты Таблица и Подходы
def update_table(data1):
    global fDataP
    global fDataA
    global dataCells
    global bSave
    global widget
    global currentAtt
    global atts
    global select
    select = -1

    bSave.configure(state=NORMAL)
    bEdit.configure(state=DISABLED)
    bAdd.configure(state=ACTIVE)
    bDel.configure(state=DISABLED)
    bGo.configure(text='Попытка', state=ACTIVE)
    widget = W_MAIN

    for k in fDataP.children.values():
        k.grid_forget()
    for k in fDataA.children.values():
        k.grid_forget()

    dataCells = []
    atts = []
    data1.sort(key=lambda r: (str(r[4]), r[0]))

    ir = 0
    vk = -1
    ivk = -1


    for i, row in enumerate(data1):
        if str(data1[i][4]) != vk:
            vk = str(data1[i][4])
            Label(fDataP, text=f'Весовая категория {vk} кг').grid(row=ir, column=0, columnspan=18)
            ir += 1
            ivk += 1
        dataCells.append([])
        atts.append([i, 1, row[7], row[4]])
        atts.append([i, 2, row[9], row[4]])
        atts.append([i, 3, row[11], row[4]])
        j = 0

        for k, col in enumerate(headersParticipants):
            if col[1] > 0:
                dataCells[i].append(Label(fDataP, text=row[k], width=col[1],
                                          borderwidth=3, relief=GROOVE))
                dataCells[i][j].bind('<Button-1>', lambda ev, row=i: col_cell(ev, row))
                dataCells[i][j].grid(row=ir, column=j)
                j += 1
            elif k in {7, 9, 11}:
                if row[k] == 1:
                    dataCells[i][j - 1].configure(background='green')
                elif row[k] == 2:
                    dataCells[i][j - 1].configure(background='red')
                elif row[k] == 3:
                    dataCells[i][j - 1].configure(background='darkgray')
        ir += 1

    # Попытки
    atts.sort(key = lambda r: (str(r[3]), r[1]))
    currentAtt = -1

    for i, att in enumerate(atts):
        bg = ''
        if att[2] == 1:
            bg = 'green'
        elif att[2] == 2:
            bg = 'red'
        elif att[2] == 3:
            bg = 'gray'
        else:
            bg = ''
            if currentAtt == -1:
                currentAtt = i
        Label(fDataA, text=data[att[0]][0], width=headersAtts[0][1], background=bg, borderwidth=3, relief=GROOVE).grid(row=i, column=0)
        Label(fDataA, text=data[att[0]][1], width=headersAtts[1][1], background=bg, borderwidth=3, relief=GROOVE).grid(row=i, column=1)
        Label(fDataA, text=data[att[0]][4 + att[1] * 2], width=headersAtts[2][1], background=bg, borderwidth=3, relief=GROOVE).grid(row=i, column=2)
        Label(fDataA, text=att[1], width=headersAtts[3][1], background=bg, borderwidth=3, relief=GROOVE).grid(row=i, column=3)


# Главное окно
def start_main():
    global root
    global file_name
    global isNew
    global select
    # W_INTRO, W_MAIN, W_ADD, W_TIMER = range(4)
    # RES = {'': '0', 'Удачно': '1', 'Неудачно': '2', 'Отказ': '3'}
    global widget
    global num
    global entries
    global dataCells
    global data
    global headersParticipants
    global headersAtts
    global bAdd
    global fDataP
    global fDataA
    global bEdit
    global bDel
    global bSave
    global bGo


    root.destroy()
    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()

    root.title('Пауэрлифтинг')

    root.iconbitmap('pl.ico')
    root.geometry(f'{w // 8 * 7}x{h // 2}+{w // 10}+{h // 8}')

    # виджет Участники
    fMen = LabelFrame(root, text='Участники')
    fMen.pack(side=LEFT, fill=BOTH, expand=1)

    # фрейм Таблица
    fTableP = Frame(fMen)
    fTableP.pack()
    # Заголовки
    headersParticipants = [['№', 3, '1'], ['Участник', 20, 'Петр Иванов'], ['Г. р.', 4, '1992'],
                           ['Вес', 3, '56,5'], ['Весовая категория',0,'59'], ['Выс.с.', 5, '5'], ['П1', 4, '80'],
                           ['Р1', 0, '1'], ['П2', 4, '85'], ['Р2', 0, '2'], ['П3', 4, '88'], ['Р3', 0, '3'],
                           ['Итог', 4, '  '], ['Место', 5, '  '], ['Разряд', 6, 'КМС'], ['Город', 10, 'Иркутск'],
                           ['ДСО', 10, 'ИрГТУ'], ['Тренер', 15, 'Анисимов В.В.']]

    i = 0
    for cell in headersParticipants:
        if cell[1] > 0:
            Label(fTableP, text=cell[0], borderwidth=3, relief=GROOVE, width=cell[1], anchor='n').grid(row=0, column=i)
            i += 1
    colNum = i

    # Холст с данными
    cTable = Canvas(fTableP, background='blue')
    fDataP = Frame(cTable)
    scrollTable = Scrollbar(fTableP, orient=VERTICAL, command=cTable.yview)
    cTable.create_window((0, 0), window=fDataP, anchor="nw")
    cTable.configure(yscrollcommand=scrollTable.set)
    fDataP.bind(
        "<Configure>",
        lambda e: cTable.configure(
            scrollregion=cTable.bbox("all")
        )
    )
    cTable.grid(row=1, column=0, sticky=N+S+W+E, columnspan=colNum)
    # Полоса прокрутки
    scrollTable.grid(row=1, column=colNum, sticky=N+S)

    # Фрейм кнопки
    fButtonsP = Frame(fMen)
    fButtonsP.pack(side=BOTTOM)

    bAdd = Button(fButtonsP, text='Добавить', command=lambda: add_widget(select))
    bEdit = Button(fButtonsP, text='Редактировать', command=lambda: add_widget(select), state=DISABLED)
    bDel = Button(fButtonsP, text='Удалить', command=cancel, state=DISABLED)
    bSave = Button(fButtonsP, text='Сохранить', command=lambda:save_base(file_name,data))
    bGo = Button(fButtonsP, text='Попытка', command=att_widget)
    bAdd.grid()
    bEdit.grid(row=0, column=1)
    bDel.grid(row=0, column=2)
    bSave.grid(row=0, column=3)
    bGo.grid(row=0, column=4)




    # виджет Подходы
    fAtt = LabelFrame(root, text='Подходы')

    fAtt.pack(side=LEFT, fill=BOTH, expand=1)

    # фрейм Таблица
    fTableA = Frame(fAtt)
    fTableA.pack()
    # Заголовки
    headersAtts = [['№', 3, 0], ['Участник', 25, 1], ['Вес', 10, 3], ['Подход', 10, '1']]

    i = 0
    for cell in headersAtts:
        Label(fTableA, text=cell[0], borderwidth=3, relief=GROOVE, width=cell[1], anchor='n').grid(row=0, column=i)
        i += 1
    colNum = i

    # Холст с данными
    cAtt = Canvas(fTableA, background='blue', width=50)
    fDataA = Frame(cAtt)
    scrollAtt = Scrollbar(fTableA, orient=VERTICAL, command=cAtt.yview)
    cAtt.create_window((0, 0), window=fDataA, anchor="nw")
    cAtt.configure(yscrollcommand=scrollAtt.set)
    fDataA.bind(
        "<Configure>",
        lambda e: cAtt.configure(
            scrollregion=cAtt.bbox("all")
        )
    )
    cAtt.grid(row=1, column=0, sticky=N+S+W+E, columnspan=colNum)
    # Полоса прокрутки
    scrollAtt.grid(row=1, column=colNum, sticky=N+S)

    # Данные участников
    if isNew:
        data = []
    else:
        data = que(file_name)
        num = max([i[0] for i in data])
    update_table(data)
    bSave.configure(state=DISABLED)




# глобальные переменные
file_name: str = ''
isNew = False
select = -1
W_INTRO, W_MAIN, W_ADD, W_TIMER = range(4)
RES = {'': 0, 'Удачно': 1, 'Неудачно': 2, 'Отказ': 3}
widget = W_MAIN
num = 0
entries = []
dataCells = []
data = []
headersParticipants = []
headersAtts = []
bAdd = None
fDataP = None
fDataA = None
bEdit = None
bDel = None
bSave = None
bGo = None
rowsAtt = [['', 1], ['Разряд:', 14], ['Жим:', -1], ['Заявленный вес:', 6], ['Высота стоек:', 5],
           ['Город:', 15], ['ДСО:', 16]]
atts = []
currentAtt = -1
clock = False

# Начало
root = Tk()
w = root.winfo_screenwidth()
h = root.winfo_screenheight()

root.title('Пауэрлифтинг')

root.iconbitmap('pl.ico')
root.geometry(f'{w // 4}x{h // 4}+{w // 2}+{h // 4}')
root.configure(bg='gray')
# Картинка
canvas = Canvas(root, height=150, width=w // 2, bg='gray', highlightbackground = 'gray')
img = PhotoImage(file='pl.png')
image = canvas.create_image(0, 0, anchor='nw', image=img)
canvas.pack()

#Кнопки
bNew = Button(root, text='Создать...', command=new_base)
bNew.pack()
bOpen = Button(root, text='Открыть...', command=open_base)
bOpen.pack()


root.mainloop()
