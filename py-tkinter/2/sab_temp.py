# -*- coding: utf-8 -*-

from tkinter import *
from math import sqrt
import tkinter.font

class myApp:

    def prevod(self, event=None):
        v = float(self.ent_in.get())
        print(self.dir.get())
        self.ent_out.delete(0, END)
        if self.dir.get() == 0:
            v = v * 9/5 + 32
        else:
            v = (v - 32) * 5/9
        
        self.ent_out.insert(0, str(round(v, 2)))
        y = self.map_value(v, -20, 50, 292, 80)
        y = max(80, min(292, y))
        self.ca.coords(self.r , 146, 292, 152, y)

    def __init__(self, root):

        root.title('Převodník teplot')
        root.resizable(False, False)
        root.bind('<Return>', self.prevod)        

        def_font = tkinter.font.nametofont("TkDefaultFont")
        def_font.config(size=16)

        self.left_frame = Frame(root)
        self.right_frame = Frame(root)
        
        self.dir = IntVar()
        self.dir.set(1)
        
        self.radio_frame = LabelFrame(self.left_frame, text= "Směr převodu")
        
        self.radio_ctf = Radiobutton(self.radio_frame, text="C -> F", variable=self.dir, value=0)
        self.radio_ftc = Radiobutton(self.radio_frame, text="F -> C", variable=self.dir, value=1)
        self.radio_ctf.pack(side="left")
        self.radio_ftc.pack(side="right")
        
        
        self.ent_frame = Frame(self.left_frame, bd=2, relief="groove")
        
        self.lbl_in = Label(self.ent_frame, text="Vstup")
        self.ent_in = Entry(self.ent_frame, width=10, font = def_font)
        self.ent_in.insert(0, '0')
        
        self.lbl_out = Label(self.ent_frame, text="Výstup")
        self.ent_out = Entry(self.ent_frame, width=10, font = def_font)
        self.ent_out.insert(0, '0')
        
        self.btn = Button(self.ent_frame, text="Převést", command=self.prevod)
        # self.me = Label(self.ent_frame, text="Richard Trávníček (TRA0117)", font=("Arial", 8))

        self.ca = Canvas(self.right_frame, width=300, height=400)
        self.photo = PhotoImage(file="th_empty.png")
        self.ca.create_image(150, 200, image=self.photo)
        self.r = self.ca.create_rectangle(146, 292, 152, 80, fill="blue")

        self.left_frame.pack(side="left", fill=Y, padx=5, pady=5)
        self.right_frame.pack(side="right")
        self.radio_frame.pack(fill=X, padx=5, pady=5)
        self.ent_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.lbl_in.pack()
        self.ent_in.pack()
        self.lbl_out.pack()
        self.ent_out.pack()
        # self.me.pack(side="bottom", pady=10)
        self.btn.pack(side="bottom", pady=5)
        self.ca.pack()

        self.ent_in.focus_force()

    @staticmethod
    def map_value(value, source_min, source_max, target_min, target_max):
        return target_min + ((value - source_min) * (target_max - target_min) / (source_max - source_min))

root = Tk()
app = myApp(root)
root.mainloop()

