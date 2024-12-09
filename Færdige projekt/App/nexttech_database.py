import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('manufacturing.db')
cursor = conn.cursor()

# Drop existing tables if they exist
cursor.execute('DROP TABLE IF EXISTS Machine')
cursor.execute('DROP TABLE IF EXISTS BuildRate')
cursor.execute('DROP TABLE IF EXISTS CostType')
cursor.execute('DROP TABLE IF EXISTS MachineCost')
cursor.execute('DROP TABLE IF EXISTS FixedCosts')
cursor.execute('DROP TABLE IF EXISTS EmployeePay')
cursor.execute('DROP TABLE IF EXISTS Materials')
cursor.execute('DROP TABLE IF EXISTS MachineMaterialCost')
cursor.execute('DROP TABLE IF EXISTS MaterialCostPerCM3')




# Create tables
cursor.execute('''
CREATE TABLE Machine (
    MachineID INTEGER PRIMARY KEY AUTOINCREMENT,
    MachineName TEXT NOT NULL,
    ProcessType TEXT NOT NULL
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

cursor.execute('''
CREATE TABLE BuildRate (
    MachineID INTEGER PRIMARY KEY,
    BuildRate REAL NOT NULL,
    FOREIGN KEY (MachineID) REFERENCES Machine (MachineID)
)
''')

cursor.execute('''
CREATE TABLE CostType (
    CostTypeID INTEGER PRIMARY KEY AUTOINCREMENT,
    CostDescription TEXT NOT NULL,
    Unit TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE MachineCost (
    MachineID INTEGER,
    CostTypeID INTEGER,
    CostAmount REAL,
    PRIMARY KEY (MachineID, CostTypeID),
    FOREIGN KEY (MachineID) REFERENCES Machine (MachineID),
    FOREIGN KEY (CostTypeID) REFERENCES CostType (CostTypeID)
)
''')

cursor.execute('''
CREATE TABLE FixedCosts (
    MachineID INTEGER PRIMARY KEY,
    SetupCost REAL,
    RemovalCost REAL,
    FOREIGN KEY (MachineID) REFERENCES Machine (MachineID)
)
''')

cursor.execute('''
CREATE TABLE EmployeePay (
    MachineID INTEGER PRIMARY KEY,
    PayPerMachineSupervised REAL NOT NULL,
    FOREIGN KEY (MachineID) REFERENCES Machine (MachineID)
)
''')


# Create MaterialCostPerCM3 table
cursor.execute('''
CREATE TABLE MaterialCostPerCM3 (
    MachineID INTEGER,
    MaterialID INTEGER,
    CostPerCM3 REAL,
    PRIMARY KEY (MachineID, MaterialID),
    FOREIGN KEY (MachineID) REFERENCES Machines (MachineID),
    FOREIGN KEY (MaterialID) REFERENCES Materials (MaterialID)
)
''')


# Insert data
# Machine data
machines = [
    ('Ultimaker 3', 'FDM'),
    ('Fortus 360mc', 'FDM'),
    ('Form2', 'SLA'),
    ('ProX 950', 'SLA'),
    ('EOSINT P800', 'SLS'),
    ('EOSm100', 'SLM'),
    ('EOSm400-4', 'SLM'),
    ('Figure 4 - Stand Alone', 'DLP'),
    ('Figure 4 - Modular', 'DLP')
]
cursor.executemany("INSERT INTO Machine (MachineName, ProcessType) VALUES (?, ?)", machines)

# Insert for Materials
materials_data = [
    ('ABS', 1.1),
    ('Ultem', 1.27),
    ('Clear Resin', 1.18),
    ('Dental Model Resin', 1.18),
    ('Accura Xtreme', 1.18),
    ('Casting Resin', 1.18),
    ('PA2200', 0.93),
    ('PA12', 1.01),
    ('Alumide', 1.36),
    ('Ti6Al4V', 4.43),
    ('SSL316', 8.00),
    ('Problack 10', 1.07)
]
cursor.executemany("INSERT INTO Materials (MaterialName, Density) VALUES (?, ?)", materials_data)

# Insert for MachineMaterialCost
machine_material_cost_data = [
    (1, 1, 66.66, '$/kg'),
    (2, 2, 343, 'unit'),
    (3, 3, 149, '$/L'),
    (3, 4, 149, '$/L'),
    (4, 5, 2800, '$/10kg'),
    (3, 6, 299, '$/L'),
    (5, 7, 67.5, '$/kg'),
    (5, 8, 60, '$/kg'),
    (5, 9, 50, '$/kg'),
    (6, 10, 400, '$/kg'),
    (6, 11, 30, '$/kg'),
    (7,10, 400, '$/kg'),
    (7, 11, 30, '$/kg'),
    (8, 12, 250, '$/kg'),
    (9, 12, 250, '$/kg')
]

cursor.executemany("INSERT INTO MachineMaterialCost (MachineID, MaterialID, Cost, Unit) VALUES (?, ?, ?, ?)", machine_material_cost_data)

# BuildRate data
build_rates = [
    (1, 29),
    (2, 61),
    (3, 105),
    (4, 600),
    (5, 2774),
    (6, 5),
    (7, 107),
    (8, 569),
    (9, 569)
]
cursor.executemany("INSERT INTO BuildRate (MachineID, BuildRate) VALUES (?, ?)", build_rates)

# CostType data
cost_types = [
    ('Additional operating cost (e.g., inert gas)', '$/hr'),
    ('Consumable cost per build (e.g., build plate)', '$'),
    ('First-time build preparation (engineer)', '$'),
    ('Subsequent build preparation (engineer)', '$')
]
cursor.executemany("INSERT INTO CostType (CostDescription, Unit) VALUES (?, ?)", cost_types)

# MachineCost data
machine_costs = [
    (1, 2, 0.58),
    (2, 3, 70),
    (3, 3, 70),
    (3, 2, 3.72),
    (4, 3, 140),
    (4, 2, 0.25),
    (4, 4, 0),
    (5, 2, 1.5),
    (7, 3, 70),
    (7, 2, 1),
    (8, 2, 25),
    (9, 2, 25)
]
cursor.executemany("INSERT INTO MachineCost (MachineID, CostTypeID, CostAmount) VALUES (?, ?, ?)", machine_costs)

# FixedCosts data
fixed_costs = [
    (1, 20, 20),
    (2, 20, 20),
    (4, 10, 12.5),
    (7, 25, 25),
    (8, 37.5, 25),
    (9, 37.5, 25)
]
cursor.executemany("INSERT INTO FixedCosts (MachineID, SetupCost, RemovalCost) VALUES (?, ?, ?)", fixed_costs)

# EmployeePay data
employee_pays = [
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 4),
    (5, 5),
    (6, 5),
    (7, 5),
    (8, 7.5),
    (9, 7.5)
]
cursor.executemany("INSERT INTO EmployeePay (MachineID, PayPerMachineSupervised) VALUES (?, ?)", employee_pays)


# Calculate cost per cm³ for each material based on density and unit cost in MachineMaterialCost
cursor.execute('''
INSERT INTO MaterialCostPerCM3 (MachineID, MaterialID, CostPerCM3)
SELECT 
    mmc.MachineID,
    mmc.MaterialID,
    CASE 
        WHEN mmc.Unit = '$/kg' THEN mmc.Cost / (materials.Density * 1000)
        WHEN mmc.Unit = 'unit' THEN NULL  -- Handle 'unit' separately if necessary
        WHEN mmc.Unit = '$/L' THEN mmc.Cost / 1000
        WHEN mmc.Unit = '$/10kg' THEN (mmc.Cost / 10) / (materials.Density * 1000)
        ELSE NULL
    END AS CostPerCM3
FROM MachineMaterialCost AS mmc
JOIN Materials ON mmc.MaterialID = Materials.MaterialID
''')


# Commit and close connection
conn.commit()
conn.close()

print("Database created and populated successfully!")
