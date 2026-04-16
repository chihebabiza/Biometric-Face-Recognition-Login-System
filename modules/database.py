import pickle
import os
from config import DB_PATH

def load_users():
    if not os.path.exists(DB_PATH):
        return {}

    try:
        with open(DB_PATH, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        # file is empty or corrupted → reset it safely
        return {}

def save_users(users):
    os.makedirs("database", exist_ok=True)
    with open(DB_PATH, "wb") as f:
        pickle.dump(users, f)