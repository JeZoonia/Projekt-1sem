from tkinter import *
import customtkinter as c
import sqlite3
from PIL import Image
from tkinter import messagebox 

class App(c.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nexttech Calculator")
        self.geometry("800x600")
        c.set_appearance_mode("dark")
        c.set_default_color_theme("blue")
        Login_menu(self).pack(expand=True, fill = "both")



class Login_menu(c.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.overskrift = c.CTkLabel(self, text="Nexttech Calculator", font=("Arial", 24))
        self.overskrift.pack(pady=10)

        self.menuframe = c.CTkFrame(self, corner_radius=10)  
        self.menuframe.pack(pady=100, padx=20)

        brugernavn_label = c.CTkLabel(self.menuframe, text="Brugernavn")
        brugernavn_label.grid(row=0, column=0, padx=10, pady=10)
        self.brugernavn_entry = c.CTkEntry(self.menuframe)
        self.brugernavn_entry.grid(row=0, column=1, padx=10, pady=10)

        adgangskode_label = c.CTkLabel(self.menuframe, text="adgangskode")
        adgangskode_label.grid(row=1, column=0, padx=10, pady=10)
        self.adgangskode_entry = c.CTkEntry(self.menuframe, show = '*')
        self.adgangskode_entry.grid(row=1, column=1, padx=10, pady=10)

        login_knap = c.CTkButton(self.menuframe, text="Login", command=self.log)
        login_knap.grid(row=2, column=0, columnspan=2, pady=20)

        logo = c.CTkImage(light_image=Image.open(r"C:\Users\caspe\Desktop\Projekt1\Login\Nexttech.png"), size=(200,200))
        logo_label = c.CTkLabel(self, text="", image=logo)
        logo_label.pack(pady=10, anchor="n", side="bottom")
        
        
    def log(self):
        brugernavn = self.brugernavn_entry.get()
        adgangskode = self.adgangskode_entry.get()
        connection = sqlite3.connect("adgang.db")
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bruger WHERE brugernavn = ? AND adgangskode = ?", (brugernavn, adgangskode))
            results = cursor.fetchone()
            if results:
                print("Login successful!")
                for widget in self.master.winfo_children():
                    widget.destroy()
                MainMenu(self.master).pack(expand=True, fill="both")
            else:
                messagebox.showinfo("Fejl", "Fejl i brugernavn eller adgangskode")
                self.brugernavn_entry.delete(0,END)
                self.adgangskode_entry.delete(0,END)
        finally:
            connection.close()


class MainMenu(c.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        c.CTkLabel(self, text="Velkommen til hovedmenuen!").pack(pady=50)


app = App()
app.mainloop()