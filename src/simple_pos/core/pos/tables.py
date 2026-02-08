from simple_pos.core.pos.products import *
from simple_pos.core.pos.history import history as History

class table(): #テーブルクラス
    def __init__(self, bought_products: list):
        self.bought_products = bought_products
        self.total = 0
    def add(self, product: product):#
        existing_product_id = self.check_product(product)
        if existing_product_id >= 0:
            self.bought_products[existing_product_id].quantity += 1
        elif existing_product_id == -1:
            self.bought_products.append(
                bought_product(
                    product, self, 1,
                )
            )
        self.totals()
    def remove(self, product:product):
        existing_product_id = self.check_product(product)
        if existing_product_id >= 0:
            self.bought_products[existing_product_id].quantity -= 1
            if self.bought_products[existing_product_id].quantity <= 0:
                self.table.bought_products.remove(self)
        self.totals()
    def check_product(self, product:product):
        for i, bought_product in enumerate(self.bought_products):
            if bought_product.product == product:
                return i
        return -1
    def check_and_delete(self):
        before = len(self.bought_products)
        self.bought_products = [
            p for p in self.bought_products if p.quantity > 0
        ]
        deleted = before - len(self.bought_products)
        self.totals()
    def show(self):
        for bought_product in self.bought_products:
            print(bought_product.product.name, bought_product.quantity)
    def totals(self):
        total = 0
        for bought_product in self.bought_products:
            total += bought_product.product.price * bought_product.quantity
        self.total = total
    def account(self, pay):
        if self.total <= pay:
            history = History()
            history.from_table(self)
            self.bought_products = []
            self.totals()
            return True
        return False
class table_list(): #テーブルリストクラス
    def __init__(self, tables:list):
        self.tables = tables
    def add(self, table:table):
        self.tables.append(table)
    def show(self):
        print("==show the product_in table:==")
        for i, table in enumerate(self.tables):
            print(" table", i)
            for product in table.bought_products:
                print("  ", product.CLASS.name, "x", product.quantity)
class bought_product(): #レシート追加済み製品クラス
    def __init__(self, product_class: product, table_class: table, quantity: int):
        self.product = product_class
        self.quantity = quantity
        self.table = table_class
    def add(self):
        self.quantity += 1
        self.table.totals()
    def remove(self):
        self.quantity -= 1
        self.table.totals()
        if self.quantity <= 0:
            self.table.bought_products.remove(self)
            return True
        return False
    def sum(self):
        return self.product.price*self.quantity
                