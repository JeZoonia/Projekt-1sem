from tkinter import *
import customtkinter as c
import sqlite3
from PIL import Image, ImageTk
from tkinter import messagebox 




def log(parent, brugernavn_entry, adgangskode_entry):
    brugernavn = brugernavn_entry.get()
    adgangskode = adgangskode_entry.get()
    connection = sqlite3.connect("adgang.db")
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bruger WHERE brugernavn = ? AND adgangskode = ?", (brugernavn, adgangskode))
        results = cursor.fetchone()
        if results:
            print("Login successful!")
            user_id_type = results [2]
            for widget in parent.winfo_children():
                widget.destroy()
            MainMenu(parent, user_id_type).pack(expand=True, fill="both")
        else:
            messagebox.showinfo("Fejl", "Fejl i brugernavn eller adgangskode")
            brugernavn_entry.delete(0, END)
            adgangskode_entry.delete(0, END)
    finally:
        connection.close()


def admin_frem(parent, user_id_type):
    for widget in parent.winfo_children():
        widget.pack_forget()
    AdminMenu(parent, user_id_type).pack(expand=True, fill="both")


def admin_tilbage(parent, user_id_type):
    for widget in parent.winfo_children():
        widget.pack_forget()
    MainMenu(parent, user_id_type).pack(expand=True, fill="both")



def opret_bruger(parent, adminbrugernavn_entry, adminadgangskode_entry, choice):
    adminbrugernavn = adminbrugernavn_entry.get()
    adminadgangskode = adminadgangskode_entry.get()
    adminvalg = choice.get()

    type_id = 1 if adminvalg == "Admin" else 2

    connection = sqlite3.connect("adgang.db")
    try:
        cursor = connection.cursor()
        
        cursor.execute("SELECT * FROM bruger WHERE brugernavn = ?", (adminbrugernavn,))
        if cursor.fetchone():
            messagebox.showerror("Fejl", "Brugernavnet eksisterer allerede")
            return
        
        cursor.execute("INSERT INTO bruger (brugernavn, adgangskode, type_id) VALUES (?, ?, ?)", (adminbrugernavn, adminadgangskode, type_id))
        connection.commit()
        messagebox.showinfo("Succes", "Bruger oprettet")
        adminbrugernavn_entry.delete(0, END)
        adminadgangskode_entry.delete(0, END)
        choice.set('Bruger rettigheder')
    except Exception as e:
        messagebox.showerror("Fejl", f"Kunne ikke oprette bruger: {e}")
    finally:
        connection.close()




class App(c.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nexttech Calculator")
        self.geometry("800x600")
        c.set_appearance_mode("dark")
        c.set_default_color_theme("blue")
        Login_menu(self).pack(expand=True, fill="both")




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

        adgangskode_label = c.CTkLabel(self.menuframe, text="Adgangskode")
        adgangskode_label.grid(row=1, column=0, padx=10, pady=10)
        self.adgangskode_entry = c.CTkEntry(self.menuframe, show='*')
        self.adgangskode_entry.grid(row=1, column=1, padx=10, pady=10)

        login_knap = c.CTkButton(self.menuframe,text="Login",command=lambda: log(parent, self.brugernavn_entry, self.adgangskode_entry),hover_color="green")
        login_knap.grid(row=2, column=0, columnspan=2, pady=20)

        logo = c.CTkImage(Image.open('Nexttech.png'), size=(200, 200))
        logo_label = c.CTkLabel(self, text="", image=logo)
        logo_label.pack(pady=10, anchor="n", side="bottom")






class MainMenu(c.CTkFrame):
    def __init__(self, parent, user_id_type):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)

        # Historik
        historik_knap = c.CTkButton(
            self, text="Historik", width=150, height=150, border_width=5, border_color="black", anchor="center", fg_color="grey", hover_color="lightgrey")
        historik_knap.grid(row=1, column=0)

        # Beregner
        beregner_knap = c.CTkButton(
            self, text="Beregner", width=150, height=150, border_width=5, border_color="black", anchor="center", fg_color="grey", hover_color="lightgrey")
        beregner_knap.grid(row=1, column=2)

        if user_id_type == 1:
            admin_knap = c.CTkButton(self, text="Admin", width=150, height=150, border_width=5, border_color="black", anchor="center", fg_color="grey", hover_color="lightgrey", command=lambda: admin_frem(parent, user_id_type))
            admin_knap.grid(row=1, column=1)


class AdminMenu(c.CTkFrame):
    def __init__(self, parent, user_id_type):
        super().__init__(parent)
        self.opretframe = c.CTkFrame(self)  
        self.opretframe.grid(row=0, column=0)

        tilbage_logo = c.CTkImage(Image.open('Back-arrow.png'), size=(20,20))
        tilbage_knap = c.CTkButton(self.opretframe, text="" ,image= tilbage_logo, width=20, height= 20, fg_color= "transparent",compound= "left", command= lambda: admin_tilbage(parent, user_id_type))
        tilbage_knap.grid(row = 0, column = 0)

        overskrift = c.CTkLabel(self.opretframe, text="Opret bruger", font=("Arial", 24))
        overskrift.grid(row=1, column=0, columnspan = 2, pady= 20)

        adminbrugernavn_label = c.CTkLabel(self.opretframe, text="Brugernavn", font=("Arial", 16))
        adminbrugernavn_label.grid(row=2, column=0, pady= 20)

        adminbrugernavn_entry = c.CTkEntry(self.opretframe)
        adminbrugernavn_entry.grid(row=2, column=1, pady= 20)

        adminadgangskode_label = c.CTkLabel(self.opretframe, text="Adgangskode", font=("Arial", 16))
        adminadgangskode_label.grid(row=3, column=0, pady= 20)

        adminadgangskode_entry = c.CTkEntry(self.opretframe)
        adminadgangskode_entry.grid(row=3, column=1, pady= 20)

        rettigheder_label = c.CTkLabel(self.opretframe, text="Rettigheder",font=("Arial", 16) )
        rettigheder_label.grid(row=4, column=0, pady= 20)

        choice = StringVar(self)
        choice.set('Bruger rettigheder') 
        valg = c.CTkOptionMenu(self.opretframe, variable=choice, values=['Admin', 'Normal bruger'])
        valg.grid(row=4, column=1)


        opret_knap = c.CTkButton(self.opretframe, text= "opret", command=lambda: opret_bruger(parent, adminbrugernavn_entry, adminadgangskode_entry, choice))
        opret_knap.grid(row = 5, column = 0, columnspan= 2)

















if __name__ == "__main__":
    app = App()
    app.mainloop()
