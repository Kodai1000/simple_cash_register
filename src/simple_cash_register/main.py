from simple_cash_register.apps.launcher import main as launcher_main

import tkinter as tk
import tkinter.font as tkFont
root = tk.Tk()
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12, weight='bold')
launcher = launcher_main(root)