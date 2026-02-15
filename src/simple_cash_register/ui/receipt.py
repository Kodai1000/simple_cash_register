import tkinter as tk
from simple_cash_register.core.register.tables import *
from simple_cash_register.core.register.print import *
class receipt_gui():
    def __init__(self, frame, accounter_frame, table_CLASS: table):
        self.table = table_CLASS
        
        self.canvas = tk.Canvas(frame, borderwidth=0)
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, expand=True, fill="both")

        self.frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0,0), window=self.frame, anchor="nw")

        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.frame.bind("<Configure>", _on_frame_configure)

        def _on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", _on_canvas_configure)

        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.table = table_CLASS
        self.bought_products = []
        self.accounter_frame = accounter_frame
        self.sum_label = tk.Label(self.accounter_frame, text="合計: " + str(self.table.total))
        self.sum_label.pack()
        
        self.ten_keys = ten_key_gui(self)
        self.change_label = tk.Label(self.accounter_frame, text="お釣: " + str(self.ten_keys.figure))
        self.change_label.pack()

        self.ten_keys.show_ten_keys()
        self.initialize_buttons()

        self.print_button = tk.Button(self.frame, text="印刷", command=self.only_print)
        self.print_button.pack(side="top")

       

        #self.ten_key_frame = tk.Frame(self.accounter_frame)

        self.account_button = tk.Button(self.accounter_frame, text="会計", command=self.account)
        self.account_button.pack()

    def add(self, product_CLASS):
        self.table.add(product_CLASS)
        self.sync()
        
    def change_table(self, table_CLASS):
        for bought_product_gui in self.bought_products:
            bought_product_gui.all_forget()
        
        self.table = table_CLASS
        self.ten_keys.change_table()
        self.sync()
        self.renew_change_label()

    def initialize_buttons(self):
        for bought_product in self.bought_products:
            bought_product.all_forget()
        self.bought_products = []
        self.sync()
        """
        for bought_product in self.table.bought_products:
            self.bought_products.append(
                bought_product_gui(
                    self.frame,
                    bought_product,
                    self
                )
            )
        """
    def check_and_delete(self):
        for bought_product in self.bought_products:
            if bought_product.bought_product.quantity < 0:
                pass
        
    def renew_change_label(self):
        change = self.ten_keys.figure - int(self.table.total)
        self.change_label['text'] = "お釣: " + str(change)
    
    def account(self):
        if self.table.account(int(self.ten_keys.figure)):
            for bought_product in self.bought_products:
                bought_product.all_forget()
            self.ten_keys.figure = 0
            self.ten_keys.renew()
            self.check_and_delete()
            self.renew_change_label()
            self.bought_products = []
            self.sync()
        else:
            pass
    def only_print(self):
        print_receipt(self.table, mode="abnormal")
    def sync(self):
        self.sum_label['text'] = "合計: " + str(self.table.total)
        internal_product_length = len(self.table.bought_products)
        gui_product_length = len(self.bought_products)
        self.bought_products = self.bought_products[0:internal_product_length]
        for i, table_product in enumerate(self.table.bought_products):
            if i < gui_product_length:
                if table_product.product.name != self.bought_products[i].bought_product.product.name or table_product.quantity != self.bought_products[i].bought_product.quantity:
                    self.bought_products[i].bought_product = table_product
            else:
                self.bought_products.append(
                    bought_product_gui(
                        self.frame,
                        table_product,
                        self
                    )
                )
                self.bought_products[-1].show()
            self.bought_products[i].renew()
        
class bought_product_gui():
    def __init__(self, frame, bought_product:bought_product, receipt_gui:receipt_gui):
        self.frame = tk.Frame(frame, relief=tk.SUNKEN, bd=5)
        self.frame.pack(side='top', fill='both'),
        self.bought_product = bought_product
        self.receipt_gui = receipt_gui
    def show(self):
        product_font=tk.font.Font(family="MS Gothic", size=20)
        self.name_label = tk.Label(self.frame, text=self.bought_product.product.name, font=product_font)
        self.unit_price_label = tk.Label(self.frame, text=self.bought_product.product.price, font=product_font)
        self.quantity_label = tk.Label(self.frame, font=product_font)
        self.remove_button = tk.Button(self.frame, text="←", command=self.remove, font=product_font, bg="lightblue")
        self.add_button = tk.Button(self.frame, text="→", command=self.add, font=product_font, bg="lightblue")
        self.sum_price_label = tk.Button(self.frame, font=product_font)
        self.renew()

        self.name_label.pack(side="left")
        self.unit_price_label.pack(side="left")

        self.sum_price_label.pack(side="right")
        self.add_button.pack(side="right")
        self.quantity_label.pack(side="right")
        self.remove_button.pack(side="right")
        
    def all_forget(self):
        self.frame.forget()
    def add(self):
        self.bought_product.add()
        self.renew()
        self.receipt_gui.sync()
    def remove(self):
        self.bought_product.remove()
        self.renew()
        self.receipt_gui.sync()
    def renew(self):
        if self.bought_product.quantity > 0:
            self.quantity_label['text'] = str(self.bought_product.quantity).zfill(2)
            self.sum_price_label['text'] = str(self.bought_product.sum()).zfill(5)
        else:
            self.all_forget()
        self.receipt_gui.check_and_delete()

class ten_key_gui():
    def __init__(self, receipt_gui:receipt_gui):
        self.receipt_gui = receipt_gui
        self.frame = self.receipt_gui.accounter_frame
        self.figure = self.receipt_gui.table.pay
        self.label = tk.Label(self.frame, text="支払: " + str(self.figure))
        self.label.pack()
    def show_ten_keys(self):
        buttons = []
        key_font=tk.font.Font(family="MS Gothic", size=15)
        for i in range(10):
            buttons.append(
                tk.Button(self.frame, text=str(i),command=lambda i=i: self.add_figure(i), width=6, height=2, bg="lightblue", font=key_font)
            )
            buttons[-1].pack(side='left')
        self.deleted_button = tk.Button(self.frame, text="◁", command=self.deleted_button, width=4, height=2, bg="lightblue", font=key_font)
        self.deleted_button.pack(side='left')
    def add_figure(self, added_figure):
        strized = str(self.figure)
        added_strized_figure = strized + str(added_figure)
        self.figure = int(added_strized_figure)
        self.renew()
        self.receipt_gui.renew_change_label()
    def deleted_button(self):
        strized = str(self.figure)
        strized = strized[0:-1]
        if strized == "":
            self.figure = 0
        else:
            self.figure = int(strized)
        self.renew()
        self.receipt_gui.renew_change_label()
    def change_table(self):
        self.figure = self.receipt_gui.table.pay
        self.renew()
    def renew(self):
        self.label['text'] = "支払: " + str(self.figure)
        self.receipt_gui.table.pay = self.figure