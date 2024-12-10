import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('manufacturing.db')
cursor = conn.cursor()


cursor.execute('DROP TABLE IF EXISTS MachineMaterialCost')
cursor.execute('DROP TABLE IF EXISTS Machines')
cursor.execute('DROP TABLE IF EXISTS Materials')
cursor.execute('DROP TABLE IF EXISTS Processes')

# Create tables
cursor.execute('''
CREATE TABLE Processes (
    ProcessID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProcessName TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE Machines (
    MachineID INTEGER PRIMARY KEY AUTOINCREMENT,
    MachineName TEXT NOT NULL,
    ProcessID INTEGER,
    FOREIGN KEY (ProcessID) REFERENCES Processes (ProcessID)
)
''')

cursor.execute('''
CREATE TABLE Materials (
    MaterialID INTEGER PRIMARY KEY AUTOINCREMENT,
    MaterialName TEXT NOT NULL,
    Density REAL NOT NULL
)
''')

cursor.execute('''
CREATE TABLE MachineMaterialCost (
    MachineID INTEGER,
    MaterialID INTEGER,
    Cost REAL,
    Unit TEXT,
    PRIMARY KEY (MachineID, MaterialID),
    FOREIGN KEY (MachineID) REFERENCES Machines (MachineID),
    FOREIGN KEY (MaterialID) REFERENCES Materials (MaterialID)
)
''')

# Insert data into Processes
cursor.execute("INSERT INTO Processes (ProcessName) VALUES ('FDM')")
cursor.execute("INSERT INTO Processes (ProcessName) VALUES ('SLA')")
cursor.execute("INSERT INTO Processes (ProcessName) VALUES ('SLS')")
cursor.execute("INSERT INTO Processes (ProcessName) VALUES ('SLM')")

# Insert data into Machines
cursor.execute("INSERT INTO Machines (MachineName, ProcessID) VALUES ('Ultimaker 3', 1)")
cursor.execute("INSERT INTO Machines (MachineName, ProcessID) VALUES ('Fortus 360mc', 1)")
cursor.execute("INSERT INTO Machines (MachineName, ProcessID) VALUES ('Form2', 2)")
cursor.execute("INSERT INTO Machines (MachineName, ProcessID) VALUES ('ProX 950', 2)")
cursor.execute("INSERT INTO Machines (MachineName, ProcessID) VALUES ('EOSINT P800', 3)")
cursor.execute("INSERT INTO Machines (MachineName, ProcessID) VALUES ('EOSm100 or 400-4', 4)")

# Insert data into Materials
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('ABS', 1.1)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Ultem', 1.27)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Clear Resin', 1.18)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Dental Model Resin', 1.18)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Accura Xtreme', 1.18)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Casting Resin', 1.18)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('PA2200', 0.93)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('PA12', 1.01)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Alumide', 1.36)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('Ti6Al4V', 4.43)")
cursor.execute("INSERT INTO Materials (MaterialName, Density) VALUES ('SSL316', 8.00)")

# Insert data into MachineMaterialCost
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (1, 1, 66.66, '$/kg')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (2, 2, 343, 'unit')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (3, 3, 149, '$/L')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (3, 4, 149, '$/L')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (4, 5, 2800, '$/10kg')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (3, 6, 299, '$/L')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (5, 7, 67.5, '$/kg')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (5, 8, 60, '$/kg')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (5, 9, 50, '$/kg')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (6, 10, 400, '$/kg')")
cursor.execute("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (6, 11, 30, '$/kg')")

# Commit and close connection
conn.commit()
conn.close()

print("Database created and populated successfully!")



def calculate_material_cost(machine_name, material_name, amount):
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()
    
    # Fetch MachineID and MaterialID based on names
    cursor.execute('''
        SELECT Machines.MachineID, Materials.MaterialID, MachineMaterialCost.Cost, MachineMaterialCost.Unit
        FROM Machines
        JOIN MachineMaterialCost ON Machines.MachineID = MachineMaterialCost.MachineID
        JOIN Materials ON Materials.MaterialID = MachineMaterialCost.MaterialID
        WHERE Machines.MachineName = ? AND Materials.MaterialName = ?
    ''', (machine_name, material_name))
    
    result = cursor.fetchone()
    
    if not result:
        print("No matching machine or material found.")
        conn.close()
        return None
    
    machine_id, material_id, cost, unit = result
    
    # Calculate total cost
    if unit in ['$kg', '$/L', '$/unit', '$/10kg','$/kg']:
        # Adjust amount based on unit
        if unit == '$/10kg':
            amount /= 10
        
        total_cost = cost * amount
        print(f"The total cost for {amount} units of {material_name} on {machine_name} is ${total_cost:.2f}")
    else:
        print(f"Unrecognized unit: {unit}.")
        total_cost = None
    
    # Close connection
    conn.close()
    
    return total_cost

# Example usage
calculate_material_cost('Ultimaker ', 'ABS', 5)  # Example call


