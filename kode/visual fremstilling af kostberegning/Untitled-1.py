import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Materiale- og procesdata
material_data = { "ABS": {"cost": 66.66, "unit": "kg", "density": 1.1, "compatible_processes": ["FDM"]},
    "Ultem": {"cost": 343, "unit": "unit", "density": 1.27, "compatible_processes": ["FDM"]},
    "Clear Resin": {"cost": 149, "unit": "L", "density": 1.18, "compatible_processes": ["SLA"]},
    "PA2200": {"cost": 67.5, "unit": "kg", "density": 0.93, "compatible_processes": ["SLS"]},
    "Ti6Al4V": {"cost": 400, "unit": "kg", "density": 4.43, "compatible_processes": ["SLM"]},
    "Problack 10": {"cost": 250, "unit": "kg", "density": 1.07, "compatible_processes": ["DLP"]},}

process_machine_data = {  "FDM": ["Ultimaker 3", "Fortus 360mc"],
    "SLA": ["Form2", "ProX 950"],
    "SLS": ["EOSINT P800"],
    "SLM": ["EOSm100 or 400-4"],
    "DLP": ["3D Systems Figure 4"],}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("3D Printing Cost Estimation")
        self.geometry("800x600")
        self.grid_columnconfigure(1, weight=1)

        # Labels and Inputs
        self.label_material = ctk.CTkLabel(self, text="Select Material:")
        self.label_material.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.material_var = ctk.StringVar(value=list(material_data.keys())[0])
        self.dropdown_material = ctk.CTkOptionMenu(self, variable=self.material_var, values=list(material_data.keys()), command=self.update_process_dropdown)
        self.dropdown_material.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_process = ctk.CTkLabel(self, text="Select Process:")
        self.label_process.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.process_var = ctk.StringVar(value="")
        self.dropdown_process = ctk.CTkOptionMenu(self, variable=self.process_var, values=[])
        self.dropdown_process.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.label_machine = ctk.CTkLabel(self, text="Select Machine:")
        self.label_machine.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.machine_var = ctk.StringVar(value="")
        self.dropdown_machine = ctk.CTkOptionMenu(self, variable=self.machine_var, values=[])
        self.dropdown_machine.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.label_volume = ctk.CTkLabel(self, text="Volume per Print (cm³):")
        self.label_volume.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_volume = ctk.CTkEntry(self)
        self.entry_volume.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.label_num_prints = ctk.CTkLabel(self, text="Number of Prints:")
        self.label_num_prints.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_num_prints = ctk.CTkEntry(self)
        self.entry_num_prints.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.button_calculate = ctk.CTkButton(self, text="Calculate and Plot", command=self.calculate_and_plot)
        self.button_calculate.grid(row=5, column=0, columnspan=2, pady=20)

        # Initialize dropdowns
        self.update_process_dropdown()

    def update_process_dropdown(self, *args):
        selected_material = self.material_var.get()
        compatible_processes = material_data[selected_material]["compatible_processes"]
        self.dropdown_process.configure(values=compatible_processes)
        self.process_var.set(compatible_processes[0])
        self.update_machine_dropdown()

    def update_machine_dropdown(self, *args):
        selected_process = self.process_var.get()
        if selected_process in process_machine_data:
            machines = process_machine_data[selected_process]
            self.dropdown_machine.configure(values=machines)
            self.machine_var.set(machines[0])

    def calculate_and_plot(self):
        material = self.material_var.get()
        process = self.process_var.get()
        machine = self.machine_var.get()
        try:
            volume_cm3 = float(self.entry_volume.get())
            num_prints = int(self.entry_num_prints.get())
        except ValueError:
            ctk.CTkMessageBox.show_error("Invalid Input", "Please enter valid numbers for volume and number of prints.")
            return

        # Validation
        if process not in material_data[material]["compatible_processes"]:
            ctk.CTkMessageBox.show_error("Incompatibility", f"{process} is not compatible with {material}.")
            return

  # Sæt vinduets størrelse og titel
        self.title("CustomTkinter with Gray Background")
        self.geometry("600x400")

        # Sæt baggrundsfarve på hovedvinduet
        self.configure(fg_color="gray")  # Grå baggrund
        # Calculate cost
        material_info = material_data[material]
        cost_per_unit = material_info["cost"]
        density = material_info["density"]
        unit = material_info["unit"]

        weight_g = volume_cm3 * density
        if unit == "kg":
            cost_per_print = (weight_g / 1000) * cost_per_unit
        elif unit == "L":
            cost_per_print = (volume_cm3 / 1000) * cost_per_unit
        else:
            cost_per_print = cost_per_unit

        x = list(range(1, num_prints + 1))
        y = [cost_per_print * i for i in x]

        # Plot in CustomTkinter
        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', label=f'{material}, {machine} ({process})')
        ax.set_title("Cost vs Number of Prints")
        ax.set_xlabel("Number of Prints")
        ax.set_ylabel("Cost (DKK)")
        ax.legend()
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=6, column=0, columnspan=2, pady=20)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()






