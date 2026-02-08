import os
import copy
import pickle
import toml
from pathlib import Path
from datetime import datetime
from pathlib import Path
import sys

def _get_base_dir() -> Path:
    """
    PyInstaller 実行時と、通常実行時の双方で使える BASE_DIR を返す
    """
    if getattr(sys, "frozen", False):  # exe 実行時
        return Path(sys._MEIPASS)
    else:  # 通常実行時
        return Path(__file__).resolve().parents[2]

class past_bought_product:
    def __init__(self, name:str, price:int, quantity:int):
        self.name = name
        self.price = price
        self.quantity = quantity

class past_receipt:
    def __init__(self, name: str, products: list, total:int):
        self.name = name
        self.bought_products = products
        self.total = total
        self.time = str(datetime.now())
    def add_bought_product(self, bought_product):
        name = copy.deepcopy(bought_product.product.name)
        price = copy.deepcopy(bought_product.product.price)
        quantity = copy.deepcopy(bought_product.quantity)
        self.bought_products.append(
            past_bought_product(name,price,quantity)
        )
    def sum_price(self):
        sum = 0
        for bought_product in self.bought_products:
            sum += bought_product.price * bought_product.quantity
        return sum

class history:
    def __init__(self):
        self.receipts = []
        self.load()
    def add(self, past_receipt):
        self.receipts.append(past_receipt)
        self.save()
    def from_table(self, table):
        new_past_receipt = past_receipt(str(datetime.now())+"のレシート", [], table.total)
        for bought_product in table.bought_products:
            new_past_receipt.add_bought_product(
                bought_product
            )
        self.add(new_past_receipt)
        
    def save(self):
        BASE_DIR = _get_base_dir()

        config_path = BASE_DIR / "config.toml"

        if not config_path.exists():
            raise FileNotFoundError(f"config.toml が見つかりません: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = toml.load(f)
        history_path = config["database"]["history_path"]
        with open(history_path, "wb") as f:
            pickle.dump(self.receipts, f)

    def load(self):
        BASE_DIR = _get_base_dir()

        config_path = BASE_DIR / "config.toml"

        if not config_path.exists():
            raise FileNotFoundError(f"config.toml が見つかりません: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            config = toml.load(f)

        history_path = config["database"]["history_path"]

        if os.path.exists(history_path):
            with open(history_path, "rb") as f:
                self.receipts = pickle.load(f)