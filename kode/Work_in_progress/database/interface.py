import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Fetch machine names for the dropdown
def fetch_dropdown_data():
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    machines = [row[0] for row in cursor.execute("SELECT MachineName FROM Machines")]
    conn.close()
    return machines

# Fetch compatible materials and process for the selected machine
def fetch_compatible_data(machine_name):
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    
    # Fetch materials compatible with the selected machine
    materials = [row[0] for row in cursor.execute('''
        SELECT Materials.MaterialName 
        FROM MaterialCostPerCM3
        JOIN Machines ON Machines.MachineID = MaterialCostPerCM3.MachineID
        JOIN Materials ON Materials.MaterialID = MaterialCostPerCM3.MaterialID
        WHERE Machines.MachineName = ?
    ''', (machine_name,))]
    
    # Fetch the process compatible with the selected machine
    process = cursor.execute('''
        SELECT Processes.ProcessName
        FROM Machines
        JOIN Processes ON Machines.ProcessID = Processes.ProcessID
        WHERE Machines.MachineName = ?
    ''', (machine_name,)).fetchone()
    
    conn.close()
    return materials, process[0] if process else None

# Update materials and process dropdowns based on selected machine
def update_dropdowns(*args):
    selected_machine = machine_var.get()
    if selected_machine:
        compatible_materials, compatible_process = fetch_compatible_data(selected_machine)
        material_dropdown.configure(values=compatible_materials)
        material_var.set('')  # Clear previous material selection
        process_var.set(compatible_process)  # Set the process directly since it's one-to-one

# Calculate material cost based on volume in cm³
def calculate_material_cost():
    try:
        volume_cm3 = float(volume_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for volume.")
        return

    machine_name, material_name = machine_var.get(), material_var.get()

    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT MaterialCostPerCM3.CostPerCM3
        FROM Machines
        JOIN MaterialCostPerCM3 ON Machines.MachineID = MaterialCostPerCM3.MachineID
        JOIN Materials ON Materials.MaterialID = MaterialCostPerCM3.MaterialID
        WHERE Machines.MachineName = ? AND Materials.MaterialName = ?
    ''', (machine_name, material_name))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        cost_per_cm3 = result[0]
        total_cost = cost_per_cm3 * volume_cm3
        messagebox.showinfo("Result", f"Material cost for {volume_cm3} cm³ of {material_name} on {machine_name}: ${total_cost:.2f}")
    else:
        messagebox.showinfo("Result", "No matching machine or material found.")

# Initialize dropdown data
machines = fetch_dropdown_data()

# Set up customtkinter GUI window
ctk.set_appearance_mode("System")  # Use system theme
ctk.set_default_color_theme("blue")  # Set default color theme

root = ctk.CTk()
root.title("Material Cost Calculator")

# Dropdowns and Entry fields
machine_var = ctk.StringVar()
machine_var.trace_add('write', update_dropdowns) # Trigger update on machine selection

material_var = ctk.StringVar()
process_var = ctk.StringVar()

# Labels and dropdowns
ctk.CTkLabel(root, text="Select Machine:").grid(row=0, column=0, padx=10, pady=5)
machine_dropdown = ctk.CTkComboBox(root, variable=machine_var, values=machines)
machine_dropdown.grid(row=0, column=1, padx=10, pady=5)

ctk.CTkLabel(root, text="Select Material:").grid(row=1, column=0, padx=10, pady=5)
material_dropdown = ctk.CTkComboBox(root, variable=material_var, values=[])
material_dropdown.grid(row=1, column=1, padx=10, pady=5)

ctk.CTkLabel(root, text="Process:").grid(row=2, column=0, padx=10, pady=5)
process_entry = ctk.CTkEntry(root, textvariable=process_var, state='readonly')
process_entry.grid(row=2, column=1, padx=10, pady=5)

ctk.CTkLabel(root, text="Enter Volume (cm³):").grid(row=3, column=0, padx=10, pady=5)
volume_entry = ctk.CTkEntry(root)
volume_entry.grid(row=3, column=1, padx=10, pady=5)

# Calculate button
calculate_button = ctk.CTkButton(root, text="Calculate Cost", command=calculate_material_cost)
calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

root.mainloop()
