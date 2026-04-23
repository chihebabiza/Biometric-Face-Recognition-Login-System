import cv2
from deepface import DeepFace
import numpy as np
from config import MODEL_NAME, DETECTOR_BACKEND


def get_embedding(image):
    try:
        embedding = DeepFace.represent(
            img_path=image,
            model_name=MODEL_NAME,
            detector_backend=DETECTOR_BACKEND,
            enforce_detection=True,
        )
        return np.array(embedding[0]["embedding"])
    except:
        return None


# def is_real_face(image, threshold=50):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

#     return blur_score > threshold