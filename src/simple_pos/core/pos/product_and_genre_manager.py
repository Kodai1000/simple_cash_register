import sys, os
import sqlite3
import toml
from pathlib import Path

def resource_path(relative_path: str) -> Path:
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parents[3] / "simple_pos"
    return base / relative_path

class product_and_genre_manager():
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parents[2]

        CONFIG_PATH = resource_path("config.toml")

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = toml.load(f)
        
        APP_DIR = Path(os.getenv("APPDATA")) / "simple_pos"
        APP_DIR.mkdir(parents=True, exist_ok=True)

        db_name = Path(config["database"]["sqlite_path"]).name
        DB_PATH = APP_DIR / db_name

        self.conn = sqlite3.connect(str(DB_PATH))


        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_list_table(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price INTEGER,
                genre_id INTEGER
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS genre_table(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
        ''')
        self.conn.commit()

    def add_genre(self, genre_name):
        self.cursor.execute('INSERT INTO genre_table (name) VALUES (?)', (genre_name,))
        self.conn.commit()

    def add_product(self, name, price, genre_id):
        self.cursor.execute('SELECT id FROM genre_table WHERE id = ?', (genre_id,))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute('INSERT INTO product_list_table (name, price, genre_id) VALUES (?,?,?)', (name, price, genre_id))
            self.conn.commit()
            return True
        return False

    def get_all_products(self):
        self.cursor.execute('SELECT id, name, price, genre_id FROM product_list_table')
        all_products = [row for row in self.cursor]
        return all_products
    
    def get_all_genres(self):
        self.cursor.execute('SELECT id, name FROM genre_table')
        all_genres = [row for row in self.cursor]
        return all_genres

    def change_product(self, id, name, price, genre_id):
        self.cursor.execute(
            'UPDATE product_list_table SET name=?, price=?, genre_id=? WHERE id=?',
            (name, price, genre_id, id)
        )
        self.conn.commit()

    def change_genre(self, id, name):
        self.cursor.execute(
            'UPDATE genre_table SET name=? WHERE id=?',
            (name, id)
        )
        self.conn.commit()

    def delete_product(self, deleted_id):
        self.cursor.execute(
            'DELETE FROM product_list_table WHERE id=?', (deleted_id, )
        )
        self.conn.commit()

    def delete_genre(self, deleted_id):
        self.cursor.execute(
            'DELETE FROM genre_table WHERE id=?', (deleted_id, )
        )
        self.conn.commit()