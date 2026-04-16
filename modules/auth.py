import numpy as np
from modules.database import load_users, save_users

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def register_user(username, embedding):
    users = load_users()
    users[username] = embedding
    save_users(users)

def authenticate_user(embedding, threshold=0.6):
    users = load_users()

    for username, stored_embedding in users.items():
        sim = cosine_similarity(embedding, stored_embedding)

        if sim > threshold:
            return username, sim

    return None, None