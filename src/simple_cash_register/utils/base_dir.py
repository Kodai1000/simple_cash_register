import sys, os
from pathlib import Path
import os
import sys
from pathlib import Path

def get_base_data_dir() -> Path:
    """
    PyInstaller 実行時でも通常実行時でも
    書き込み可能なアプリ用ディレクトリを返す
    """
    if getattr(sys, "frozen", False):
        # exe 実行時
        base_dir = Path(sys.executable).parent
    else:
        # 通常実行時
        base_dir = Path(__file__).resolve().parent

    return base_dir

def make_dir(folder_name):
    path = get_base_data_dir() / folder_name
    if not os.path.isdir(path):
        os.makedirs(path)