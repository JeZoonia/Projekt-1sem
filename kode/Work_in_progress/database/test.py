import sqlite3
import customtkinter as ctk
from tkinter import messagebox

# Fetch machine names for the dropdown
def fetch_dropdown_data():
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    machines = [row[0] for row in cursor.execute("SELECT MachineName FROM Machine")]
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
        JOIN Machine ON Machine.MachineID = MaterialCostPerCM3.MachineID
        JOIN Materials ON Materials.MaterialID = MaterialCostPerCM3.MaterialID
        WHERE Machine.MachineName = ?
    ''', (machine_name,))]
    
    # Fetch the process type for the selected machine
    process_type = cursor.execute('''
        SELECT ProcessType
        FROM Machine
        WHERE MachineName = ?
    ''', (machine_name,)).fetchone()
    
    conn.close()
    return materials, process_type[0] if process_type else None

# Update materials and process dropdowns based on selected machine
def update_dropdowns(*args):
    selected_machine = machine_var.get()
    if selected_machine:
        compatible_materials, process_type = fetch_compatible_data(selected_machine)
        material_dropdown.configure(values=compatible_materials)
        material_var.set('')  # Clear previous material selection
        process_var.set(process_type)  # Set the process directly since it's one-to-one

# Calculate the total cost based on volume in cm³
def calculate_total_cost():
    try:
        volume_cm3 = float(volume_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for volume.")
        return

    machine_name, material_name = machine_var.get(), material_var.get()

    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()

    # Fetch material cost per cm³
    cursor.execute('''
        SELECT MaterialCostPerCM3.CostPerCM3
        FROM Machine
        JOIN MaterialCostPerCM3 ON Machine.MachineID = MaterialCostPerCM3.MachineID
        JOIN Materials ON Materials.MaterialID = MaterialCostPerCM3.MaterialID
        WHERE Machine.MachineName = ? AND Materials.MaterialName = ?
    ''', (machine_name, material_name))
    result = cursor.fetchone()

    if not result:
        messagebox.showinfo("Result", "No matching machine or material found.")
        conn.close()
        return

    cost_per_cm3 = result[0]
    material_cost = cost_per_cm3 * volume_cm3

    # Fetch build rate to calculate build time in hours
    cursor.execute('''
        SELECT BuildRate
        FROM BuildRate
        JOIN Machine ON Machine.MachineID = BuildRate.MachineID
        WHERE Machine.MachineName = ?
    ''', (machine_name,))
    build_rate_result = cursor.fetchone()

    if not build_rate_result:
        messagebox.showinfo("Result", "No build rate found for the selected machine.")
        conn.close()
        return

    build_rate = build_rate_result[0]
    build_time_hours = volume_cm3 / build_rate

    # Fetch employee pay rate per hour
    cursor.execute('''
        SELECT PayPerMachineSupervised
        FROM EmployeePay
        JOIN Machine ON Machine.MachineID = EmployeePay.MachineID
        WHERE Machine.MachineName = ?
    ''', (machine_name,))
    result = cursor.fetchone()
    employee_pay_rate = result[0] if result else 0
    employee_pay = build_time_hours * employee_pay_rate

    # Fetch fixed setup and removal costs for the machine
    cursor.execute('''
        SELECT SetupCost, RemovalCost
        FROM FixedCosts
        JOIN Machine ON Machine.MachineID = FixedCosts.MachineID
        WHERE Machine.MachineName = ?
    ''', (machine_name,))
    fixed_costs = cursor.fetchone()
    setup_cost = fixed_costs[0] if fixed_costs else 0
    removal_cost = fixed_costs[1] if fixed_costs else 0

    # Calculate process costs (additional operating cost and consumable cost)
    cursor.execute('''
        SELECT CostAmount
        FROM MachineCost
        JOIN CostType ON MachineCost.CostTypeID = CostType.CostTypeID
        JOIN Machine ON Machine.MachineID = MachineCost.MachineID
        WHERE Machine.MachineName = ? AND CostType.Unit = '$/hr'
    ''', (machine_name,))
    operating_cost_per_hour = sum([row[0] for row in cursor.fetchall()])
    operating_cost = operating_cost_per_hour * build_time_hours

    cursor.execute('''
        SELECT CostAmount
        FROM MachineCost
        JOIN CostType ON MachineCost.CostTypeID = CostType.CostTypeID
        JOIN Machine ON Machine.MachineID = MachineCost.MachineID
        WHERE Machine.MachineName = ? AND CostType.Unit = '$'
    ''', (machine_name,))
    consumable_cost = sum([row[0] for row in cursor.fetchall()])

    conn.close()

    # Total process cost
    process_cost = setup_cost + removal_cost + consumable_cost + operating_cost + employee_pay

    # Total cost
    total_cost = material_cost + process_cost

    # Display the result
    messagebox.showinfo(
        "Cost Calculation Result",
        f"Material Cost for {volume_cm3} cm³: ${material_cost:.2f}\n"
        f"Process Cost: ${process_cost:.2f}\n"
        f"Total Cost: ${total_cost:.2f}"
    )


    conn.close()

    # Total process cost
    process_cost = setup_cost + removal_cost + consumable_cost + operating_cost + employee_pay

    # Total cost
    total_cost = material_cost + process_cost

    # Display the result
    messagebox.showinfo(
        "Cost Calculation Result",
        f"Material Cost for {volume_cm3} cm³: ${material_cost:.2f}\n"
        f"Process Cost: ${process_cost:.2f}\n"
        f"Total Cost: ${total_cost:.2f}"
    )

# Initialize dropdown data
machines = fetch_dropdown_data()

# Set up customtkinter GUI window
ctk.set_appearance_mode("System")  # Use system theme
ctk.set_default_color_theme("blue")  # Set default color theme

root = ctk.CTk()
root.title("Material Cost Calculator")

# Dropdowns and Entry fields
machine_var = ctk.StringVar()
machine_var.trace_add('write', update_dropdowns)  # Trigger update on machine selection

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
calculate_button = ctk.CTkButton(root, text="Calculate Cost", command=calculate_total_cost)
calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

root.mainloop()
