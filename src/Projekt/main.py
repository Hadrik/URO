import shutil
from tkinter import *
from tkinter import ttk, messagebox, filedialog, colorchooser
from tkinter.font import Font
from PIL import ImageTk, Image
from typing import TypedDict, Callable, Optional
from typing import NewType
import json

class Data(TypedDict):
    id: str
    name: str
    price: int
    info: str
    img_path: str

DataList = NewType('DataList', list[Data])

class App:
    data: DataList
    default_path = './data.json'

    def __init__(self, root: Tk):
        root.option_add('*Font', Font(family='Helvetica', size=14))

        self.load_data(self.default_path)

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

        self.left_panel = Frame(root)

        # Filter
        filter_container = Frame(self.left_panel)
        label = Label(filter_container, text='Filtr')
        self.sv = StringVar()
        self.sv.trace_add("write", self.filter)
        self.filter_box = Entry(filter_container, textvariable=self.sv)
        label.pack(side='left')
        self.filter_box.pack(side='right', padx=18, expand=True, fill=X)
        filter_container.pack(side='top', fill=X)

        # Tree
        self.tree_frame = Frame(self.left_panel)
        self.tree = self.Tree(self.tree_frame)
        self.tree.fill(self.data)
        self.tree.on_click(self.show_info)
        self.tree_frame.pack(fill=BOTH, expand=True)

        # Menu
        self.menulist = Menu(root)
        self.menulist.add_command(label='Nastavení', command=self.open_settings)
        root.config(menu=self.menulist)

        # Pack
        self.left_panel.pack(side='left', fill=BOTH, expand=True)
        self.notebook.pack(side='right', fill=Y)

    def show_info(self, id: str):
        item = self.__find_by_id(id)
        self.info_view.set(item)
        self.notebook.select(self.n_info)

    def add_entry(self, data: Data):
        existing = self.__find_by_id(data['id'])
        if existing:
            if 'img_path' in data and existing.get('img_path') != data['img_path']:
                data['img_path'] = self.__copy_image(data['img_path'])
            existing.update(data)
            self.tree.insert(existing)
        else:
            if 'img_path' in data:
                data['img_path'] = self.__copy_image(data['img_path'])
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
        settings.on_color_change(self.change_color)

    def filter(self, n: str, i: str, m: str):
        value = self.filter_box.get()
        filtered_data = DataList([item for item in self.data if value in item['name'].lower()])
        self.tree.refresh(filtered_data)

    def load_data(self, path: str | None = None):
        if path is None:
            path = filedialog.askopenfilename(
                title="Vyberte soubor",
                filetypes=[('JSON files', '*.json')],
                defaultextension='*.json',
                initialdir='.')
        try:
            with open(path, 'r') as file:
                self.data = json.load(file)
                try:
                    self.tree.refresh(self.data)
                except AttributeError:
                    pass
        except FileNotFoundError:
            print('Cannot load data, file not found!')

    def save_data(self, path: str | None = None):
        if path is None:
            path = filedialog.asksaveasfilename(
                title="Uložte soubor",
                filetypes=[('JSON files', '*.json')],
                defaultextension='*.json',
                initialdir='.')
        with open(path, 'w') as file:
            json.dump(self.data, file)

    def change_color(self, color: str):
        self.left_panel.config(bg=color)
        self.n_add.config(bg=color)
        self.n_info.config(bg=color)
        self.tree_frame.config(bg=color)
        self.add_view.set_bg(color)
        self.info_view.set_bg(color)

    def __find_by_id(self, id: str) -> Data | None:
        for item in self.data:
            if item['id'] == id:
                return item
        return None

    @staticmethod
    def __copy_image(path: str) -> str | None:
        try:
            return shutil.copy2(path, './images')
        except Exception:
            return None

    class Settings:
        load_cb: Optional[Callable[[], None]] = None
        save_cb: Optional[Callable[[], None]] = None
        color_cb: Optional[Callable[[str], None]] = None

        def __init__(self, root):
            self.top = Toplevel(root, takefocus=True)
            self.top.title('Nastavení')
            self.top.geometry('230x150')
            self.top.resizable(False, False)

            self.load_btn = Button(self.top, text='Importovat', command=self.__on_load)
            self.save_btn = Button(self.top, text='Exportovat', command=self.__on_save)
            self.color_btn = Button(self.top, text='Změnit barvu', command=self.__on_color_change)

            self.load_btn.pack(expand=True)
            self.save_btn.pack(expand=True)
            self.color_btn.pack(expand=True)

        def on_load(self, callback: Callable[[], None]):
            self.load_cb = callback

        def on_save(self, callback: Callable[[], None]):
            self.save_cb = callback

        def on_color_change(self, callback: Callable[[str], None]):
            self.color_cb = callback

        def __on_load(self):
            if self.load_cb is not None:
                self.load_cb()

        def __on_save(self):
            if self.save_cb is not None:
                self.save_cb()

        def __on_color_change(self):
            color: tuple[tuple[int, int, int], str] = colorchooser.askcolor()
            if self.color_cb is not None and color[1] is not None:
                self.color_cb(color[1])


    class Tree:
        click_cb: Optional[Callable[[str], None]] = None

        def __init__(self, root: Frame):
            self.container = Frame(root)

            self.tree = ttk.Treeview(self.container, columns=('id', 'name'), show='headings')
            self.tree.heading('id', text='ID')
            self.tree.heading('name', text='Název')
            self.tree.column('id', width=30, stretch=NO)
            self.tree.column('name', width=250, minwidth=250)

            self.tree.bind('<<TreeviewSelect>>', self.__clicked)

            self.scrollbar = ttk.Scrollbar(self.container, orient='vertical', command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.scrollbar.set)
            self.scrollbar.grid(row=0, column=1, sticky='ns')
            self.tree.grid(row=0, column=0, sticky='nsew')
            self.container.grid_rowconfigure(0, weight=1)
            self.container.grid_columnconfigure(0, weight=1)
            self.container.pack(fill=BOTH, expand=True)

        def fill(self, data: DataList):
            for item in data:
                self.insert(item)

        def clear(self):
            self.tree.delete(*self.tree.get_children())

        def refresh(self, data: DataList):
            self.clear()
            self.fill(data)

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
            self.name_label = Label(root, text='Název')
            self.name_input = Entry(root)

            self.id_label = Label(root, text='ID')
            self.id_input = Entry(root)

            self.price_label = Label(root, text='Cena')
            self.price_input = Entry(root)

            self.image_wrapper = Frame(root)
            self.image_select = Button(self.image_wrapper, text='Vyberte obrázek', command=self.__open_image_picker)
            self.image_name = Label(self.image_wrapper, text='Obrázek nevybrán')
            self.image_select.pack(side='left')
            self.image_name.pack(side='left')

            self.info_label = Label(root, text='Info')
            self.info_input = Text(root)

            self.add_btn = Button(root, text='Přidat', command=self.__on_add)

            self.name_label.grid(column=0, row=0, sticky='e')
            self.name_input.grid(column=1, row=0, sticky='ew')
            self.id_label.grid(column=0, row=1, sticky='e')
            self.id_input.grid(column=1, row=1, sticky='ew')
            self.price_label.grid(column=0, row=2, sticky='e')
            self.price_input.grid(column=1, row=2, sticky='ew')
            self.image_wrapper.grid(columnspan=2, column=0, row=3, sticky='ew')
            self.info_label.grid(column=0, row=4, sticky='w')
            self.info_input.grid(column=0, row=5, columnspan=2, sticky='nsew')
            self.add_btn.grid(column=0, row=6, columnspan=2)

            root.grid_rowconfigure(5, weight=1)
            root.grid_columnconfigure(1, weight=1)

        def on_add(self, callback: Callable[[Data], None]):
            self.add_cb = callback

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
            img = self.image_name.cget('text')
            return Data(
                name = name if name != '' else None,
                id = id if id != '' else None,
                price = int(price) if price != '' else None,
                info = info if info.strip(' \n\r\t') != '' else None,
                img_path = img if img != '' else None
            )

        def clear(self):
            self.name_input.delete(0, 'end')
            self.id_input.delete(0, 'end')
            self.price_input.delete(0, 'end')
            self.info_input.delete(0.0, 'end')

        def set_bg(self, color: str):
            self.name_label.config(bg=color)
            self.name_input.config(bg=color)
            self.id_label.config(bg=color)
            self.id_input.config(bg=color)
            self.price_label.config(bg=color)
            self.price_input.config(bg=color)
            self.info_label.config(bg=color)
            self.info_input.config(bg=color)
            self.image_wrapper.config(bg=color)
            self.image_select.config(bg=color)
            self.image_name.config(bg=color)
            self.add_btn.config(bg=color)

        def __open_image_picker(self):
            file = filedialog.askopenfilename(
                title='Vyberte obrázek',
                filetypes=[('JPG files', '*.JPG'), ('PNG files', '*.PNG')]
            )
            self.image_name.config(text=file)

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
            self.info_label = Label(root, text='Dodatečné informace')
            self.info = Text(root, state=DISABLED)
            self.none_image = ImageTk.PhotoImage(Image.open('Image-not-found.png'))
            self.image = self.none_image
            self.image_panel = Label(root, image=self.none_image)
            self.buttons_wrapper = Frame(root)
            self.delete_btn = Button(self.buttons_wrapper, text='Odstranit', command=self.__on_delete)
            self.edit_btn = Button(self.buttons_wrapper, text='Upravit', command=self.__on_edit)

            self.name.grid(row=0)
            self.id.grid(row=1)
            self.price.grid(row=2)
            self.info_label.grid(row=3)
            self.info.grid(row=4)
            self.image_panel.grid(row=5)
            self.delete_btn.pack(side='left')
            self.edit_btn.pack(side='right')
            self.buttons_wrapper.grid(row=6, sticky='ew')

            root.grid_rowconfigure(4, weight=1)
            root.columnconfigure(0, weight=1)

        def set(self, data: Data):
            self.name.config(text=data['name'])
            self.id.config(text=f"ID: {data['id']}")
            self.price.config(text=f"{str(data['price'])} Kč")
            self.info.config(state=NORMAL)
            self.info.delete(0.0, 'end')
            if data['info'] is not None:
                self.info.insert('end', data['info'])
            self.info.config(state=DISABLED)

            try:
                path = data['img_path']
                image = Image.open(path)
                self.image = ImageTk.PhotoImage(image)
                self.image_panel.config(image=self.image)
                return
            except FileNotFoundError as e:
                print(f"Error loading image '{e.filename}'")
            except KeyError:
                print('Item does not have image path')
            self.image_panel.config(image=self.none_image)

        def clear(self):
            self.name.config(text='_')
            self.id.config(text='_')
            self.price.config(text='_')
            self.info.config(state=NORMAL)
            self.info.delete(0.0, 'end')
            self.info.config(state=DISABLED)
            self.image_panel.config(image=self.none_image)

        def set_bg(self, color: str):
            self.name.config(bg=color)
            self.id.config(bg=color)
            self.price.config(bg=color)
            self.info_label.config(bg=color)
            self.info.config(bg=color)
            self.image_panel.config(bg=color)
            self.buttons_wrapper.config(bg=color)
            self.delete_btn.config(bg=color)
            self.edit_btn.config(bg=color)

        def on_delete(self, callback: Callable[[str], None]):
            self.delete_cb = callback

        def on_edit(self, callback: Callable[[str], None]):
            self.edit_cb = callback

        def __on_delete(self):
            if self.delete_cb is None: return

            id: str = self.id.cget('text')
            id = id.lstrip('ID: ')
            if id == '_':
                messagebox.showerror(message='Není vybrán žádný produkt!')
                return

            self.delete_cb(id)

        def __on_edit(self):
            if self.edit_cb is None: return

            id: str = self.id.cget('text')
            id = id.lstrip('ID: ')
            if id == '_':
                messagebox.showerror(message='Není vybrán žádný produkt!')
                return

            self.edit_cb(id)


root = Tk()
app = App(root)
root.mainloop()
