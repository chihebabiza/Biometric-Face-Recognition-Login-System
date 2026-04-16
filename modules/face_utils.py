from deepface import DeepFace
import numpy as np
from config import MODEL_NAME, DETECTOR_BACKEND

def get_embedding(image):
    try:
        embedding = DeepFace.represent(
            img_path=image,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True
        )
        return np.array(embedding[0]["embedding"])
    except:
        return None