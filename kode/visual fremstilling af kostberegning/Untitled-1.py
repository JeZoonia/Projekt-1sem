import matplotlib.pyplot as plt

# Table data (unchanged)
material_data = { "ABS": {"cost": 66.66, "unit": "kg", "density": 1.1, "compatible_processes": ["FDM"]},
    "Ultem": {"cost": 343, "unit": "unit", "density": 1.27, "compatible_processes": ["FDM"]},
    "Clear Resin": {"cost": 149, "unit": "L", "density": 1.18, "compatible_processes": ["SLA"]},
    "Dental Model Resin": {"cost": 149, "unit": "L", "density": 1.18, "compatible_processes": ["SLA"]},
    "Accura Xtreme": {"cost": 2800, "unit": "10kg", "density": 1.18, "compatible_processes": ["SLA"]},
    "Casting Resin": {"cost": 299, "unit": "L", "density": 1.18, "compatible_processes": ["SLA"]},
    "PA2200": {"cost": 67.5, "unit": "kg", "density": 0.93, "compatible_processes": ["SLS"]},
    "PA12": {"cost": 60, "unit": "kg", "density": 1.01, "compatible_processes": ["SLS"]},
    "Alumide": {"cost": 50, "unit": "kg", "density": 1.36, "compatible_processes": ["SLS"]},
    "Ti6Al4V": {"cost": 400, "unit": "kg", "density": 4.43, "compatible_processes": ["SLM"]},
    "SSL316": {"cost": 30, "unit": "kg", "density": 8, "compatible_processes": ["SLM"]},
    "Problack 10": {"cost": 250, "unit": "kg", "density": 1.07, "compatible_processes": ["DLP"]},}

process_machine_data = {  "FDM": ["Ultimaker 3", "Fortus 360mc"],
    "SLA": ["Form2", "ProX 950"],
    "SLS": ["EOSINT P800"],
    "SLM": ["EOSm100 or 400-4"],
    "DLP": ["3D Systems Figure 4"],}

# Function to calculate and plot costs
def calculate_and_plot_cost(material, process, machine, num_prints, volume_cm3):
    # Validation
    if material not in material_data:
        print("The selected material is not valid!")
        return
    if process not in material_data[material]["compatible_processes"]:
        print("The selected process is not compatible with the material!")
        return
    if process not in process_machine_data or machine not in process_machine_data[process]:
        print("The selected machine is not compatible with the process!")
        return

    # Get data
    material_info = material_data[material]
    cost_per_unit = material_info["cost"]
    density = material_info["density"]
    unit = material_info["unit"]

    # Calculate weight from volume using density (volume in cm³, density in g/cm³)
    weight_g = (volume_cm3 * density)  # Convert cm³ to grams using density

    # Calculate cost per print
    if unit == "kg":
        cost_per_print = (weight_g / 1000) * cost_per_unit  # Cost by weight (convert g to kg)
    elif unit == "L":
        cost_per_print = (volume_cm3 / 1000) * cost_per_unit  # Cost by volume in liters
    else:
        cost_per_print = cost_per_unit  # Flat cost for unit-based pricing

    # Calculate total costs for each print
    x = list(range(1, num_prints + 1))  # Number of prints
    y = [cost_per_print * i for i in x]  # Total costs

    # Plot graph
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', label=f'{material}, {machine} ({process})')
    plt.title("Cost vs Number of Prints")
    plt.xlabel("Number of Prints")
    plt.ylabel("Cost (DKK)")
    plt.legend()
    plt.grid()
    plt.show()


# Main program: Interactive inputs
if __name__ == "__main__":
    print("Welcome to the 3D Printing Cost Estimation Program!")

    # Get material
    print("\nAvailable Materials:")
    for material in material_data.keys():
        print(f"- {material}")
    material = input("Select a material: ").strip()

    # Show compatible processes
    if material in material_data:
        compatible_processes = material_data[material]["compatible_processes"]
        print(f"\nCompatible processes for {material}:")
        for process in compatible_processes:
            print(f"- {process}")
        process = input("Select a process: ").strip()
    else:
        print("The material is not valid!")
        exit()

    # Show compatible machines
    if process in compatible_processes:
        print(f"\nCompatible machines for {process}:")
        for machine in process_machine_data[process]:
            print(f"- {machine}")
        machine = input("Select a machine: ").strip()
    else:
        print("The process is not valid!")
        exit()

    # Get volume per print
    try:
        volume_cm3 = float(input("Enter the volume per print (cm³): ").strip())
    except ValueError:
        print("The volume must be a number!")
        exit()

    # Get number of prints
    try:
        num_prints = int(input("Enter the number of prints: ").strip())
    except ValueError:
        print("The number of prints must be a number!")
        exit()

    # Calculate and plot costs
    calculate_and_plot_cost(material, process, machine, num_prints, volume_cm3)





