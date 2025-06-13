import sqlite3
from tkinter import *
import customtkinter as ck
from tkinter import messagebox
from PIL import Image as PILImage, ImageTk
import os
ck.set_appearance_mode("light")
ck.set_default_color_theme("blue")

class LoginForm:
    def __init__(self, master):
        self.login = Toplevel(master)
        self.login.title("Login Form")
        self.login.geometry("800x550")
        self.login.configure(bg="#330000")

        image = PILImage.open(os.path.join("Images", "splash.jpg"))
        resized_image = image.resize((800, 550), PILImage.LANCZOS)
        photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas = Canvas(self.login, width=800, height=550)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=photo_image, anchor=NW)

        login_image = PILImage.open(os.path.join("Images", "login.png"))
        login_image_resized = login_image.resize((400, 350), PILImage.LANCZOS)
        self.login_photo = ImageTk.PhotoImage(login_image_resized)
        self.canvas.create_image(100, 200, image=self.login_photo)

        self.canvas.create_text(520, 130, text="LogIn", fill="white", font=("yu gothic ui", 20, "bold"))

        self.canvas.create_text(420, 220, text="Username", fill="white", font=("yu gothic ui", 13, "bold"))
        self.username = ck.CTkEntry(self.login, width=200, border_color="brown4", border_width=1)
        self.username.place(x=480, y=205)

        self.canvas.create_text(420, 270, text="Password", fill="white", font=("yu gothic ui", 13, "bold"))
        self.password = ck.CTkEntry(self.login, show="*", width=200, border_color="red4", border_width=1)
        self.password.place(x=480, y=255)

        login_button = ck.CTkButton(self.login, text="Login", font=("Arial", 15, "bold"),
                                    command=self.login_user, corner_radius=10, height=35, width=90,
                                    fg_color="firebrick4", hover_color="firebrick3")
        login_button.place(x=500, y=330)

        self.canvas.create_text(500, 400, text="Don't have an account?", fill="white", font=("yu gothic ui", 10, "bold"))
        register_text = self.canvas.create_text(610, 400, text="Register", fill="firebrick1", font=("yu gothic ui", 10, "bold"))
        self.canvas.tag_bind(register_text, "<Button-1>", lambda e: self.open_register_form())

        self.login.mainloop()

    def login_user(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            self.open_materials_form()
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    def open_register_form(self):
        from register_form import RegisterForm
        self.login.withdraw()
        RegisterForm(self.login)

    def open_materials_form(self):
        from upload_studentPaper import StudentMaterial
        self.login.withdraw()
        StudentMaterial(self.login)

