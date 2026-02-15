import tkinter as tk

class table_list_gui():
    def __init__(self, frame, table_list_CLASS, receipt_CLASS):
        self.canvas = tk.Canvas(frame)
        self.canvas.pack()
        self.frame = tk.Frame(self.canvas, bg="red")
        self.frame.pack()
        self.table_list_CLASS = table_list_CLASS
        self.receipt = receipt_CLASS
    def show_buttons(self):
        self.buttons = [tk.Button(self.frame, text="table " + str(i), command=lambda i=i:self.change_table(i)) for i, table in enumerate(self.table_list_CLASS.tables)]
        self.change_table(0)
        for button in self.buttons:
            button.pack(side='left')
    def change_table(self, i):
        for button in self.buttons:
            button['bg'] = "white"
        self.buttons[i]['bg'] = "red"
        self.receipt.change_table(self.table_list_CLASS.tables[i])
        self.receipt.initialize_buttons()
