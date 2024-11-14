import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def plot_cost_calculation(machine_name, material_names, max_amount=10):
    # Åben forbindelse til databasen
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    
    amounts = np.linspace(1, max_amount, 10)  # Generer en række mængder fra 1 til max_amount
    
    plt.figure(figsize=(10, 6))
    
    for material_name in material_names:
        costs = []
        
        # Beregn kost for hver mængde og tilføj til liste
        for amount in amounts:
            cursor.execute('''
                SELECT Machines.MachineID, Materials.MaterialID, MachineMaterialCost.Cost, MachineMaterialCost.Unit
                FROM Machines
                JOIN MachineMaterialCost ON Machines.MachineID = MachineMaterialCost.MachineID
                JOIN Materials ON Materials.MaterialID = MachineMaterialCost.MaterialID
                WHERE Machines.MachineName = ? AND Materials.MaterialName = ?
            ''', (machine_name, material_name))
            
            result = cursor.fetchone()
            
            if result:
                machine_id, material_id, cost, unit = result
                if unit == '$/10kg':
                    amount /= 10
                total_cost = cost * amount
                costs.append(total_cost)
            else:
                print(f"No matching data found for {material_name} on {machine_name}.")
                costs.append(0)  # Tilføj 0 hvis der mangler data
        
        # Plot data for dette materiale
        plt.plot(amounts, costs, label=material_name)
    
    # Luk forbindelse til databasen
    conn.close()
    
    # Plotindstillinger
    plt.xlabel('Amount (kg or L)')
    plt.ylabel('Total Cost ($)')
    plt.title(f'Cost Calculation for Different Materials on {machine_name}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Eksempel brug
plot_cost_calculation('Ultimaker 3', ['ABS', 'Ultem', 'Clear Resin'], max_amount=10)





