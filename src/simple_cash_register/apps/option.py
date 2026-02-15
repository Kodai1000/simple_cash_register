import tkinter as tk
import tkinter as tk
from simple_cash_register.core.register.option import option as Option

class option:
    def __init__(self, ROOT):
        self.Option = Option()
        self.Option.load()
        self.root = ROOT
        self.shop_name_label = tk.Label(self.root, text="店名")
        self.shop_name_entry = tk.Entry(self.root) 
        self.shop_name_entry.insert(0, self.Option.shop_name)
        self.sync_button = tk.Button(self.root, text="更新", command=self.sync)
        self.shop_name_label.pack(side=tk.LEFT)
        self.shop_name_entry.pack(side=tk.LEFT)
        self.sync_button.pack(side=tk.BOTTOM)
        self.root.mainloop()
    def sync(self):
        self.Option.add_shop_name(self.shop_name_entry.get())
        self.Option.save()