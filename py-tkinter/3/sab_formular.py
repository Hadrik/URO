# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
import MultiListbox as table


data = [
       ["Petr", "Bílý","045214/1512", "17. Listopadu", 15, "Ostrava", 70800,"poznamka"],
       ["Jana", "Zelený","901121/7238", "Vozovna", 54, "Poruba", 78511,""],
       ["Karel", "Modrý","800524/5417", "Porubská", 7, "Praha", 11150,""],
       ["Martin", "Stříbrný","790407/3652", "Sokolovská", 247, "Brno", 54788,"nic"]]


class App:

    def __init__(self, root):
        self.mlb = table.MultiListbox(root, (('Jméno', 20), ('Příjmení', 20), ('Rodné číslo', 12)))
        for i in range(len(data)):
            self.mlb.insert(END, (data[i][0], data[i][1],data[i][2]))
        self.mlb.pack(expand=YES,fill=BOTH, padx=10, pady=10)
        self.mlb.subscribe( lambda row: self.edit( row ) )


        self.jprcBox = Frame(root, width=100)
        self.jmenoInput = Entry(self.jprcBox)
        self.jmenoLabel = Label(self.jprcBox, text="Jméno:", padx=10)
        self.prijmeniInput = Entry(self.jprcBox)
        self.prijmeniLabel = Label(self.jprcBox, text="Příjmení:", padx=10)
        self.rcInput = Entry(self.jprcBox)
        self.rcLabel = Label(self.jprcBox, text="Rodné číslo:", padx=10)
        self.jmenoLabel.grid(column=0, row=0, sticky=E)
        self.jmenoInput.grid(column=1, row=0, sticky=W)
        self.prijmeniLabel.grid(column=0, row=1, sticky=E)
        self.prijmeniInput.grid(column=1, row=1, sticky=W)
        self.rcLabel.grid(column=0, row=2, sticky=E)
        self.rcInput.grid(column=1, row=2, sticky=W)
        self.jprcBox.pack()


        self.nb = ttk.Notebook(root)
        self.nb.pack(fill=BOTH, padx=5, pady=5)

        self.p1 = Frame(self.nb)
        self.silenyWrapper = Frame(self.p1)
        self.uliceInput = Entry(self.silenyWrapper, width=10)
        self.uliceLabel = Label(self.p1, text="Ulice:", padx=10)
        self.uliceInput.grid(column=0, row=0, sticky=W)
        self.uliceLabel.grid(column=0, row=0, sticky=E)

        self.cpWrapper = Frame(self.silenyWrapper)
        self.cpInput = Entry(self.cpWrapper, width=8)
        self.cpLabel = Label(self.cpWrapper, text="č. p.:", padx=10)
        self.cpInput.grid(column=1, row=0, sticky=W)
        self.cpLabel.grid(column=0, row=0, sticky=E)
        self.cpWrapper.grid(column=1, row=0, sticky=E)

        self.silenyWrapper.grid(column=1, row=0, sticky=W)

        self.mestoInput = Entry(self.p1, width=27)
        self.mestoLabel = Label(self.p1, text="Město:", padx=10)
        self.mestoInput.grid(column=1, row=1, sticky=W)
        self.mestoLabel.grid(column=0, row=1, sticky=E)

        self.pscInput = Entry(self.p1, width=7)
        self.pscLabel = Label(self.p1, text="PSČ:", padx=10)
        self.pscInput.grid(column=1, row=2, sticky=W)
        self.pscLabel.grid(column=0, row=2, sticky=E)

        self.p2 = Frame(self.nb)

        self.nb.add(self.p1, text="Adresa")
        self.nb.add(self.p2, text="Poznámka")

        self.poznamka = Text(self.p2, height=5, width=20)
        self.poznamka.pack(expand=1,fill=BOTH)


        self.buttons = Frame(root)
        self.cancelbtn = Button(self.buttons, command=self.cancel)
        self.newbtn = Button(self.buttons, command=self.new)
        self.savebtn = Button(self.buttons, command=self.save)

        self.menubar = Menu(root)
    
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Konec", command=root.quit)
        self.menubar.add_cascade(label="Soubor", menu=self.filemenu)

        root.config(menu=self.menubar)

    def cancel(self):
        self.jmenoInput.delete(0, END)
        self.prijmeniInput.delete(0, END)
        self.rcInput.delete(0, END)
        self.uliceInput.delete(0, END)
        self.cpInput.delete(0, END)
        self.mestoInput.delete(0, END)
        self.pscInput.delete(0, END)

    def new(self):


    def save(self):

        
    def read(self):
        self.jmenoInput.get()
        self.prijmeniInput.get()
        self.rcInput.get()
        self.uliceInput.get()
        self.cpInput.get()
        self.mestoInput.get()
        self.pscInput.get()

    def edit(self, row):
        self.cancel()
        self.jmenoInput.insert(0, data[row][0])
        self.prijmeniInput.insert(0, data[row][1])
        self.rcInput.insert(0, data[row][2])
        self.uliceInput.insert(0, data[row][3])
        self.cpInput.insert(0, data[row][4])
        self.mestoInput.insert(0, data[row][5])
        self.pscInput.insert(0, data[row][6])
        # self.poznamka.insert(0, "kokot")


root = Tk()
root.wm_title("Formulář")
app = App(root)
root.mainloop()

