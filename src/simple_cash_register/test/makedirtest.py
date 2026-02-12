from simple_cash_register.utils.base_dir import get_base_data_dir
from simple_cash_register.utils.base_dir import make_dir
print(get_base_data_dir())
a = input("何かボタンを押してください。")
try:
    make_dir("test_folder")
except:
    print("失敗！")
b = input("何かボタンを押してください。")