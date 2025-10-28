import tkinter as tk
from login import LoginWindow
from database import init_db

if __name__ == "__main__":
    init_db()  # Initialize the database
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
