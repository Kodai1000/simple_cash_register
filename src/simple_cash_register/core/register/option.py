from simple_cash_register.utils.base_dir import get_base_data_dir
from simple_cash_register.utils.base_dir import make_dir
import pickle
import os

class option:
    def __init__(self):
        self.filepath = get_base_data_dir() / "data/option"
        self.shop_name = ""
    def save(self):
        print("SAVE")
        data = {
            "shop_name": self.shop_name
        }
        with open(self.filepath, "wb") as f:
            pickle.dump(data, f)
    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "rb") as f:
                data = pickle.load(f)
                self.shop_name = data["shop_name"]
    def add_shop_name(self, shop_name):
        self.shop_name = shop_name