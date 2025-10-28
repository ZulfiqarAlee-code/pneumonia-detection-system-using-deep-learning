import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import logging
import os  # ✅ for saving reports in a folder
from models.model import get_model


# ---------------- Logging Setup ----------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ---------------- Detection Window ----------------
class DetectionWindow:
    def __init__(self, root, email):
        self.root = root
        self.email = email
        self.root.title("Pneumonia Detection")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Header
        self.header_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=10)
        self.header_frame.pack(fill="x")

        tk.Label(
            self.header_frame,
            text="Pneumonia Detection System by using Deep Learning",
            font=("Arial", 18, "bold"),
            fg="#4B0082",
            bg="#FFFFFF",
        ).pack(side="left", pady=5)

        # ✅ Log Out button in header
        tk.Button(
            self.header_frame,
            text="Log Out",
            command=self.log_out,
            bg="#4B0082",
            fg="white",
            activeforeground="white",
            activebackground="#FF4C4C",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=5,
        ).pack(side="right")

        # Canvas
        self.canvas = tk.Canvas(
            root, width=screen_width, height=screen_height, bg="#4B0082", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(
            screen_width * 0.5, 0, screen_width, screen_height, fill="#6A0DAD", outline=""
        )

        # Form frame
        self.form_frame = tk.Frame(root, bg="white", padx=30, pady=30)
        self.form_frame.place(relx=0.3, rely=0.5, anchor="center")

        tk.Label(
            self.form_frame,
            text="Pneumonia Detection System",
            font=("Arial", 12),
            fg="#4B0082",
            bg="white",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        tk.Label(
            self.form_frame,
            text="DETECTION",
            font=("Arial", 24, "bold"),
            fg="#4B0082",
            bg="white",
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Upload button
        tk.Label(
            self.form_frame,
            text="Please Upload an X-ray Image",
            font=("Arial", 12),
            fg="#4B0082",
            bg="white",
        ).grid(row=2, column=0, columnspan=2, pady=5)

        tk.Button(
            self.form_frame,
            text="Choose File",
            command=self.upload_image,
            bg="#4B0082",
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
        ).grid(row=3, column=0, columnspan=2, pady=10)

        self.image_label = tk.Label(root, bg="#6A0DAD")
        self.image_label.place(
            relx=0.7, rely=0.5, anchor="center", width=screen_width * 0.2, height=screen_height * 0.6
        )

        self.predict_button = tk.Button(
            self.form_frame,
            text="Predict",
            command=self.predict,
            bg="#4B0082",
            fg="white",
            activeforeground="white",
            activebackground="#4B0082",
            font=("Arial", 12, "bold"),
            width=20,
            state=tk.DISABLED,
        )
        self.predict_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(
            self.form_frame, text="", font=("Arial", 14), fg="#4B0082", bg="white"
        )
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

        self.report_button = tk.Button(
            self.form_frame,
            text="Generate Report",
            command=self.regenerate_report,
            bg="#4B0082",
            fg="white",
            activeforeground="white",
            activebackground="#4B0082",
            font=("Arial", 12, "bold"),
            width=20,
            state=tk.DISABLED,
        )
        self.report_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.image_path = None
        self.result = None

    # ---------------- Upload Image ----------------
    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            try:
                img = Image.open(self.image_path)
                # Check if image is grayscale (chest X-rays are typically in 'L' mode)
                if img.mode != "L":
                    messagebox.showwarning("Warning", "Only chest X-ray images (grayscale) can be uploaded.")
                    self.predict_button.config(state=tk.DISABLED)
                    self.image_label.config(image="")
                    self.image_path = None
                    return

                # Resize and display
                img = img.resize(
                    (int(self.root.winfo_screenwidth() * 0.2), int(self.root.winfo_screenheight() * 0.6)),
                    Image.Resampling.LANCZOS,
                )
                self.photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.photo)
                self.image_label.image = self.photo
                self.predict_button.config(state=tk.NORMAL)
                logging.info(f"Image uploaded: {self.image_path}")

            except Exception as e:
                logging.error(f"Failed to load image: {e}")
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.predict_button.config(state=tk.DISABLED)

    # ---------------- Preprocess Image ----------------
    def preprocess_image(self, path):
        try:
            img = Image.open(path).convert("L")  # Ensure grayscale
            img = img.resize((150, 150))  # Resize to match model input
            img_array = np.array(img, dtype=np.float32)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = np.expand_dims(img_array, axis=-1)
            img_array = img_array / 255.0
            logging.info("Image preprocessed successfully")
            return img_array
        except Exception as e:
            logging.error(f"Failed to preprocess image: {e}")
            messagebox.showerror("Error", f"Failed to preprocess image: {e}")
            return None

    # ---------------- Predict ----------------
    def predict(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image uploaded")
            return

        img_array = self.preprocess_image(self.image_path)
        if img_array is None:
            return

        try:
            model = get_model()
            prediction = model.predict(img_array)
            self.result = "Pneumonia" if prediction[0][0] > 0.5 else "Normal"
            self.result_label.config(text=f"Prediction: {self.result}")

            timestamp = datetime.now()
            conn = sqlite3.connect("pneumonia_app.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tests (email, result, timestamp) VALUES (?, ?, ?)",
                (self.email, self.result, timestamp),
            )
            conn.commit()
            conn.close()
            self.report_button.config(state=tk.NORMAL)
            logging.info(f"Prediction made: {self.result}")

        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            messagebox.showerror("Error", f"Prediction failed: {e}")

    # ---------------- Generate Report ----------------
    def regenerate_report(self):
        if not self.result or not self.image_path:
            messagebox.showerror("Error", "No prediction available or no image uploaded")
            return

        try:
            # ✅ Create Reports directory if it doesn’t exist
            reports_dir = os.path.join(os.getcwd(), "Reports")
            os.makedirs(reports_dir, exist_ok=True)

            # ✅ Save report inside Reports folder
            report_filename = f"report_{self.email}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            report_path = os.path.join(reports_dir, report_filename)

            c = canvas.Canvas(report_path, pagesize=letter)
            c.drawString(100, 750, "Pneumonia Detection Report")
            c.drawString(100, 730, f"Email: {self.email}")
            c.drawString(100, 710, f"Image Path: {self.image_path}")
            c.drawString(100, 690, f"Prediction: {self.result}")
            c.drawString(100, 670, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.save()

            messagebox.showinfo("Success", f"Report saved in 'Reports' folder:\n{report_filename}")
            logging.info(f"Report generated: {report_path}")

        except Exception as e:
            logging.error(f"Failed to generate report: {e}")
            messagebox.showerror("Error", f"Failed to generate report: {e}")

    # ---------------- Log Out ----------------
    def log_out(self):
        """Return to the login page after user clicks 'Log Out'."""
        from login import LoginWindow  # Lazy import (prevents circular import)
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to log out?")
        if confirm:
            self.root.destroy()
            root = tk.Tk()
            LoginWindow(root)
            root.mainloop()
