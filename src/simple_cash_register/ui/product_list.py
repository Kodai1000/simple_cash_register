import tkinter as tk
from simple_cash_register.core.register.products import *
from simple_cash_register.ui.receipt import *
class product_list_gui:
    def __init__(self, frame, product_list_CLASS, receipt_gui_CLASS, genres):
        # Canvas/Scrollbar を外側の frame に配置、内部フレームは canvas.create_window に渡す（pack しない）
        self.canvas = tk.Canvas(frame, borderwidth=0)
        self.scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        # 内部コンテンツ用フレーム（ここでは pack/grid しない）
        self.frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        # 内部フレームサイズに応じて scrollregion を更新
        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.frame.bind("<Configure>", _on_frame_configure)

        # canvas の幅に合わせて内部 window の幅を調整（横スクロールを防ぐ）
        def _on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", _on_canvas_configure)

        # マウスホイール（マウスが canvas 上にある時だけバインド）
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        def _bind_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        def _unbind_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
        self.canvas.bind("<Enter>", _bind_mousewheel)
        self.canvas.bind("<Leave>", _unbind_mousewheel)

        self.product_list_CLASS = product_list_CLASS
        self.receipt_gui_CLASS = receipt_gui_CLASS
        self.genres = genres
        self.buttons = []
        self.back_button = None
# ...existing code...
    def all_forget(self):
        if len(self.buttons) > 0:
            for button in self.buttons:
                 button.grid_forget()
        if self.back_button != None:
            self.back_button.grid_forget()
        self.buttons = []
    def show_buttons_genre(self):
        self.all_forget()
        for genre in self.genres:
            self.buttons.append(
                    tk.Button(
                        self.frame, 
                        text=genre,
                        command=lambda genre=genre:self.show_buttons_product(genre),
                        width=10, height=3,
                        relief=tk.RAISED,
                        bg="lightblue"
                    )
                )
        c,r = 0,0
        mc = 4
        for button in self.buttons:
            button.grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c >= mc:
                r += 1
                c = 0
    def show_buttons_product(self, showed_genre):
        self.all_forget()
        for i, product in enumerate(self.product_list_CLASS.products):
            if product.genre == showed_genre:
                self.buttons.append(
                    tk.Button(
                        self.frame, 
                        text=product.name + "\n" + str(product.price),
                        command=lambda product=product:self.add_product(product),
                        width=10, height=3,
                        relief=tk.RAISED,
                        bg="lightblue"
                    )
                )
        c,r = 0,0
        mc = 4
        for button in self.buttons:
            button.grid(row=r, column=c, padx=2, pady=2)
            c += 1
            if c >= mc:
                r += 1
                c = 0
        self.back_button = tk.Button(self.frame, text="return", command=self.show_buttons_genre)
        self.back_button.grid()

    def add_product(self, product):
        self.receipt_gui_CLASS.add(product)
