import streamlit as st
import cv2
import numpy as np

from modules.face_utils import get_embedding, is_real_face
from modules.auth import (
    register_user,
    authenticate_user,
    get_top_matches,
    add_user_images,
)
from modules.history import log_attempt
from modules.database import load_users

st.title("DeepFace Biometric Security System")

menu = st.sidebar.selectbox("Menu", ["Register", "Login"])

if menu == "Register":

    st.subheader("User Registration")

    username = st.text_input("Enter username")

    uploaded_files = st.file_uploader(
        "Upload 3–5 face images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
    )

    if st.button("Register User"):

        if not username:
            st.warning("Please enter username")
            st.stop()

        if not uploaded_files:
            st.warning("Please upload at least 3 images")
            st.stop()

        for file in uploaded_files:

            file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)

            if not is_real_face(image):
                continue

            embedding = get_embedding(image)

            if embedding is not None:
                register_user(username, embedding)

        st.success(f"User {username} registered successfully")

    st.markdown("---")
    st.subheader("Add images to existing user")

    users_list = list(load_users().keys())

    if users_list:

        selected_user = st.selectbox("Select user", users_list)

        new_files = st.file_uploader(
            "Upload new face images",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="add_images",
        )

        if st.button("Add Images to User"):

            if not new_files:
                st.warning("Please upload images")
                st.stop()

            for file in new_files:

                file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, 1)

                embedding = get_embedding(image)

                if embedding is not None:
                    add_user_images(selected_user, embedding)

            st.success(f"Images added to {selected_user}")

    else:
        st.info("No users registered yet")

elif menu == "Login":

    st.subheader("Login System")

    input_mode = st.radio("Choose input method", ["Camera", "Upload Image"])

    image = None

    if input_mode == "Camera":
        img_file = st.camera_input("Capture your face")

        if img_file:
            file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)

    else:
        uploaded_file = st.file_uploader(
            "Upload face image", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)

    if image is not None:

        st.image(image, channels="BGR")

        if not is_real_face(image):
            st.error("Spoof detected")
            st.stop()

        embedding = get_embedding(image)

        if embedding is None:
            st.error("No face detected")
            st.stop()

        if st.button("Login"):

            top_matches = get_top_matches(embedding)

            st.subheader("Top Matches")

            for name, score in top_matches:
                st.write(name, score)
                st.progress(float(score))

            user, score = authenticate_user(embedding)

            if user:
                st.success(f"Welcome {user}")
                log_attempt(user, "SUCCESS")
            else:
                st.error("Access Denied")
                log_attempt("UNKNOWN", "FAIL")
