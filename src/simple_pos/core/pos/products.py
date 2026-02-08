from simple_pos.core.pos.product_and_genre_manager import *
class product(): #製品クラス
    def __init__(self, name, price, genre):
        self.name = name
        self.price = price
        self.genre = genre
class product_list(): #製品一覧クラス
    def __init__(self, products:list):
        self.products = products
    def add(self, product:product):
        self.products.append(
            product
        )
    def delete(self, i:int):
        del self.products[i]
    def show(self):
        print("==show the product_list==")
        for product in self.products:
            print(" ", product.name, product.price, product.genre)
class product_data_base():
    def __init__(self):
        self.manager = product_and_genre_manager()
    def get_genre_name(self, genres, id):
        for genre in genres:
            if genre[0] == id:
                return genre[1]
    def load(self):
        genres = self.manager.get_all_genres()
        product_datas = self.manager.get_all_products()
        product_classes_list = product_list([])
        for product_data in product_datas:
            product_classes_list.add(
                product(
                    product_data[1],
                    product_data[2],
                    self.get_genre_name(genres, product_data[3])
                )    
            )
        genre_names = []
        for genre in genres:
            genre_names.append(genre[1])
        return product_classes_list, genre_names