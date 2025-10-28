import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import logging
from tkinter import messagebox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL_PATH = os.path.join("models", "model.h5")

def check_model_path():
    exists = os.path.exists(MODEL_PATH)
    size = os.path.getsize(MODEL_PATH) if exists else "N/A"
    logging.info(f"Model Path: {MODEL_PATH}")
    logging.info(f"Exists? {exists}")
    logging.info(f"Size: {size}")
    logging.info(f"TensorFlow Version: {tf.__version__}")
    return exists

def get_model():
    global model
    if 'model' not in globals():
        if not check_model_path():
            messagebox.showerror("Model Error", f"Model file not found at: {MODEL_PATH}")
            raise SystemExit("Model file not found")
        try:
            model = load_model(MODEL_PATH, compile=False)
            logging.info("Model loaded successfully")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            messagebox.showerror("Model Loading Error", f"Error loading model:\n{e}")
            raise SystemExit(f"Failed to load the model: {e}")
    return model
