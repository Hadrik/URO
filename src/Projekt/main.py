from idlelib.mainmenu import menudefs
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.font import Font
from typing import TypedDict, Callable, Optional
from typing import NewType
import json

class Data(TypedDict):
    id: str
    name: str
    price: int
    info: str

DataList = NewType('DataList', list[Data])

class App:
    data: DataList
    path: str = './data.json'

    def __init__(self, root: Tk):
        root.option_add('*Font', Font(family='Helvetica', size=14))

        self.load_data()

        # Notebook
        self.notebook = ttk.Notebook(root)

        self.n_add = Frame()
        self.n_add.pack(fill=Y)
        self.add_view = self.Add(self.n_add)
        self.add_view.on_add(self.add_entry)

        self.n_info = Frame()
        self.n_info.pack(fill=Y)
        self.info_view = self.Info(self.n_info)
        self.info_view.on_edit(self.edit_entry)
        self.info_view.on_delete(self.remove_entry)

        self.notebook.add(self.n_add, text='Přidat')
        self.notebook.add(self.n_info, text='Zobrazit')

        # Tree
        self.tree_frame = Frame()
        self.tree = self.Tree(self.tree_frame)
        self.tree.fill(self.data)
        self.tree.on_click(self.show_info)

        # Menu
        self.menulist = Menu(root)
        self.menulist.add_command(label='Nastavení', command=self.open_settings)
        root.config(menu=self.menulist)

        # Pack
        self.tree_frame.pack(side='left', fill=BOTH, expand=True)
        self.notebook.pack(side='right', fill=Y)

    def show_info(self, id: str):
        item = self.__find_by_id(id)
        self.info_view.set(item)
        self.notebook.select(self.n_info)

    def add_entry(self, data: Data):
        existing = self.__find_by_id(data['id'])
        if existing:
            existing.update(data)
            self.tree.insert(existing)
        else:
            self.data.append(data)
            self.tree.insert(data)
        self.add_view.clear()

    def edit_entry(self, id: str):
        item = self.__find_by_id(id)
        self.add_view.set(item)
        self.notebook.select(self.n_add)

    def remove_entry(self, id: str):
        item = self.__find_by_id(id)
        self.data.remove(item)
        self.tree.remove(id)
        self.info_view.clear()

    def open_settings(self):
        settings = self.Settings(self.n_add)
        settings.on_load(self.load_data)
        settings.on_save(self.save_data)
        

    def load_data(self):
        try:
            with open(self.path, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print('Cannot load data, file not found!')
            self.data = DataList([Data(id='i1', name='aaa', price=10, info='bbb'), Data(id='i2', name='ccc', price=20, info='ddd')])

    def save_data(self):
        with open(self.path, 'w') as file:
            json.dump(self.data, file)

    def __find_by_id(self, id: str) -> Data | None:
        for item in self.data:
            if item['id'] == id:
                return item
        return None

    class Settings:
        load_cb: Optional[Callable[[], None]] = None
        save_cb: Optional[Callable[[], None]] = None

        def __init__(self, root):
            self.top = Toplevel(root, takefocus=True)
            self.top.title('Nastavení')
            self.top.geometry('230x100')
            self.top.resizable(False, False)

            self.load_btn = Button(self.top, text='Importovat', command=self.__on_load)
            self.save_btn = Button(self.top, text='Exportovat', command=self.__on_save)

            self.load_btn.pack(expand=True)
            self.save_btn.pack(expand=True)

        def on_load(self, callback: Callable[[], None]):
            self.load_cb = callback

        def on_save(self, callback: Callable[[], None]):
            self.save_cb = callback

        def __on_load(self):
            if self.load_cb is not None:
                self.load_cb()

        def __on_save(self):
            if self.save_cb is not None:
                self.save_cb()


    class Tree:
        click_cb: Optional[Callable[[str], None]] = None

        def __init__(self, root: Frame):
            self.tree = ttk.Treeview(root, columns=('id', 'name'), show='headings')
            self.tree.heading('id', text='ID')
            self.tree.heading('name', text='Název')
            self.tree.column('id', width=100, stretch=NO)
            self.tree.column('name', width=250, minwidth=250)

            self.tree.bind('<<TreeviewSelect>>', self.__clicked)

            self.tree.pack(fill=BOTH, expand=True)

        def fill(self, data: DataList):
            for item in data:
                self.insert(item)

        def insert(self, data: Data):
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[0] == data['id']:
                    self.tree.item(item, values=[data['id'], data['name']])
                    return

            self.tree.insert('', 'end', values=[data['id'], data['name']])

        def remove(self, id: str):
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[0] == id:
                    self.tree.delete(item)
                    return

        def on_click(self, fn: Callable[[str], None]):
            self.click_cb = fn

        def __clicked(self, event):
            if self.click_cb is not None:
                try:
                    val = str(self.tree.item(self.tree.selection()[0])['values'][0])
                    self.click_cb(val)
                except IndexError:
                    pass


    class Add:
        add_cb: Optional[Callable[[Data], None]] = None

        def __init__(self, root: Frame):
            name_label = Label(root, text='Název')
            self.name_input = Entry(root)

            id_label = Label(root, text='ID')
            self.id_input = Entry(root)

            price_label = Label(root, text='Cena')
            self.price_input = Entry(root)

            info_label = Label(root, text='Info')
            self.info_input = Text(root)

            self.add_btn = Button(root, text='Přidat', command=self.__on_add)

            name_label.grid(column=0, row=0, sticky='e')
            self.name_input.grid(column=1, row=0, sticky='ew')
            id_label.grid(column=0, row=1, sticky='e')
            self.id_input.grid(column=1, row=1, sticky='ew')
            price_label.grid(column=0, row=2, sticky='e')
            self.price_input.grid(column=1, row=2, sticky='ew')
            info_label.grid(column=0, row=3, sticky='w')
            self.info_input.grid(column=0, row=4, columnspan=2, sticky='nsew')
            self.add_btn.grid(column=0, row=5, columnspan=2)

            root.grid_rowconfigure(4, weight=1)
            root.grid_columnconfigure(1, weight=1)

        def on_add(self, fallback: Callable[[Data], None]):
            self.add_cb = fallback

        def set(self, data: Data):
            self.clear()

            self.name_input.insert(0, data['name'])
            self.id_input.insert(0, data['id'])
            self.price_input.insert(0, str(data['price']))
            self.info_input.insert('end', data['info'])

        def get(self) -> Data:
            name = self.name_input.get()
            id = self.id_input.get()
            price = self.price_input.get()
            info = self.info_input.get(0.0, 'end')
            return Data(
                name = name if name != '' else None,
                id = id if id != '' else None,
                price = int(price) if price != '' else None,
                info = info if info.strip(' \n\r\t') != '' else None)

        def clear(self):
            self.name_input.delete(0, 'end')
            self.id_input.delete(0, 'end')
            self.price_input.delete(0, 'end')
            self.info_input.delete(0.0, 'end')

        def __on_add(self):
            if self.add_cb is None: return
            data = self.get()

            if data['name'] is None:
                messagebox.showerror(message='Zadejte název produktu')
                return
            if data['id'] is None:
                messagebox.showerror(message='Zadejte ID produktu')
                return
            if data['price'] is None:
                messagebox.showerror(message='Zadejte cenu produktu')
                return

            self.add_cb(self.get())


    class Info:
        delete_cb: Optional[Callable[[str], None]] = None
        edit_cb: Optional[Callable[[str], None]] = None

        def __init__(self, root: Frame):
            self.name = Label(root, text='_')
            self.name.config(font=('Helvetica', 16, 'bold'))
            self.id = Label(root, text='_')
            self.id.config(font=('Helvetica', 12), foreground='grey')
            self.price = Label(root, text='_')
            self.price.config(font=('Helvetica', 14, 'italic'))
            info_label = Label(root, text='Dodatečné informace')
            self.info = Text(root, state=DISABLED)
            buttons_wrapper = Frame(root)
            self.delete_btn = Button(buttons_wrapper, text='Odstranit', command=self.__on_delete)
            self.edit_btn = Button(buttons_wrapper, text='Upravit', command=self.__on_edit)

            self.name.pack()
            self.id.pack()
            self.price.pack()
            info_label.pack()
            self.info.pack()
            self.delete_btn.pack(side='left')
            self.edit_btn.pack(side='right')
            buttons_wrapper.pack(fill=X)

        def set(self, data: Data):
            self.name.config(text=data['name'])
            self.id.config(text=data['id'])
            self.price.config(text=str(data['price']))
            self.info.config(state=NORMAL)
            self.info.delete(0.0, 'end')
            if data['info'] is not None:
                self.info.insert('end', data['info'])
            self.info.config(state=DISABLED)

        def clear(self):
            self.name.config(text='_')
            self.id.config(text='_')
            self.price.config(text='_')
            self.info.config(state=NORMAL)
            self.info.delete(0.0, 'end')
            self.info.config(state=DISABLED)

        def on_delete(self, callback: Callable[[str], None]):
            self.delete_cb = callback

        def on_edit(self, callback: Callable[[str], None]):
            self.edit_cb = callback

        def __on_delete(self):
            if self.delete_cb is None: return

            id: str = self.id.cget('text')
            if id == '_':
                messagebox.showerror(message='Není vybrán žádný produkt!')
                return

            self.delete_cb(id)

        def __on_edit(self):
            if self.edit_cb is None: return

            id: str = self.id.cget('text')
            if id == '_':
                messagebox.showerror(message='Není vybrán žádný produkt!')
                return

            self.edit_cb(id)

root = Tk()
app = App(root)
root.mainloop()
