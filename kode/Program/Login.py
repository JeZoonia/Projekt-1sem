from tkinter import *
import customtkinter as c
import sqlite3
from PIL import Image, ImageTk
from tkinter import messagebox 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def log(parent, brugernavn_entry, adgangskode_entry, db_name):
    brugernavn = brugernavn_entry.get()
    adgangskode = adgangskode_entry.get()
    connection = sqlite3.connect(db_name)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bruger WHERE brugernavn = ? AND adgangskode = ?", (brugernavn, adgangskode))
        results = cursor.fetchone()
        if results:
            print("Login successful!")
            for widget in parent.winfo_children():
                widget.destroy()
            MainMenu(parent, db_name).pack(expand=True, fill="both")
        else:
            messagebox.showinfo("Fejl", "Fejl i brugernavn eller adgangskode")
            brugernavn_entry.delete(0, END)
            adgangskode_entry.delete(0, END)
    finally:
        connection.close()


def admin_frem(parent, db_name):
    for widget in parent.winfo_children():
        widget.pack_forget()
    AdminMenu(parent, db_name).pack(expand=True, fill="both")


def tilbage(parent, db_name):
    for widget in parent.winfo_children():
        widget.pack_forget()
    MainMenu(parent, db_name).pack(expand=True, fill="both")


def berenger_frem(parent, db_name):
    for widget in parent.winfo_children():
        widget.destroy()  
    GUISetup(parent, db_name).pack(expand=True, fill="both")




def opret_bruger(parent, adminbrugernavn_entry, adminadgangskode_entry, choice, db_name):
    adminbrugernavn = adminbrugernavn_entry.get()
    adminadgangskode = adminadgangskode_entry.get()
    adminvalg = choice.get()

    type_id = 1 if adminvalg == "Admin" else 2

    connection = sqlite3.connect(db_name)
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
    def __init__(self, db_name):
        super().__init__()
        self.title("Nexttech Calculator")
        self.geometry("1200x800")
        c.set_appearance_mode("dark")
        c.set_default_color_theme("blue")
        Login_menu(self, db_name).pack(expand=True, fill="both")




class Login_menu(c.CTkFrame):
    def __init__(self, parent, db_name):
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

        login_knap = c.CTkButton(self.menuframe,text="Login",command=lambda: log(parent, self.brugernavn_entry, self.adgangskode_entry, db_name),hover_color="green")
        login_knap.grid(row=2, column=0, columnspan=2, pady=20)

        logo = c.CTkImage(Image.open('Nexttech.png'), size=(200, 200))
        logo_label = c.CTkLabel(self, text="", image=logo)
        logo_label.pack(pady=10, anchor="n", side="bottom")


class MainMenu(c.CTkFrame):
    def __init__(self, parent, db_name):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)

        # Historik
        historik_knap = c.CTkButton(
            self, text="Historik", width=150, height=150, border_width=5, border_color="black", anchor="center", hover_color="green")
        historik_knap.grid(row=1, column=0)

        # Beregner
        beregner_knap = c.CTkButton(self, text="Beregner", width=150, height=150, border_width=5, border_color="black", anchor="center",  hover_color="green", command=lambda: berenger_frem(parent, db_name))
        beregner_knap.grid(row=1, column=2)

        admin_knap = c.CTkButton(self, text="Admin", width=150, height=150, border_width=5, border_color="black", anchor="center",  hover_color="green", command=lambda: admin_frem(parent, db_name))
        admin_knap.grid(row=1, column=1)


