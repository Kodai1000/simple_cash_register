import tkinter as tk
from simple_cash_register.core.register.products import product_data_base as ProductDataBase
from simple_cash_register.core.register.tables import table as Table
from simple_cash_register.core.register.tables import table_list as TableList
from simple_cash_register.ui.product_list import product_list_gui as ProductListGui
from simple_cash_register.ui.receipt import receipt_gui as ReceiptGui
from simple_cash_register.ui.table_list import table_list_gui as TableListGui

class simple_pos_app:
    def __init__(self, root, the_number_of_tables):
        self.product_data_base = ProductDataBase()
        self.product_data_base = ProductDataBase()
        self.product_list, self.genre_names = self.product_data_base.load()
        #self.root = tk.Tk()
        self.root = root
        self.root.title("Simple Cash Register")
        self.root.geometry("1280x720")
        self.the_number_of_tables = the_number_of_tables
        self.layout()
        self.prepare_data()
        self.prepare_gui_classes()
        
    def layout(self):
        self.main = tk.Frame(self.root)
        self.main.pack(fill="both", expand=True, padx=8, pady=8)
        self.top_col = tk.Frame(self.main, width=1280)
        self.top_col.pack()
        self.left_col = tk.Frame(self.main, width=640)
        self.left_col.pack(side="left", fill="both", padx=8, pady=8)
        self.right_col = tk.Frame(self.main, width=640)
        self.right_col.pack(side="right", fill="both",expand=True, padx=8, pady=8)
        self.right_col.pack_propagate(0)

        self.product_frame = tk.LabelFrame(self.left_col, text="Product")
        self.product_frame.pack(fill="both", expand=True)
        self.receipt_frame = tk.LabelFrame(self.right_col, text="receipt")
        self.receipt_frame.pack(fill="both", expand=True)
        self.payment_frame = tk.LabelFrame(self.right_col, text="Payment")
        self.payment_frame.pack(fill="x", pady=(8,0))
        self.table_frame = tk.LabelFrame(self.top_col, text="Tables")
        self.table_frame.pack(fill="both", expand=True)
    def prepare_data(self):
        self.table_list = TableList([Table(str(i+1), []) for i in range(self.the_number_of_tables)])
    def prepare_gui_classes(self):
        self.receipt_gui = ReceiptGui(self.receipt_frame, self.payment_frame, self.table_list.tables[0])
        self.table_list_gui = TableListGui(self.table_frame, self.table_list, self.receipt_gui)
        self.table_list_gui.show_buttons()
        self.product_list_gui = ProductListGui(self.product_frame, self.product_list, self.receipt_gui, self.genre_names)
        self.product_list_gui.show_buttons_genre()

def main(root):
    SimplePosApp = simple_pos_app(root, 10)
    SimplePosApp.root.mainloop()