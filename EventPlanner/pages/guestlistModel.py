import os

SAVE_PATH = "C:/EventPlanner/guests.txt"

def get_save_path():
    folder = os.path.dirname(SAVE_PATH)
    os.makedirs(folder, exist_ok=True)
    return SAVE_PATH
