from PIL import Image, ImageDraw, ImageFont
import win32print
import win32ui
from PIL import Image, ImageWin
from simple_cash_register.core.register.tables import *
from simple_cash_register.core.register.products import product
from simple_cash_register.core.register.option import option as Option
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

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def draw_right_line(draw, y, label, price, font, width, margin=20):
    draw.text((0, y), label, fill="black", font=font)

    bbox = draw.textbbox((0, 0), price, font=font)
    text_width = bbox[2] - bbox[0]
    x = width - text_width - margin

    draw.text((x, y), price, fill="black", font=font)


def print_receipt(Table, mode="normal"):
    option = Option()
    option.load()

    bought_products = Table.bought_products

    # フォントサイズを分ける
    title_font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 60)
    normal_font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 35)
    total_font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 40)

    margin = 60
    img_width = 400
    img_height = margin * (len(bought_products) * 2 + 20)
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    y = 0
    sum_price = 0

    # ===== タイトル =====
    draw.text((0, y), option.shop_name, font=title_font, fill="black")
    y += margin

    draw.text((0, y), f"テーブル名: {Table.name}", fill="black", font=normal_font)
    y += margin

    draw.text((0, y), str(datetime.now()), fill="black", font=normal_font)
    y += margin

    draw.text((0, y), " ===== ", fill="black", font=title_font)
    y += margin

    # ===== 商品一覧 =====
    for bought_product in bought_products:
        name_line = f"{bought_product.product.name} x {bought_product.quantity}"
        price_line = f"   \ {bought_product.product.price} x {bought_product.quantity} = \ {bought_product.product.price * bought_product.quantity}"

        draw.text((0, y), name_line, fill="black", font=normal_font)
        y += margin

        price_line = f"{bought_product.product.price} x {bought_product.quantity} = {bought_product.product.price * bought_product.quantity}"

        draw_right_line(draw, y, "", price_line, normal_font, img_width)
        y += margin

        sum_price += bought_product.product.price * bought_product.quantity

    # ===== 合計 =====
    y += margin
    draw_right_line(draw, y, "合計", f"\ {sum_price}", total_font, img_width)
    y += margin
    if mode == "normal":
        draw_right_line(draw, y, "お支払", f"\ {Table.pay}", total_font, img.width)
        y += margin
        draw_right_line(draw, y, "お釣", f"\ {Table.pay - sum_price}", total_font, img_width)
        y += margin
    # ==== 情報 ======
    text = ">\n>\n>\n\n\n\n\n>\n>"
    draw.text((0, y), text, font=normal_font, fill="black")

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