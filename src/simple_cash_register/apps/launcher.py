import tkinter as tk
from simple_cash_register.apps.editor import main as editor_main
from simple_cash_register.apps.history import main as history_main
from simple_cash_register.apps.register import main as pos_main
from simple_cash_register.apps.option import option as option_main

class launcher:
    def __init__(self, ROOT):
        self.root = ROOT
        self.pos_button = tk.Button(self.root, text="POSレジ", command=self.pos)
        self.editor_button = tk.Button(self.root, text="商品・ジャンル編集", command=self.editor)
        self.history_button = tk.Button(self.root, text="取引履歴", command=self.history)
        self.option_button = tk.Button(self.root, text="そのほか設定", command=self.option)
        self.pos_button.pack()
        self.editor_button.pack()
        self.history_button.pack()
        self.option_button.pack()
        self.root.mainloop()
    def all_forget(self):
        self.pos_button.forget()
        self.editor_button.forget()
        self.history_button.forget()
        self.option_button.forget()
    def pos(self):
        self.all_forget()
        pos_main(self.root)
    def editor(self):
        self.all_forget()
        editor_main(self.root)
    def history(self):
        self.all_forget()
        history_main(self.root)
    def option(self):
        self.all_forget()
        option_main(self.root)
def main(ROOT):
    LAUNCHER = launcher(ROOT)