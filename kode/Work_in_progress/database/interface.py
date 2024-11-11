import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Fetch data for dropdown options from the database
def fetch_dropdown_data():
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    machines = [row[0] for row in cursor.execute("SELECT MachineName FROM Machines")]
    materials = [row[0] for row in cursor.execute("SELECT MaterialName FROM Materials")]
    processes = [row[0] for row in cursor.execute("SELECT ProcessName FROM Processes")]
    conn.close()
    return machines, materials, processes

# Calculate material cost based on user selection
def calculate_material_cost():
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for amount.")
        return

    machine_name, material_name = machine_var.get(), material_var.get()

    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT MachineMaterialCost.Cost, MachineMaterialCost.Unit
        FROM Machines
        JOIN MachineMaterialCost ON Machines.MachineID = MachineMaterialCost.MachineID
        JOIN Materials ON Materials.MaterialID = MachineMaterialCost.MaterialID
        WHERE Machines.MachineName = ? AND Materials.MaterialName = ?
    ''', (machine_name, material_name))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        cost, unit = result
        if unit == '$/10kg':
            amount /= 10
        total_cost = cost * amount
        messagebox.showinfo("Result", f"Total cost for {amount} units of {material_name} on {machine_name}: ${total_cost:.2f}")
    else:
        messagebox.showinfo("Result", "No matching machine or material found.")

# Initialize dropdown data
machines, materials, processes = fetch_dropdown_data()

# Set up customtkinter GUI window
ctk.set_appearance_mode("System")  # Use system theme
ctk.set_default_color_theme("blue")  # Set default color theme

root = ctk.CTk()
root.title("Material Cost Calculator")

# Dropdowns and Entry fields
fields = [("Select Machine:", machines, ctk.StringVar()), 
          ("Select Material:", materials, ctk.StringVar()), 
          ("Select Process:", processes, ctk.StringVar()), 
          ("Enter Amount:", None, None)]

variables = {}

for i, (label, options, var) in enumerate(fields):
    ctk.CTkLabel(root, text=label).grid(row=i, column=0, padx=10, pady=5)
    if options:
        variables[label] = var
        ctk.CTkComboBox(root, variable=var, values=options).grid(row=i, column=1, padx=10, pady=5)
    else:
        amount_entry = ctk.CTkEntry(root)
        amount_entry.grid(row=i, column=1, padx=10, pady=5)

machine_var, material_var = variables["Select Machine:"], variables["Select Material:"]

# Calculate button
calculate_button = ctk.CTkButton(root, text="Calculate Cost", command=calculate_material_cost)
calculate_button.grid(row=len(fields), column=0, columnspan=2, padx=10, pady=20)

root.mainloop()