class AdminMenu(c.CTkFrame):
    def __init__(self, parent, db_name):
        super().__init__(parent)


        self.opretframe = c.CTkFrame(self)  
        self.opretframe.pack(fill = "both", expand = "true")

        tilbage_logo = c.CTkImage(Image.open('Back-arrow.png'), size=(20,20))
        tilbage_knap = c.CTkButton(self.opretframe, text="" ,image= tilbage_logo, width=20, height= 20, fg_color= "transparent", command= lambda: tilbage(parent, db_name), hover_color="green")
        tilbage_knap.grid(row = 0, column = 0, sticky= "w")

        overskrift_opret = c.CTkLabel(self.opretframe, text="Opret bruger", font=("Arial", 24))
        overskrift_opret.grid(row=1, column=0, columnspan = 2, pady= 20, padx= 20)

        adminbrugernavn_label = c.CTkLabel(self.opretframe, text="Brugernavn", font=("Arial", 16))
        adminbrugernavn_label.grid(row=2, column=0, pady= 20)

        adminbrugernavn_entry = c.CTkEntry(self.opretframe)
        adminbrugernavn_entry.grid(row=2, column=1, pady=20, padx= 20)

        adminadgangskode_label = c.CTkLabel(self.opretframe, text="Adgangskode", font=("Arial", 16))
        adminadgangskode_label.grid(row=3, column=0, pady= 20)

        adminadgangskode_entry = c.CTkEntry(self.opretframe)
        adminadgangskode_entry.grid(row=3, column=1, pady= 20, padx= 20)

        rettigheder_label = c.CTkLabel(self.opretframe, text="Rettigheder",font=("Arial", 16) )
        rettigheder_label.grid(row=4, column=0, pady= 20)

        choice = StringVar(self)
        choice.set('Vælg') 
        valg = c.CTkOptionMenu(self.opretframe, variable=choice, values=['Admin', 'Normal bruger'])
        valg.grid(row=4, column=1, padx= 20)

        opret_knap = c.CTkButton(self.opretframe, text= "Opret", command=lambda: opret_bruger(parent, adminbrugernavn_entry, adminadgangskode_entry, choice))
        opret_knap.grid(row = 5, column = 0, columnspan= 2)

 
