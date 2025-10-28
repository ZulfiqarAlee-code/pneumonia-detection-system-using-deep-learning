# Pneumonia Detection System Using Deep Learning

## Description
This project is a **Pneumonia Detection System** that uses deep learning (TensorFlow/Keras) to analyze chest X-ray images and detect pneumonia.  
It provides a GUI built with **Tkinter** for user signup, login, image upload, prediction, and PDF report generation.

---
```
Project Structure
Pneumonia-Detection-System/
│
├─ main.py                 # Entry point of the application
├─ model.py                # Loads the trained deep learning model
├─ signup.py               # Handles user registration
├─ login.py                # Handles user login
├─ detection.py            # Image upload, prediction, and report generation
├─ database.py             # Database setup and password hashing
├─ models/
│   └─ model.h5            # Pre-trained deep learning model
├─ Images/                 # Contains background and interface images
├─ Reports/                # Folder where generated PDF reports are saved
└─ README.md               # Project documentation


```
## Prerequisites & Installation

Make sure you have **Python 3.9+** installed.

### 1. Create a virtual environment


# 1. Create virtual environment (if not already created)
```
python -m venv venv
```
# 2. Activate virtual environment

# Windows (CMD)
```
venv\Scripts\activate
```
# Windows (Git Bash / MINGW64)
```
source venv/Scripts/activate
```
# Linux / macOS
```
source venv/bin/activate
```

# 3. Install project dependencies
```
pip install -r requirements.txt
```
# 4.Download Chest X-ray dataset and put in main directory
**Chest X-ray Images (Pneumonia) Dataset:** [Download from Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)

