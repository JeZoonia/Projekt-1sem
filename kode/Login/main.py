from tkinter import *
import customtkinter as c
import sqlite3

connection = sqlite3.connect("ntb.db")
cursor = connection.cursor()

def menu2():
    app.destroy()
    screen2 = Tk()
    screen2.title("menu")
    Label(screen2, text="det virker").pack()
    screen2.mainloop()
    

def log():
    global brugernavn_entry, adgangskode_entry, login_knap, login_frame, app, login
    cursor.execute("SELECT * FROM bruger")
    results = cursor.fetchall()

    for result in results:
        if brugernavn_entry.get() == result[0] and adgangskode_entry.get() == result[1]:
            menu2()
        else:
            Label(app, text="fejl i brugernavn eller adgangskode").pack()


def login_menu():
    global brugernavn_entry, adgangskode_entry, login_frame, login_knap, app, login
    app = Tk()
    app.title("nexttech calculator")
    app.geometry('340x440')
    app.configure(bg='#999999')

 
    Label(app, text="Nexttech Calculator", bg='#999999',pady= 20, ).pack()

    login_frame = Frame(app, height=220, width= 200, padx=20, pady= 20, bg='#b8b8b8', highlightthickness=2, highlightbackground="black")
    login_frame.pack()

    brugernavn_label = Label(login_frame, text="Brugernavn", bg= '#b8b8b8')
    brugernavn_label.grid(row=1, column=0)
    brugernavn_entry = Entry(login_frame)
    brugernavn_entry.grid(row=1, column=1)


    adgangskode_label = Label(login_frame, text="Adgangskode", bg='#b8b8b8')
    adgangskode_label.grid(row=2, column=0)
    adgangskode_entry = Entry(login_frame)
    adgangskode_entry.grid(row=2, column=1)

    login_knap = Button(login_frame, text="Login", relief='raised', command= log)
    login_knap.grid(row=3, columnspan=2)

    logo = PhotoImage(file='Nexttech.png')
    logo_label = Label(app, image=logo, background= '#999999')
    logo_label.pack()

    app.mainloop()

login_menu()