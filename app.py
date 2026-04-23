import streamlit as st
import cv2
import numpy as np
import pandas as pd

from modules.face_utils import get_embedding
from modules.auth import (
    register_user,
    authenticate_user,
    get_top_matches,
    add_user_images,
)
from modules.history import log_attempt
from modules.database import load_users


# ================= SIDEBAR =================
st.sidebar.title("🔐 Navigation")
page = st.sidebar.selectbox("Choose Page", ["Login", "Register"])

register_mode = None
if page == "Register":
    register_mode = st.sidebar.radio(
        "Register Mode",
        ["Register New User", "Add Images to Existing User"]
    )


# ================= TITLE =================
st.title("DeepFace Biometric Security System")


# ================= LOGIN =================
if page == "Login":

    st.subheader("Login System")

    input_mode = st.radio("Choose input method", ["Upload Image", "Camera"])

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

        if st.button("Login"):

            embedding = get_embedding(image)

            if embedding is None:
                st.error("No face detected")
                st.stop()

            top_matches = get_top_matches(embedding)

            st.subheader("Top Matches")

            for name, score in top_matches:
                st.write(name, score)
                st.progress(float(score))

            user, score = authenticate_user(embedding)

            safe_score = float(score) if score is not None else 0.0

            if user is not None:
                add_user_images(user, embedding)
                st.success(f"Welcome {user}")
                log_attempt(user, "SUCCESS", safe_score)
            else:
                st.error("Access Denied")
                log_attempt("UNKNOWN", "FAIL", safe_score)


# ================= REGISTER =================
elif page == "Register":

    st.subheader("User Registration System")

    if "camera_images" not in st.session_state:
        st.session_state.camera_images = []

    uploaded_files = None
    images_to_process = []

    # ======================================================
    # MODE 1: REGISTER NEW USER
    # ======================================================
    if register_mode == "Register New User":

        username = st.text_input("Enter username")

        input_mode = st.radio("Choose input method", ["Upload Images", "Use Camera"])

        # ---------------- UPLOAD ----------------
        if input_mode == "Upload Images":

            uploaded_files = st.file_uploader(
                "Upload 3–5 face images",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
            )

        # ---------------- CAMERA ----------------
        elif input_mode == "Use Camera":

            camera_image = st.camera_input("Capture face image")

            if camera_image:
                file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, 1)

                st.image(image, channels="BGR")

                if st.button("➕ Add Capture"):
                    st.session_state.camera_images.append(image)
                    st.success("Image added!")

        # ---------------- REGISTER BUTTON ----------------
        if st.button("Register User"):

            if not username:
                st.warning("Enter username")
                st.stop()

            # upload images
            if uploaded_files:
                for file in uploaded_files:
                    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                    image = cv2.imdecode(file_bytes, 1)
                    images_to_process.append(image)

            # camera images
            images_to_process.extend(st.session_state.camera_images)

            if len(images_to_process) == 0:
                st.warning("No images provided")
                st.stop()

            for image in images_to_process:
                embedding = get_embedding(image)
                if embedding is not None:
                    register_user(username, embedding)

            st.session_state.camera_images = []
            st.success("User registered successfully")


    # ======================================================
    # MODE 2: ADD IMAGES TO EXISTING USER
    # ======================================================
    elif register_mode == "Add Images to Existing User":

        users_list = list(load_users().keys())

        if not users_list:
            st.info("No users available")
            st.stop()

        selected_user = st.selectbox("Select user", users_list)

        input_mode = st.radio("Choose input method", ["Upload Images", "Use Camera"])

        new_files = None

        # ---------------- UPLOAD ----------------
        if input_mode == "Upload Images":

            new_files = st.file_uploader(
                "Upload face images",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
            )

        # ---------------- CAMERA ----------------
        elif input_mode == "Use Camera":

            camera_image = st.camera_input("Capture face image")

            if camera_image:
                file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, 1)

                st.image(image, channels="BGR")

                if st.button("➕ Add Capture"):
                    st.session_state.camera_images.append(image)
                    st.success("Image added!")

        # ---------------- ADD IMAGES BUTTON ----------------
        if st.button("Add Images"):

            images_to_process = []

            if new_files:
                for file in new_files:
                    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
                    image = cv2.imdecode(file_bytes, 1)
                    images_to_process.append(image)

            images_to_process.extend(st.session_state.camera_images)

            if len(images_to_process) == 0:
                st.warning("No images provided")
                st.stop()

            for image in images_to_process:
                embedding = get_embedding(image)
                if embedding is not None:
                    add_user_images(selected_user, embedding)

            st.session_state.camera_images = []
            st.success(f"Images added to {selected_user}")


# ================= COMMON SECTIONS =================
st.markdown("---")
st.subheader("Logs")

try:
    df = pd.read_csv("database/logs.csv")
    st.dataframe(df)
    st.bar_chart(df["status"].value_counts())
except:
    st.info("No logs yet")

st.markdown("---")
st.subheader("Users Database")

users = load_users()

if users:
    for u, v in users.items():
        st.write(f"👤 {u} → {len(v)} samples")
else:
    st.info("No users")

st.markdown("---")
st.subheader("📈 Analytics")

try:
    df = pd.read_csv("database/logs.csv")

    total = len(df)
    success = len(df[df["status"] == "SUCCESS"])
    fail = len(df[df["status"] == "FAIL"])

    st.metric("Total", total)
    st.metric("Success", success)
    st.metric("Fail", fail)

    if total > 0:
        st.progress(success / total)

except:
    st.info("No data")