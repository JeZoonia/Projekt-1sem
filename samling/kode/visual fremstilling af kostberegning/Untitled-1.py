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

        self.title("nexttech calculator")
        self.geometry("800x600")  # Justeret for prisramme
        self.grid_columnconfigure(1, weight=1)
        self.configure(fg_color="#808080")  # dark baggrund

        # Labels og Input
        self.label_material = ctk.CTkLabel(self, text="Vælg Materiale:")
        self.label_material.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.material_var = ctk.StringVar(value=list(material_data.keys())[0])
        self.dropdown_material = ctk.CTkOptionMenu(
            self,
            variable=self.material_var,
            values=list(material_data.keys()),
            command=self.update_process_dropdown,
        )
        self.dropdown_material.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_process = ctk.CTkLabel(self, text="Vælg Proces:")
        self.label_process.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.process_var = ctk.StringVar(value="")
        self.dropdown_process = ctk.CTkOptionMenu(self, variable=self.process_var, values=[])
        self.dropdown_process.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.label_machine = ctk.CTkLabel(self, text="Vælg Maskine:")
        self.label_machine.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.machine_var = ctk.StringVar(value="")
        self.dropdown_machine = ctk.CTkOptionMenu(self, variable=self.machine_var, values=[])
        self.dropdown_machine.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.label_volume = ctk.CTkLabel(self, text="Volumen pr. Print (cm³):")
        self.label_volume.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_volume = ctk.CTkEntry(self)
        self.entry_volume.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.label_num_prints = ctk.CTkLabel(self, text="Antal Prints:")
        self.label_num_prints.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.entry_num_prints = ctk.CTkEntry(self)
        self.entry_num_prints.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.button_calculate = ctk.CTkButton(
            self, text="Beregn og Vis", fg_color="green", text_color="white", command=self.calculate_and_plot
        )
        self.button_calculate.grid(row=5, column=0, columnspan=2, pady=20)

        # Placeholder til grafen
        self.plot_frame = ctk.CTkFrame(self, width=500, height=400)
        self.plot_frame.grid(row=0, column=2, rowspan=6, padx=10, pady=10, sticky="nsew")

        # Prisramme
        self.price_frame = ctk.CTkFrame(self, width=500, height=100, corner_radius=10)
        self.price_frame.grid(row=6, column=2, padx=10, pady=10, sticky="nsew")

        self.label_cost_per_unit = ctk.CTkLabel(self.price_frame, text="Pris pr. Print: - USD", font=("Arial", 14))
        self.label_cost_per_unit.pack(pady=10)

        self.label_total_cost = ctk.CTkLabel(self.price_frame, text="Total Pris: - USD", font=("Arial", 14))
        self.label_total_cost.pack(pady=10)

        # Opdater dropdowns
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
            ctk.CTkMessageBox.show_error("Ugyldig Input", "Indtast venligst gyldige tal for volumen og antal prints.")
            return

        # Validering
        if process not in material_data[material]["compatible_processes"]:
            ctk.CTkMessageBox.show_error("Inkompatibilitet", f"{process} er ikke kompatibel med {material}.")
            return

        # Beregn omkostninger
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

        total_cost = cost_per_print * num_prints

        # Opdater prisrammen
        self.label_cost_per_unit.configure(text=f"Pris pr. Print: {cost_per_print:.2f} USD")
        self.label_total_cost.configure(text=f"Total Pris: {total_cost:.2f} USD")

        # Plot i CustomTkinter
        x = list(range(1, num_prints + 1))
        y = [cost_per_print * i for i in x]

        fig, ax = plt.subplots()
        ax.plot(x, y, marker='o', label=f'{material}, {machine} ({process})')
        ax.set_title("Pris vs Antal Prints")
        ax.set_xlabel("Antal Prints")
        ax.set_ylabel("Pris (USD)")
        ax.legend()
        ax.grid()

        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
