from typing import Tuple


def get_primary_display_size() -> Tuple[int, int]:
    try:
        import pyautogui  # local import to avoid hard dependency at import time
        w, h = pyautogui.size()
        return int(w), int(h)
    except Exception:
        return 1024, 768


