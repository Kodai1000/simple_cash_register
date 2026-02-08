from simple_cash_register.core.register.product_and_genre_manager import product_and_genre_manager as ProductAndGenreManager
import tkinter as tk
import tkinter.ttk as ttk

class product_edit_gui:
    def __init__(self, frame, product_and_genre_manager: ProductAndGenreManager):
        self.parent_frame = frame
        self.canvas = tk.Canvas(self.parent_frame)
        self.frame = tk.Frame(self.canvas)
        self.entry_frame = tk.Frame(self.frame)
        self.entry_frame.pack(side=tk.BOTTOM)
        self.products_container = tk.Frame(self.frame)
        self.products_container.pack(fill="x", anchor="n")
        self.canvas.pack()
        self.frame.pack()
        self.manager = product_and_genre_manager
        self._genre_map = {}  # "id: name" -> id

    def refresh_genres(self):
        genres = self.manager.get_all_genres()
        self._genre_map = {f"{g[0]}: {g[1]}": g[0] for g in genres}
        if hasattr(self, "genre_combobox"):
            self.genre_combobox['values'] = list(self._genre_map.keys())

    def show_products(self):
        products = self.manager.get_all_products()
        self.refresh_genres()
        for w in self.products_container.winfo_children():
            w.destroy()
        for i, product in enumerate(products):
            product_frame = tk.Frame(self.products_container, relief=tk.SUNKEN, bd=2)
            id_label = tk.Label(product_frame, text=str(product[0]))
            name_label = tk.Label(product_frame, text=str(product[1]))
            price_label = tk.Label(product_frame, text=str(product[2]).zfill(5))
            genre_label = tk.Label(product_frame, text=str(product[3]).zfill(5))
            edit_button = tk.Button(product_frame, text="編集", command=lambda i=i: self.insert_into_edit_entries(i))
            del_button = tk.Button(product_frame, text="削除", command=lambda id=product[0]: self.delete_product(id))
            product_frame.pack(fill="x")
            id_label.pack(side=tk.LEFT, padx=4, pady=4)
            name_label.pack(side=tk.LEFT, padx=4, pady=4)
            del_button.pack(side=tk.RIGHT)
            edit_button.pack(side=tk.RIGHT)
            price_label.pack(side=tk.RIGHT, padx=4, pady=4)
            genre_label.pack(side=tk.RIGHT, padx=4, pady=4)

    def insert_into_edit_entries(self, i):
        products = self.manager.get_all_products()
        product = products[i]
        if not hasattr(self, "id_entry"):
            self.show_edit_entries_and_buttons()
        try:
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            self.price_entry.delete(0, tk.END)
            # combobox clear handled below
        except:
            pass
        self.id_entry.insert(0, product[0])
        self.name_entry.insert(0, product[1])
        self.price_entry.insert(0, product[2])
        # set combobox selection to matching "id: name"
        self.refresh_genres()
        if product[3] is None:
            self.genre_combobox.set('')
        else:
            # build mapping id -> "id: name"
            id_to_key = {v:k for k,v in self._genre_map.items()}
            key = id_to_key.get(product[3], '')
            self.genre_combobox.set(key)

    def delete_product(self, deleted_id):
        self.manager.delete_product(deleted_id)
        self.show_products()

    def show_combobox(self):
        self.combobox = ttk.Combobox(self.frame, values=["編集","追加"])
        self.combobox.bind("<<ComboboxSelected>>", lambda e: self.change_mode())
        self.combobox.pack()

    def change_mode(self, event=None):
        gotten_mode = self.combobox.get()
        self.entries_and_button_forget()
        if gotten_mode == "編集":
            self.show_edit_entries_and_buttons()
        elif gotten_mode == "追加":
            self.show_add_entries()

    def show_edit_entries_and_buttons(self):
        self.id_col_label = tk.Label(self.entry_frame, text="ID")
        self.id_entry = ttk.Entry(self.entry_frame)
        self.name_col_label = tk.Label(self.entry_frame, text="名前")
        self.name_entry = ttk.Entry(self.entry_frame)
        self.price_col_label = tk.Label(self.entry_frame, text="値段")
        self.price_entry = ttk.Entry(self.entry_frame)
        self.genre_col_label = tk.Label(self.entry_frame, text="ジャンル")
        # genre combobox instead of entry
        self.refresh_genres()
        self.genre_combobox = ttk.Combobox(self.entry_frame, values=list(self._genre_map.keys()))
        self.deciding_button = tk.Button(self.entry_frame, text="決定", command=self.decide_edit)
        self.id_col_label.pack(side=tk.LEFT)
        self.id_entry.pack(side=tk.LEFT)
        self.name_col_label.pack(side=tk.LEFT)
        self.name_entry.pack(side=tk.LEFT)
        self.price_col_label.pack(side=tk.LEFT)
        self.price_entry.pack(side=tk.LEFT)
        self.genre_col_label.pack(side=tk.LEFT)
        self.genre_combobox.pack(side=tk.LEFT)
        self.deciding_button.pack()

    def decide_edit(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        price = self.price_entry.get()
        genre_sel = self.genre_combobox.get()
        genre_id = self._genre_map.get(genre_sel, "")
        self.manager.change_product(id, name, price, genre_id)
        self.show_products()

    def show_add_entries(self):
        self.name_col_label = tk.Label(self.entry_frame, text="名前")
        self.name_entry = ttk.Entry(self.entry_frame)
        self.price_col_label = tk.Label(self.entry_frame, text="値段")
        self.price_entry = ttk.Entry(self.entry_frame)
        self.genre_col_label = tk.Label(self.entry_frame, text="ジャンル")
        self.refresh_genres()
        self.genre_combobox = ttk.Combobox(self.entry_frame, values=list(self._genre_map.keys()))
        self.deciding_button = tk.Button(self.entry_frame, text="決定", command=self.decide_add)
        self.name_col_label.pack(side=tk.LEFT)
        self.name_entry.pack(side=tk.LEFT)
        self.price_col_label.pack(side=tk.LEFT)
        self.price_entry.pack(side=tk.LEFT)
        self.genre_col_label.pack(side=tk.LEFT)
        self.genre_combobox.pack(side=tk.LEFT)
        self.deciding_button.pack()

    def decide_add(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        genre_sel = self.genre_combobox.get()
        genre_id = self._genre_map.get(genre_sel, "")
        self.manager.add_product(name, price, genre_id)
        self.show_products()

    def entries_and_button_forget(self):
        try:
            self.id_col_label.pack_forget()
            self.id_entry.pack_forget()
        except:
            pass
        try:
            self.name_col_label.pack_forget()
            self.name_entry.pack_forget()
            self.price_col_label.pack_forget()
            self.price_entry.pack_forget()
            self.genre_col_label.pack_forget()
            # prefer pack_forget for combobox if present
            try:
                self.genre_combobox.pack_forget()
            except:
                try:
                    self.genre_entry.pack_forget()
                except:
                    pass
            self.deciding_button.pack_forget()
        except:
            pass

class genre_edit_gui:
    def __init__(self, frame, product_and_genre_manager: ProductAndGenreManager, on_genre_change=None):
        self.parent_frame = frame
        self.canvas = tk.Canvas(self.parent_frame)
        self.frame = tk.Frame(self.canvas)
        self.entry_frame = tk.Frame(self.frame)
        self.entry_frame.pack(side=tk.BOTTOM)
        self.genres_container = tk.Frame(self.frame)
        self.genres_container.pack(fill="x", anchor="n")
        self.canvas.pack()
        self.frame.pack()
        self.manager = product_and_genre_manager
        self._genre_map = {}  # "id: name" -> id
        self.on_genre_change = on_genre_change

    def show_genres(self):
        genres = self.manager.get_all_genres()
        for w in self.genres_container.winfo_children():
            w.destroy()
        for i, genre in enumerate(genres):
            genre_frame = tk.Frame(self.genres_container, relief=tk.SUNKEN, bd=2)
            id_label = tk.Label(genre_frame, text=str(genre[0]))
            name_label = tk.Label(genre_frame, text=str(genre[1]))
            edit_button = tk.Button(genre_frame, text="編集", command=lambda i=i: self.insert_into_edit_entries(i))
            del_button = tk.Button(genre_frame, text="削除", command=lambda id=genre[0]: self.delete_genre(id))
            genre_frame.pack(fill="x")
            id_label.pack(side=tk.LEFT, padx=4, pady=4)
            name_label.pack(side=tk.LEFT, padx=4, pady=4)
            del_button.pack(side=tk.RIGHT)
            edit_button.pack(side=tk.RIGHT)

    def insert_into_edit_entries(self, i):
        genres = self.manager.get_all_genres()
        genre = genres[i]
        if not hasattr(self, "id_entry"):
            self.show_edit_entries_and_buttons()
        try:
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
        except:
            pass
        self.id_entry.insert(0, genre[0])
        self.name_entry.insert(0, genre[1])

    def delete_genre(self, deleted_id):
        self.manager.delete_genre(deleted_id)
        self.show_genres()
        if self.on_genre_change:
            self.on_genre_change()

    def show_edit_entries_and_buttons(self):
        self.id_col_label = tk.Label(self.entry_frame, text="ID")
        self.id_entry = ttk.Entry(self.entry_frame)
        self.name_col_label = tk.Label(self.entry_frame, text="名前")
        self.name_entry = ttk.Entry(self.entry_frame)
        self.deciding_button = tk.Button(self.entry_frame, text="決定", command=self.decide_edit)
        self.id_col_label.pack(side=tk.LEFT)
        self.id_entry.pack(side=tk.LEFT)
        self.name_col_label.pack(side=tk.LEFT)
        self.name_entry.pack(side=tk.LEFT)
        self.deciding_button.pack(side=tk.LEFT)

    def decide_edit(self):
        id = self.id_entry.get()
        name = self.name_entry.get()
        self.manager.change_genre(id, name)
        self.show_genres()
        if self.on_genre_change:
            self.on_genre_change()

    def show_combobox(self):
        self.combobox = ttk.Combobox(self.frame, values=["編集","追加"])
        self.combobox.bind("<<ComboboxSelected>>", lambda e: self.change_mode())
        self.combobox.pack()

    def change_mode(self, event=None):
        gotten_mode = self.combobox.get()
        self.entries_and_button_forget()
        if gotten_mode == "編集":
            self.show_edit_entries_and_buttons()
        elif gotten_mode == "追加":
            self.show_add_entries()

    def show_add_entries(self):
        self.name_col_label = tk.Label(self.entry_frame, text="名前")
        self.name_entry = ttk.Entry(self.entry_frame)
        self.deciding_button = tk.Button(self.entry_frame, text="決定", command=self.decide_add)
        self.name_col_label.pack(side=tk.LEFT)
        self.name_entry.pack(side=tk.LEFT)
        self.deciding_button.pack(side=tk.LEFT)

    def decide_add(self):
        name = self.name_entry.get()
        self.manager.add_genre(name)
        self.show_genres()
        if self.on_genre_change:
            self.on_genre_change()

    def entries_and_button_forget(self):
        try:
            self.id_col_label.pack_forget()
            self.id_entry.pack_forget()
        except:
            pass
        try:
            self.name_col_label.pack_forget()
            self.name_entry.pack_forget()
            self.deciding_button.pack_forget()
        except:
            pass

def main(ROOT):
    root = ROOT
    root.geometry("1280x720")

    manager = ProductAndGenreManager()

    notebook = ttk.Notebook(root)
    product_tab_frame = tk.Frame(notebook)
    genre_tab_frame = tk.Frame(notebook)

    product_editor = product_edit_gui(product_tab_frame, manager)
    product_editor.show_products()
    product_editor.show_combobox()
    product_editor.show_edit_entries_and_buttons()

    genre_editor = genre_edit_gui(genre_tab_frame, manager, on_genre_change=product_editor.refresh_genres)
    genre_editor.show_genres()
    genre_editor.show_combobox()
    genre_editor.show_edit_entries_and_buttons()

    notebook.add(product_tab_frame, text="Products")
    notebook.add(genre_tab_frame, text="Genres")
    notebook.pack(fill="both", expand=True)

    root.mainloop()