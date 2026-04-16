# 🔐 DeepFace Biometric Security System (Streamlit)

An AI-powered biometric authentication system built with **Streamlit** and **DeepFace**.  
It supports face registration, multi-image enrollment, login verification, confidence scoring, anti-spoofing, and login history tracking.

---

# 🚀 Features

## 🧑 User Management
- Register users with multiple face images (3–5 recommended)
- Add more images to existing users anytime
- Store multiple embeddings per user for better accuracy

## 🔐 Authentication
- Face login using webcam or uploaded image
- DeepFace-based face embeddings
- Cosine similarity matching
- Top-3 match display

## 📊 AI Dashboard
- Shows similarity scores
- Progress bar for confidence
- Top matching users preview

## 🚫 Anti-Spoofing (Basic)
- Detects blurry or low-quality images
- Rejects suspicious inputs

## 🧾 Logging System
- Records login attempts
- Stores success/failure with timestamps

---

# 🧠 Tech Stack

- Streamlit
- OpenCV
- DeepFace
- NumPy
- Pickle (local database)
- CSV (logs)

---

# 📁 Project Structure

```

biometric_app/
│
├── app.py
├── config.py
│
├── database/
│   ├── users.pkl
│   └── logs.csv
│
├── modules/
│   ├── auth.py
│   ├── face_utils.py
│   ├── database.py
│   └── history.py
│
└── requirements.txt

````

---

# ⚙️ Installation

## 1. Clone project
```bash
git clone https://github.com/your-username/biometric-app.git
cd biometric-app
````

## 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the App

```bash
streamlit run app.py
```

---

# 🧑 Register User

1. Go to **Register**
2. Enter username
3. Upload 3–5 face images
4. System extracts embeddings and stores them

### ➕ Add more images later

* Select existing user
* Upload new images
* System appends embeddings automatically

---

# 🔐 Login System

1. Go to **Login**
2. Choose:

   * 📸 Camera
   * 📁 Upload image
3. Click **Login**
4. System:

   * Extracts face embedding
   * Compares with database
   * Shows top matches
   * Grants or denies access

---

# 📊 Output Example

```
Top Matches:
chiheb → 0.78
ali → 0.41
unknown → 0.22

Welcome chiheb 🎉
```

or

```
Access Denied ❌
```

---

# 🚫 Anti-Spoofing

The system blocks:

* Blurry images
* Low-quality inputs
* Fake-like face captures

---

# 🧾 Login Logs

Each attempt is saved:

| Username | Time  | Status  |
| -------- | ----- | ------- |
| chiheb   | 10:30 | SUCCESS |
| unknown  | 10:32 | FAIL    |

---

# 🧠 How It Works

1. Face is detected from image
2. DeepFace converts face → embedding vector
3. Cosine similarity compares embeddings
4. Best match is selected
5. Threshold decides access

---

# 📊 Matching Logic

* Each user has multiple embeddings
* System compares input face with ALL stored samples
* Best similarity per user is used
* Top users are ranked

---

# ⚠️ Limitations

* Not production-level security
* Sensitive to lighting conditions
* Basic anti-spoofing only
* Uses local storage (pickle)

---

# 🚀 Future Improvements

* 🔥 SQLite or cloud database
* 🔥 Strong liveness detection (blink/head movement)
* 🔥 Face quality scoring system
* 🔥 User dashboard analytics
* 🔥 Real-time video authentication
* 🔥 Deployment on Streamlit Cloud

---

# 👨‍💻 Author

Built as a student AI project for learning biometric authentication systems using Deep Learning.
