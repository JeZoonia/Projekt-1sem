import sqlite3
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt

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
        self.database = database

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

        # Fetch necessary details
        cost_per_cm3 = self.database.fetch_cost_details(queries["cost_per_cm3"], (machine_name, material_name))
        cost_per_cm3 = cost_per_cm3[0][0] if cost_per_cm3 else 0
        material_cost = cost_per_cm3 * volume_cm3

        build_rate = self.database.fetch_cost_details(queries["build_rate"], (machine_name,))
        build_rate = build_rate[0][0] if build_rate else 1  # Prevent division by zero
        build_time_hours = volume_cm3 / build_rate

        employee_pay_rate = self.database.fetch_cost_details(queries["employee_pay_rate"], (machine_name,))
        employee_pay_rate = employee_pay_rate[0][0] if employee_pay_rate else 0
        employee_pay = build_time_hours * employee_pay_rate

        fixed_costs = self.database.fetch_cost_details(queries["fixed_costs"], (machine_name,))
        setup_cost, removal_cost = fixed_costs[0] if fixed_costs else (0, 0)

        operating_cost = sum(
            row[0] for row in self.database.fetch_cost_details(queries["operating_cost"], (machine_name,))
        )
        consumable_cost = sum(
            row[0] for row in self.database.fetch_cost_details(queries["consumable_cost"], (machine_name,))
        )

        process_cost = setup_cost + removal_cost + consumable_cost + (operating_cost * build_time_hours) + employee_pay
        total_cost = material_cost + process_cost

        return total_cost, material_cost, process_cost
    


class GraphPlot:
    def plot_cost_vs_volume(machine_name, material_name, calculator, volumes):
        costs = [calculator.calculate_total_cost(machine_name, material_name, v)[0] for v in volumes]
        plt.figure(figsize=(10, 6))
        plt.plot(volumes, costs, marker='o', linestyle='-', label=f"Cost vs. Volume for {machine_name} and {material_name}")
        plt.title("Total Cost vs. Volume")
        plt.xlabel("Volume (cm³)")
        plt.ylabel("Total Cost ($)")
        plt.grid(True)
        plt.legend()
        plt.show()


class GUISetup:
    def __init__(self, root, db_name):
        self.database = Database(db_name)
        self.calculator = Calculator(self.database)
        self.root = root
        self.machine_var = ctk.StringVar()
        self.material_var = ctk.StringVar()
        self.process_var = ctk.StringVar()
        self.volume_entry = None

    def setup_gui(self):
        self.root.geometry("800x500")
        self.root.configure(fg_color="#777777")
        self.root.title("NEXTTECH CALCULATOR")

        title_label = ctk.CTkLabel(self.root, text="NEXTTECH CALCULATOR", font=("Arial", 24, "bold"), text_color="black")
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        machines = self.database.fetch_dropdown_data()
        self.machine_var.trace_add('write', self.update_dropdowns)

        ctk.CTkLabel(self.root, text="Select Machine:", font=("Arial", 14), text_color="black").grid(row=1, column=0, padx=20, pady=10, sticky="e")
        ctk.CTkComboBox(self.root, variable=self.machine_var, values=machines, width=200).grid(row=1, column=1, padx=20, pady=10)

        ctk.CTkLabel(self.root, text="Select Material:", font=("Arial", 14), text_color="black").grid(row=2, column=0, padx=20, pady=10, sticky="e")
        ctk.CTkComboBox(self.root, variable=self.material_var, values=[], width=200).grid(row=2, column=1, padx=20, pady=10)

        ctk.CTkLabel(self.root, text="Process:", font=("Arial", 14), text_color="black").grid(row=3, column=0, padx=20, pady=10, sticky="e")
        process_entry = ctk.CTkEntry(self.root, textvariable=self.process_var, state='readonly', width=200)
        process_entry.grid(row=3, column=1, padx=20, pady=10)

        ctk.CTkLabel(self.root, text="Enter Volume (cm³):", font=("Arial", 14), text_color="black").grid(row=4, column=0, padx=20, pady=10, sticky="e")
        self.volume_entry = ctk.CTkEntry(self.root, width=200, fg_color="white", text_color="black")
        self.volume_entry.grid(row=4, column=1, padx=20, pady=10)

        calculate_button = ctk.CTkButton(self.root, text="Calculate Cost", command=self.calculate_and_plot, font=("Arial", 14, "bold"),
                                         text_color="white", fg_color="#39B54A", hover_color="#2E8B3A", corner_radius=8)
        calculate_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def update_dropdowns(self, *args):
        selected_machine = self.machine_var.get()
        if selected_machine:
            compatible_materials, process_type = self.database.fetch_compatible_data(selected_machine)
            material_dropdown = ctk.CTkComboBox(self.root, variable=self.material_var, values=compatible_materials, width=200)
            material_dropdown.grid(row=2, column=1, padx=20, pady=10)
            self.process_var.set(process_type)

    def calculate_and_plot(self):
        try:
            volume_cm3 = float(self.volume_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for volume.")
            return

        machine_name = self.machine_var.get()
        material_name = self.material_var.get()

        if not machine_name or not material_name:
            messagebox.showerror("Input Error", "Please select a machine and material first.")
            return

        total_cost, material_cost, process_cost = self.calculator.calculate_total_cost(machine_name, material_name, volume_cm3)
        result_message = (
            f"Material Cost for {volume_cm3} cm³: ${material_cost:.2f}\n"
            f"Process Cost: ${process_cost:.2f}\n"
            f"Total Cost: ${total_cost:.2f}"
        )

        with open("calculation_results.txt", "a") as file:
            file.write(f"Machine: {machine_name}, Material: {material_name}\n")
            file.write(f"Volume: {volume_cm3} cm³\n")
            file.write(result_message + "\n\n")

        messagebox.showinfo("Cost Calculation Result", result_message)

        lower_bound = int(volume_cm3 * 0.5)  
        upper_bound = int(volume_cm3 * 1.5)
        volume_range = range(lower_bound, upper_bound + 1, (upper_bound - lower_bound) // 10 or 1)

        # Generate graph
        GraphPlot.plot_cost_vs_volume(machine_name, material_name, self.calculator, volume_range)



if __name__ == "__main__":
    root = ctk.CTk()
    gui = GUISetup(root, 'manufacturing.db')
    gui.setup_gui()
    root.mainloop()
