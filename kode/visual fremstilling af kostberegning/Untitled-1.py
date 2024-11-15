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

# Konverter data til DataFrame for nemmere behandling
df = pd.DataFrame(data, columns=['Process', 'Machine', 'Material', 'Cost_per_unit', 'Unit'])

# Lad kunden vælge antallet af printere
num_printers = int(input("Indtast antal printere: "))

# Beregn samlede omkostninger ved at multiplicere kost pr. enhed med antallet af printere
df['Total_Cost'] = df['Cost_per_unit'] * num_printers

# Tegn linjegraf
plt.figure(figsize=(12, 8))
plt.plot(df['Material'], df['Total_Cost'], marker='o', linestyle='-', color='b')
plt.title(f'Samlede Omkostninger for {num_printers} Printere pr. Maskine og Materiale')
plt.xlabel('Materiale')
plt.ylabel('Samlede Omkostninger i USD')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.grid()
plt.show()





