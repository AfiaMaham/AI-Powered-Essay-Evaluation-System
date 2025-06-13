from tkinter import *
from tkinter import font
from PIL import ImageTk, Image 
from Login_form import LoginForm
import time
import os

class Splash:
    def __init__(self):
        self.welcome = Tk()
        self.welcome.title("Welcome Screen")

        width_of_window = 427
        height_of_window = 250
        self.welcome.configure(bg="#330000") 

        screen_width = self.welcome.winfo_screenwidth()
        screen_height = self.welcome.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        self.welcome.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
        
        self.welcome.overrideredirect(1) 

        Frame(self.welcome, width=427, height=250, bg='#330000').place(x=0,y=0)
        label1=Label(self.welcome, text='Essay Evaluator', fg='white', bg='#330000') 
        label1.configure(font=("Game Of Squids", 24, "bold"))  
        label1.place(x=90,y=90)

        label2=Label(self.welcome, text='Loading...', fg='white', bg='#330000') 
        label2.configure(font=("Calibri", 11))
        label2.place(x=10,y=215)

        #making animation

        image_a = ImageTk.PhotoImage(Image.open(os.path.join("Images", "c1.png")))

        image_b=ImageTk.PhotoImage(Image.open(os.path.join("Images", "c2.png")))
        image_splash=ImageTk.PhotoImage(Image.open(os.path.join("Images", "logo.png")))
        original_image = Image.open(os.path.join("Images", "logo.png"))

        # Resize it to your desired size (e.g., 100x100 pixels)
        resized_image = original_image.resize((60, 60), Image.LANCZOS)

        # Convert it to a PhotoImage
        image_splash = ImageTk.PhotoImage(resized_image)
        l=Label(self.welcome, image=image_splash, bg= "#330000", border=0, relief=SUNKEN).place(x=170, y=25)


        for i in range(1): 
            l1=Label(self.welcome, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            self.welcome.update_idletasks()
            time.sleep(0.5)

            l1=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.welcome, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            self.welcome.update_idletasks()
            time.sleep(0.5)

            l1=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.welcome, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
            self.welcome.update_idletasks()
            time.sleep(0.5)

            l1=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
            l2=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
            l3=Label(self.welcome, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
            l4=Label(self.welcome, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
            self.welcome.update_idletasks()
            time.sleep(0.5)


        self.welcome.withdraw()    
        LoginForm(self.welcome)

Splash()



        