import numpy as np
from modules.database import load_users, save_users


def register_user(username, embedding):
    users = load_users()

    if username not in users:
        users[username] = []

    # store as list for safe serialization
    users[username].append(embedding.tolist())

    save_users(users)


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    denom = np.linalg.norm(a) * np.linalg.norm(b)

    if denom == 0:
        return 0.0

    return float(np.dot(a, b) / denom)


def authenticate_user(embedding, threshold=0.5):
    users = load_users()

    best_user = None
    best_score = 0.0

    for username, embeddings in users.items():
        for stored in embeddings:
            score = cosine_similarity(embedding, stored)

            if score > best_score:
                best_score = score
                best_user = username

    if best_score > threshold:
        return best_user, best_score

    return None, None


def get_top_matches(embedding, top_k=3):
    users = load_users()
    scores = []

    for username, embeddings in users.items():
        best_score = 0.0

        for stored in embeddings:
            score = cosine_similarity(embedding, stored)

            if score > best_score:
                best_score = score

        scores.append((username, best_score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def add_user_images(username, embedding):
    users = load_users()

    if username not in users:
        return False

    users[username].append(embedding.tolist())
    save_users(users)

    return True