import sqlite3
from tkinter import *
import customtkinter as ck
from tkinter import messagebox
from PIL import Image as PILImage, ImageTk
import os
ck.set_appearance_mode("light")
ck.set_default_color_theme("blue")

class RegisterForm:
    def __init__(self, master):
        self.register = Toplevel(master)
        self.register.title("Register Form")
        self.register.geometry("800x550")
        self.register.configure(bg="#330000")

        image = PILImage.open(os.path.join("Images", "splash.jpg"))
        resized_image = image.resize((800, 550), PILImage.LANCZOS)
        photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas = Canvas(self.register, width=800, height=550)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=photo_image, anchor=NW)

        login_image = PILImage.open(os.path.join("Images", "login.png"))
        login_image_resized = login_image.resize((400, 350), PILImage.LANCZOS)
        self.login_photo = ImageTk.PhotoImage(login_image_resized)
        self.canvas.create_image(100, 200, image=self.login_photo)

        self.canvas.create_text(520, 130, text="Register", fill="white", font=("yu gothic ui", 20, "bold"))

        self.canvas.create_text(420, 220, text="Full Name", fill="white", font=("yu gothic ui", 13, "bold"))
        self.name = ck.CTkEntry(self.register, width=200, border_color="brown4", border_width=1)
        self.name.place(x=480, y=205)

        self.canvas.create_text(420, 270, text="Username", fill="white", font=("yu gothic ui", 13, "bold"))
        self.username = ck.CTkEntry(self.register, width=200, border_color="brown4", border_width=1)
        self.username.place(x=480, y=255)

        self.canvas.create_text(420, 320, text="Password", fill="white", font=("yu gothic ui", 13, "bold"))
        self.password = ck.CTkEntry(self.register, show="*", width=200, border_color="red4", border_width=1)
        self.password.place(x=480, y=305)

        register_button = ck.CTkButton(self.register, text="Register", font=("Arial", 15, "bold"),
                                       command=self.register_user, corner_radius=10, height=35, width=90,
                                       fg_color="firebrick4", hover_color="firebrick3")
        register_button.place(x=500, y=370)

        self.canvas.create_text(500, 430, text="Already have an account?", fill="white", font=("yu gothic ui", 10, "bold"))
        register_text = self.canvas.create_text(610, 430, text="login", fill="firebrick1", font=("yu gothic ui", 10, "bold"))
        self.canvas.tag_bind(register_text, "<Button-1>", lambda e: self.open_login_form())

        self.init_db()
        self.register.mainloop()

    def init_db(self):
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        full_name TEXT NOT NULL,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )""")
        conn.commit()
        conn.close()

    def register_user(self):
        full_name = self.name.get().strip()
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not full_name or not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        if len(username) < 4 or username[0].isdigit():
            messagebox.showerror("Error", "Username must be at least 4 characters and not start with a digit.")
            return

        if len(password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return

        try:
            conn = sqlite3.connect("user_data.db")
            c = conn.cursor()
            c.execute("INSERT INTO users (full_name, username, password) VALUES (?, ?, ?)",
                      (full_name, username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.open_login_form()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        finally:
            conn.close()

    def open_login_form(self):
        from Login_form import LoginForm
        self.register.withdraw()
        LoginForm(self.register)
