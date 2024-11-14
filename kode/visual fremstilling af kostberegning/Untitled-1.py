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

# Beregn de samlede omkostninger for hver type materiale
categories = []
costs = []
for process, machine, material, cost, unit in data:
    categories.append(f"{process} - {machine} - {material}")
    costs.append(cost)

# Visualisering
plt.figure(figsize=(10, 6))
plt.barh(categories, costs, color='skyblue')
plt.title('Omkostninger pr. Maskine og Materiale')
plt.xlabel('Omkostning i USD')
plt.ylabel('Processer og Maskiner')
plt.tight_layout()
plt.show()





