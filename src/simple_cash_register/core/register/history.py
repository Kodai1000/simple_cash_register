import os
import copy
import pickle
import toml
from pathlib import Path
from datetime import datetime
from pathlib import Path
import sys
from simple_cash_register.utils.base_dir import get_base_data_dir

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
        self.filepath = "data/history"
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
        BASE_DIR = get_base_data_dir()
        with open(self.filepath, "wb") as f:
            pickle.dump(self.receipts, f)

    def load(self):
        BASE_DIR = get_base_data_dir()

        if os.path.exists(self.filepath):
            with open(self.filepath, "rb") as f:
                self.receipts = pickle.load(f)