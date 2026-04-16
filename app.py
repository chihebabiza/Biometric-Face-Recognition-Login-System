import streamlit as st
import cv2
import numpy as np

from modules.face_utils import get_embedding, is_real_face
from modules.auth import register_user, authenticate_user, get_top_matches
from modules.history import log_attempt

st.title("🔐 DeepFace Biometric Security System")

menu = st.sidebar.selectbox("Menu", ["Register", "Login"])

# ======================================================
# 🧑 REGISTER (MULTIPLE IMAGES ONLY)
# ======================================================
if menu == "Register":

    st.subheader("🧑 User Registration")

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

            # 🚫 spoof check
            blur_score = is_real_face(image)

            st.write("Image quality score:", blur_score)

            if blur_score < 10:
                st.error("Image too blurry")
                st.stop()

            embedding = get_embedding(image)

            if embedding is not None:
                register_user(username, embedding)

        st.success(f"User {username} registered successfully 🎉")

# ======================================================
# 🔐 LOGIN (CAMERA OR SINGLE IMAGE)
# ======================================================
elif menu == "Login":

    st.subheader("🔐 Login System")

    input_mode = st.radio("Choose input method", ["Upload Image", "Camera"])

    image = None

    # 📸 CAMERA
    if input_mode == "Camera":
        img_file = st.camera_input("Capture your face")

        if img_file:
            file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)

    # 📁 UPLOAD
    else:
        uploaded_file = st.file_uploader(
            "Upload face image", type=["jpg", "jpeg", "png"]
        )

        if uploaded_file is not None:
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)

    # ==================================================
    # PROCESS LOGIN IMAGE
    # ==================================================
    if image is not None:

        st.image(image, channels="BGR", caption="Input Image")

        # 🚫 spoof detection
        if not is_real_face(image):
            st.error("🚫 Spoof detected! Please use a real face.")
            st.stop()

        embedding = get_embedding(image)

        if embedding is None:
            st.error("No face detected!")
            st.stop()

        if st.button("Login"):

            # 📊 Top matches
            st.subheader("📊 Top 3 Matches")

            top_matches = get_top_matches(embedding)

            for name, score in top_matches:
                st.write(f"👤 {name}: {score:.2f}")
                st.progress(float(score))

            # 🔐 authentication
            user, score = authenticate_user(embedding)

            if user:
                st.success(f"Welcome {user} 🎉")
                st.info(f"Confidence Score: {score:.2f}")
                log_attempt(user, "SUCCESS")
            else:
                st.error("Access Denied ❌")
                log_attempt("UNKNOWN", "FAIL")
