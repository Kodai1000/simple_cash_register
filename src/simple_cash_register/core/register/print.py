from PIL import Image, ImageDraw, ImageFont
import win32print
import win32ui
from PIL import Image, ImageWin
from simple_cash_register.core.register.tables import *
from simple_cash_register.core.register.products import product
from datetime import datetime

def print_pil_image(img):
    # デフォルトプリンタ取得
    printer_name = win32print.GetDefaultPrinter()

    # プリンタDC作成
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    hDC.StartDoc("PIL Print Job")
    hDC.StartPage()

    # 画像をRGBに変換（重要）
    if img.mode != "RGB":
        img = img.convert("RGB")

    # DIBに変換
    dib = ImageWin.Dib(img)

    # 印刷可能領域取得
    printable_area = hDC.GetDeviceCaps(8), hDC.GetDeviceCaps(10)

    # 画像サイズ
    img_width, img_height = img.size

    # そのままサイズで印刷（必要なら拡大縮小する）
    dib.draw(hDC.GetHandleOutput(), (0, 0, img_width, img_height))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

def print_receipt(Table):
    bought_products = Table.bought_products
    font_size = 45
    margin_size = 100
    img = Image.new("RGB", (400,margin_size*(len(bought_products)+5)), "white")
    font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", font_size)
    draw = ImageDraw.Draw(img)
    text = " ===== \nテーブル名: " + Table.name + "\n" + str(datetime.now()) + "\n =====\n"
    sum = 0
    for i, bought_product in enumerate(bought_products):
        text += bought_product.product.name + " x " + str(bought_product.quantity) + "\n   " + str(bought_product.product.price) + " x " + str(bought_product.quantity) + " = " + str(bought_product.product.price*bought_product.quantity)
        sum += bought_product.product.price * bought_product.quantity
    text += "\n合計 " + str(sum)
    text += "\n\n\n  ====== \n\n\n"
    draw.text((0,0),text,fill="black",font=font)
    #img.show()
    try:
        print_pil_image(img)
    except:
        print("印刷に失敗しました。")

"""
product = product("テスト", 100, 0)
table = table([])
bought_product = bought_product(product, table, 1)
print_receipt([bought_product])
"""

"""
# ① 画像を作る（白背景）
img = Image.new("RGB", (400, 200), "white")

# ② 描画オブジェクトを作る
draw = ImageDraw.Draw(img)

# ③ フォントを指定（Windows標準フォント）
font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 40)

# ④ 文字を書く
draw.text((50, 50), "こんにちは", fill="black", font=font)

"""