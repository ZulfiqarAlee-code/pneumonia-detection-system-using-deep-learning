import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import logging
from database import hash_password

# ---------------- Logging Setup ----------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ---------------- Sign Up ----------------
class SignUpWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Up")

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
        ).pack(pady=5)

        # Background canvas
        self.canvas = tk.Canvas(
            root, width=screen_width, height=screen_height, bg="#4B0082", highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(
            screen_width * 0.6, 0, screen_width, screen_height, fill="#6A0DAD", outline=""
        )

        # Load side image
        self.image_path = "Images/x ray images.jpg"
        try:
            img = Image.open(self.image_path)
            img = img.resize((int(screen_width * 0.4), screen_height), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            self.canvas.create_image(
                screen_width * 0.8, screen_height // 2, image=self.photo, anchor="center"
            )
        except Exception as e:
            logging.error(f"Error loading image: {e}")

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
            text="SIGN UP",
            font=("Arial", 24, "bold"),
            fg="#4B0082",
            bg="white",
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Email
        tk.Label(self.form_frame, text="Email Address:", font=("Arial", 12), fg="#4B0082", bg="white").grid(
            row=2, column=0, pady=5, sticky="e"
        )
        self.email_entry = tk.Entry(self.form_frame, width=25, bg="#F0F0F0")
        self.email_entry.grid(row=2, column=1, pady=5)

        # Password
        tk.Label(self.form_frame, text="Password:", font=("Arial", 12), fg="#4B0082", bg="white").grid(
            row=3, column=0, pady=5, sticky="e"
        )
        self.password_entry = tk.Entry(self.form_frame, show="*", width=25, bg="#F0F0F0")
        self.password_entry.grid(row=3, column=1, pady=5)

        # Confirm Password
        tk.Label(self.form_frame, text="Confirm Password:", font=("Arial", 12), fg="#4B0082", bg="white").grid(
            row=4, column=0, pady=5, sticky="e"
        )
        self.confirm_entry = tk.Entry(self.form_frame, show="*", width=25, bg="#F0F0F0")
        self.confirm_entry.grid(row=4, column=1, pady=5)

        # Buttons
        tk.Button(
            self.form_frame,
            text="Sign Up",
            command=self.sign_up,
            bg="#4B0082",
            fg="white",
            font=("Arial", 12),
            width=20,
        ).grid(row=5, column=0, columnspan=2, pady=15)

        tk.Button(
            self.form_frame,
            text="or Log in",
            command=self.go_to_login,
            fg="#4B0082",
            bg="white",
            font=("Arial", 10),
            bd=0,
            activebackground="white",
            activeforeground="#4B0082",
        ).grid(row=6, column=0, columnspan=2, pady=5)

    def sign_up(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm = self.confirm_entry.get()

        if not email or not password or not confirm:
            messagebox.showerror("Error", "All fields are required")
            return
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return

        conn = sqlite3.connect("pneumonia_app.db")
        cursor = conn.cursor()
        try:
            hashed = hash_password(password)
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed))
            conn.commit()
            messagebox.showinfo("Success", "Sign up successful! Please login.")
            self.go_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists")
        finally:
            conn.close()

    def go_to_login(self):
        from login import LoginWindow  # moved here to break circular import
        self.root.destroy()
        root = tk.Tk()
        LoginWindow(root)
        root.mainloop()
