# 🔐 Biometric Face Recognition Login System (Streamlit + DeepFace)

A simple AI-based biometric authentication system built with **Streamlit** and **DeepFace**.
Users can register and log in using their face via webcam or uploaded images.

---

## 🚀 Features

* 📸 Face recognition login system
* 🧑 User registration with face embedding
* 📁 Upload image OR use webcam
* 🧠 DeepFace-powered face embeddings
* 🔐 Similarity-based authentication
* 📊 Shows confidence score
* 💾 Local database storage (pickle)

---

## 🧠 Tech Stack

* Streamlit
* OpenCV
* DeepFace
* NumPy
* Pickle (local storage)

---

## 📁 Project Structure

```text
biometric_app/
│
├── app.py                  # Main Streamlit app
├── config.py              # Configuration settings
│
├── database/
│   └── users.pkl          # Stored face embeddings
│
├── modules/
│   ├── face_utils.py      # Face embedding extraction
│   ├── auth.py            # Authentication logic
│   └── database.py        # Save/load users
│
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the project

```bash
git clone https://github.com/your-username/biometric-app.git
cd biometric-app
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🧪 How It Works

### 🧑 Register User

1. Go to **Register**
2. Enter username
3. Capture or upload face image
4. System stores face embedding

---

### 🔐 Login User

1. Go to **Login**
2. Capture or upload face image
3. System compares face with database
4. If similarity is high → access granted

---

## 🧠 AI Model Used

This project uses:

DeepFace

It converts face images into numerical embeddings and compares them using cosine similarity.

---

## ⚠️ Notes

* This is a **demo project**, not production-grade security
* Accuracy depends on lighting, image quality, and angle
* First-time login requires prior registration

---

## 🔧 Common Issues

### ❌ "Access Denied"

* Face not registered
* Low similarity score
* Different lighting or angle

### ❌ No face detected

* Image too blurry
* Face not visible

---

## 📈 Future Improvements

* 🔥 SQLite database instead of pickle
* 👥 Multiple images per user
* 🚫 Anti-spoofing detection
* 📊 Login history tracking
* 🌐 Deploy on Streamlit Cloud

---

## 👨‍💻 Author

Built as a student project for learning biometrics and AI authentication systems.

---

## 📜 License

This project is for educational purposes only.