class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def fetch_dropdown_data(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        machines = [row[0] for row in cursor.execute("SELECT MachineName FROM Machine")]
        conn.close()
        return machines

    def fetch_compatible_data(self, machine_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        materials = [row[0] for row in cursor.execute('''
            SELECT Materials.MaterialName 
            FROM MaterialCostPerCM3
            JOIN Machine ON Machine.MachineID = MaterialCostPerCM3.MachineID
            JOIN Materials ON Materials.MaterialID = MaterialCostPerCM3.MaterialID
            WHERE Machine.MachineName = ?
        ''', (machine_name,))]
        process_type = cursor.execute('''
            SELECT ProcessType
            FROM Machine
            WHERE MachineName = ?
        ''', (machine_name,)).fetchone()
        conn.close()
        return materials, process_type[0] if process_type else None

    def fetch_cost_details(self, query, params):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result


class Calculator:
    def __init__(self, database):
        self.database =  database

    def calculate_total_cost(self, machine_name, material_name, volume_cm3):
        queries = {
            "cost_per_cm3": '''
                SELECT MaterialCostPerCM3.CostPerCM3
                FROM Machine
                JOIN MaterialCostPerCM3 ON Machine.MachineID = MaterialCostPerCM3.MachineID
                JOIN Materials ON Materials.MaterialID = MaterialCostPerCM3.MaterialID
                WHERE Machine.MachineName = ? AND Materials.MaterialName = ?
            ''',
            "build_rate": '''
                SELECT BuildRate
                FROM BuildRate
                JOIN Machine ON Machine.MachineID = BuildRate.MachineID
                WHERE Machine.MachineName = ?
            ''',
            "employee_pay_rate": '''
                SELECT PayPerMachineSupervised
                FROM EmployeePay
                JOIN Machine ON Machine.MachineID = EmployeePay.MachineID
                WHERE Machine.MachineName = ?
            ''',
            "fixed_costs": '''
                SELECT SetupCost, RemovalCost
                FROM FixedCosts
                JOIN Machine ON Machine.MachineID = FixedCosts.MachineID
                WHERE Machine.MachineName = ?
            ''',
            "operating_cost": '''
                SELECT CostAmount
                FROM MachineCost
                JOIN CostType ON MachineCost.CostTypeID = CostType.CostTypeID
                JOIN Machine ON Machine.MachineID = MachineCost.MachineID
                WHERE Machine.MachineName = ? AND CostType.Unit = '$/hr'
            ''',
            "consumable_cost": '''
                SELECT CostAmount
                FROM MachineCost
                JOIN CostType ON MachineCost.CostTypeID = CostType.CostTypeID
                JOIN Machine ON Machine.MachineID = MachineCost.MachineID
                WHERE Machine.MachineName = ? AND CostType.Unit = '$'
            '''
        }

        cost_per_cm3 = self.database.fetch_cost_details(queries["cost_per_cm3"], (machine_name, material_name))
        cost_per_cm3 = cost_per_cm3[0][0] if cost_per_cm3 else 0
        material_cost = cost_per_cm3 * volume_cm3

        build_rate = self.database.fetch_cost_details(queries["build_rate"], (machine_name,))
        build_rate = build_rate[0][0] if build_rate else 1
        build_time_hours = volume_cm3 / build_rate

        employee_pay_rate = self.database.fetch_cost_details(queries["employee_pay_rate"], (machine_name,))
        employee_pay_rate = employee_pay_rate[0][0] if employee_pay_rate else 0
        employee_pay = build_time_hours * employee_pay_rate

        fixed_costs = self.database.fetch_cost_details(queries["fixed_costs"], (machine_name,))
        setup_cost, removal_cost = fixed_costs[0] if fixed_costs else (0, 0)

        operating_cost = sum(row[0] for row in self.database.fetch_cost_details(queries["operating_cost"], (machine_name,)))
        consumable_cost = sum(row[0] for row in self.database.fetch_cost_details(queries["consumable_cost"], (machine_name,)))

        process_cost = setup_cost + removal_cost + consumable_cost + (operating_cost * build_time_hours) + employee_pay
        total_cost = material_cost + process_cost

        return total_cost, material_cost, process_cost


class GUISetup(c.CTkFrame):
    def __init__(self, parent, db_name):
        super().__init__(parent)
        self.database = Database(db_name)
        self.calculator = Calculator(self.database)

        tilbage_logo = c.CTkImage(Image.open('Back-arrow.png'), size=(20,20))
        tilbage_knap = c.CTkButton(self, text="" ,image= tilbage_logo, width=20, height= 20, fg_color= "transparent", command= lambda: tilbage(parent, db_name), hover_color="green")
        tilbage_knap.grid(row = 0, column = 0, sticky= "w")

        self.machine_var = c.StringVar()
        self.material_var = c.StringVar()
        self.process_var = c.StringVar()

        self.input_frame = c.CTkFrame(self, width=400, height=500, corner_radius=10, fg_color="#777777")
        self.input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ne")
        self.input_frame.grid_propagate(False)

        self.label_machine = c.CTkLabel(self.input_frame, text="Select Machine:", font=("Arial", 14))
        self.label_machine.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.dropdown_machine = c.CTkOptionMenu(
            self.input_frame,
            variable=self.machine_var,
            values=[], fg_color="#444444", button_color="#555555",
            command=self.update_material_and_process_dropdowns
        )
        self.dropdown_machine.grid(row=0, column=1, padx=10, pady=10)

        self.label_material = c.CTkLabel(self.input_frame, text="Select Material:", font=("Arial", 14))
        self.label_material.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.dropdown_material = c.CTkOptionMenu(self.input_frame, variable=self.material_var, values=[], fg_color="#444444", button_color="#555555")
        self.dropdown_material.grid(row=1, column=1, padx=10, pady=10)

        self.label_process = c.CTkLabel(self.input_frame, text="Process Type:", font=("Arial", 14))
        self.label_process.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.dropdown_process = c.CTkOptionMenu(self.input_frame, variable=self.process_var, values=[],fg_color="#444444", button_color="#555555")
        self.dropdown_process.grid(row=2, column=1, padx=10, pady=10)

        self.label_volume = c.CTkLabel(self.input_frame, text="Volume (cm³):", font=("Arial", 14))
        self.label_volume.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_volume = c.CTkEntry(self.input_frame, fg_color="white", text_color="black")
        self.entry_volume.grid(row=4, column=1, padx=10, pady=10)

        self.label_prints = c.CTkLabel(self.input_frame, text="Number of Prints:", font=("Arial", 14))
        self.label_prints.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.entry_prints = c.CTkEntry(self.input_frame , fg_color="white", text_color="black")
        self.entry_prints.grid(row=6, column=1, padx=10, pady=10)

        self.button_calculate = c.CTkButton(
            self.input_frame, text="Calculate & Plot", hover_color="green", command=self.calculate_and_plot
        )
        self.button_calculate.grid(row=10, column=1, padx=10, pady=20)

        self.plot_frame = c.CTkFrame(self, width=600, height=400, corner_radius=10)
        self.plot_frame.grid(row=1, column=1, padx=20, pady=20, sticky="n")
        self.plot_frame.grid_propagate(False)

        self.price_frame = c.CTkFrame(self, width=600, height=200, corner_radius=10, fg_color="#777777")
        self.price_frame.grid(row=2, column=1, padx=20, pady=20, sticky="n")
        self.price_frame.grid_propagate(False)

        self.label_material_cost = c.CTkLabel(self.price_frame, text="Material Cost per Print: - USD", font=("Arial", 16, "bold"), text_color="black")
        self.label_material_cost.pack(pady=5)
        self.label_process_cost = c.CTkLabel(self.price_frame, text="Process Cost per Print: - USD", font=("Arial", 16, "bold"), text_color="black")
        self.label_process_cost.pack(pady=5)
        self.label_cost_per_unit = c.CTkLabel(self.price_frame, text="Cost per Print: - USD", font=("Arial", 16, "bold"), text_color="black")
        self.label_cost_per_unit.pack(pady=5)
        self.label_total_cost = c.CTkLabel(self.price_frame, text="Total Cost: - USD", font=("Arial", 16, "bold"), text_color="black")
        self.label_total_cost.pack(pady=5)

        self.populate_machine_dropdown()

    def populate_machine_dropdown(self):
        machines = self.database.fetch_dropdown_data()
        self.dropdown_machine.configure(values=machines)
        if machines:
            self.machine_var.set(machines[0])
            self.update_material_and_process_dropdowns(machines[0])

    def update_material_and_process_dropdowns(self, machine_name):
        materials, process_type = self.database.fetch_compatible_data(machine_name)
        self.dropdown_material.configure(values=materials)
        if materials:
            self.material_var.set(materials[0])

        self.dropdown_process.configure(values=[process_type] if process_type else [])
        if process_type:
            self.process_var.set(process_type)

    def calculate_and_plot(self):
        try:
            volume_cm3 = float(self.entry_volume.get())
            num_prints = int(self.entry_prints.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for volume and number of prints.")
            return

        machine_name = self.machine_var.get()
        material_name = self.material_var.get()

        if not machine_name or not material_name:
            messagebox.showerror("Input Error", "Please select a machine and material.")
            return

        total_cost, material_cost, process_cost = self.calculator.calculate_total_cost(machine_name, material_name, volume_cm3)

        cost_per_print = total_cost / num_prints
        total_cost *= num_prints
        material_cost_per_print = material_cost / num_prints
        process_cost_per_print = process_cost / num_prints

        self.label_material_cost.configure(text=f"Material Cost per Print: {material_cost_per_print:.2f} USD")
        self.label_process_cost.configure(text=f"Process Cost per Print: {process_cost_per_print:.2f} USD")
        self.label_cost_per_unit.configure(text=f"Cost per Print: {cost_per_print:.2f} USD")
        self.label_total_cost.configure(text=f"Total Cost: {total_cost:.2f} USD")

        x = list(range(1, int(num_prints) + 1))
        y = [cost_per_print * i for i in x]

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(x, y, marker='o', linestyle='-', label="Cost Curve")
        ax.set_title("Total Cost vs. Number of Prints")
        ax.set_xlabel("Number of Prints")
        ax.set_ylabel("Total Cost (USD)")
        ax.legend()
        ax.grid()

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)
        canvas.draw()


if __name__ == "__main__":
    app = App("manufacturing.db")
    app.mainloop()
