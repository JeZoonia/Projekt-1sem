import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data for materialer og omkostninger
data = [
    ('FDM', 'Ultimaker 3', 'ABS', 66.66, 'kg'),
    ('FDM', 'Fortus 360mc', 'Ultem', 343, 'unit'),
    ('SLA', 'Form2', 'Clear Resin', 149, 'L'),
    ('SLA', 'Form2', 'Dental Model Resin', 149, 'L'),
    ('SLA', 'ProX 950', 'Accura Xtreme', 2800, '10kg'),
    ('SLA', 'Form2', 'Casting Resin', 299, 'L'),
    ('SLS', 'EOSINT P800', 'PA2200', 67.5, 'kg'),
    ('SLS', 'EOSINT P800', 'PA12', 60, 'kg'),
    ('SLS', 'EOSINT P800', 'Alumide', 50, 'kg'),
    ('SLM', 'EOSm100 or 400-4', 'Ti6Al4V', 400, 'kg'),
    ('SLM', 'EOSm100 or 400-4', 'SSL316', 30, 'kg'),
    ('DLP', '3D Systems Figure 4', 'Problack 10', 250, 'kg')
]

# Konverter data til en DataFrame for nem manipulation
df = pd.DataFrame(data, columns=['Process', 'Machine', 'Material', 'Cost_per_unit', 'Unit'])

# Funktion til at beregne og vise samlede omkostninger baseret på brugerinput for antal printere
def plot_total_cost(num_printers):
    # Beregn de samlede omkostninger for hver printer/materiale baseret på antal
    df['Total_Cost'] = df['Cost_per_unit'] * num_printers  # Opdater omkostningerne baseret på antal printere

    # Visualisering
    plt.figure(figsize=(12, 8))
    plt.barh(df['Process'] + " - " + df['Machine'] + " - " + df['Material'] + " (" + df['Unit'] + ")", df['Total_Cost'], color='skyblue')
    plt.title(f'Samlede Omkostninger pr. Maskine og Materiale baseret på {num_printers} Printer(e)')
    plt.xlabel('Samlede Omkostninger i USD')
    plt.ylabel('Processer, Maskiner og Materiale (med Enhed)')
    plt.tight_layout()
    plt.show()

# Eksempel: Brugeren vælger antal printere
num_printers = int(input("Indtast antal printere: "))  # Brugeren indtaster antal printere
plot_total_cost(num_printers)






