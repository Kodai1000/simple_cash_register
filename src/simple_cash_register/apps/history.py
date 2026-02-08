import tkinter as tk
from tkinter import ttk
from simple_cash_register.core.register.history import *

def show_history_table(ROOT, history_obj):
    root = ROOT
    root.title("購入履歴")
    root.geometry("800x500")

    # フレーム
    frame = ttk.Frame(root)
    frame.pack(fill="both", expand=True)

    # 列定義
    columns = ("col1", "col2", "col3", "col4")

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="tree headings"
    )

    # 見出し
    tree.heading("#0", text="種別")
    tree.heading("col1", text="名称")
    tree.heading("col2", text="単価 / 合計")
    tree.heading("col3", text="数量")
    tree.heading("col4", text="小計 / 時刻")

    # 列幅
    tree.column("#0", width=100)
    tree.column("col1", width=250)
    tree.column("col2", width=120)
    tree.column("col3", width=80)
    tree.column("col4", width=180)

    # スクロールバー
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    tree.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # ===== データ投入 =====
    for i, receipt in enumerate(history_obj.receipts):
        # 親ノード（レシート）
        parent_id = tree.insert(
            "",
            "end",
            text="レシート",
            values=(
                receipt.name,
                f"¥{receipt.total:,}",
                "",
                receipt.time
            )
        )

        # 子ノード（商品）
        for p in receipt.bought_products:
            subtotal = p.price * p.quantity
            tree.insert(
                parent_id,
                "end",
                text="商品",
                values=(
                    p.name,
                    f"¥{p.price:,}",
                    p.quantity,
                    f"¥{subtotal:,}"
                )
            )

    root.mainloop()

def main(ROOT):
    h = history()      # 既存の履歴を load() している前提
    show_history_table(ROOT, h)