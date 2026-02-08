import sys, os
from pathlib import Path
def resource_path(relative_path: str):
    if hasattr(sys, "_MEIPASS"):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parents[3] / "simple_pos"
    return base / relative_path