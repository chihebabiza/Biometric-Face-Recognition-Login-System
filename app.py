import streamlit as st
import cv2
import numpy as np
from modules.face_utils import get_embedding
from modules.auth import register_user, authenticate_user

st.title("🔐 DeepFace Biometric Login System")

menu = st.sidebar.selectbox("Menu", ["Register", "Login"])

input_mode = st.radio("Choose input method", ["Camera", "Upload Image"])

image = None

# 📸 CAMERA MODE
if input_mode == "Camera":
    img_file = st.camera_input("Take a picture")

    if img_file:
        file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

# 📁 UPLOAD MODE
else:
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)

# ---------------- PROCESS IMAGE ----------------

if image is not None:
    embedding = get_embedding(image)

    if embedding is None:
        st.error("No face detected!")
    else:

        # ========== REGISTER ==========
        if menu == "Register":
            username = st.text_input("Enter username")

            if st.button("Register"):
                if username:
                    register_user(username, embedding)
                    st.success("User registered successfully!")
                else:
                    st.warning("Please enter a username")

        # ========== LOGIN ==========
        elif menu == "Login":

            if st.button("Login"):
                user, score = authenticate_user(embedding)

                if user:
                    st.success(f"Welcome {user} 🎉")
                    st.info(f"Similarity score: {score:.2f}")
                else:
                    st.error("Access Denied ❌")
