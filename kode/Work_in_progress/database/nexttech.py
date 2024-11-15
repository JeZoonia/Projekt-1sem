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

# Create tables
cursor.execute('''
CREATE TABLE Machine (
    MachineID INTEGER PRIMARY KEY AUTOINCREMENT,
    MachineName TEXT NOT NULL,
    ProcessType TEXT NOT NULL
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

# Insert data
# Machine data
machines = [
    ('Ultimaker 3', 'FDM'),
    ('Stratasys Fortus 360mc', 'FDM'),
    ('Form2', 'SLA'),
    ('3D Systems ProX 950', 'SLA'),
    ('Figure 4 - Stand Alone', 'DLP'),
    ('Figure 4 - Modular', 'DLP'),
    ('EOSINT P800', 'SLS'),
    ('EOSm100', 'SLM'),
    ('EOSm400-4', 'SLM')
]
cursor.executemany("INSERT INTO Machine (MachineName, ProcessType) VALUES (?, ?)", machines)

# BuildRate data
build_rates = [
    (1, 29),
    (2, 61),
    (3, 105),
    (4, 600),
    (5, 569),
    (6, 569),
    (7, 2774),
    (8, 5),
    (9, 107)
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
    (2, 10, 20),
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

# Commit and close connection
conn.commit()
conn.close()

print("Database created and populated successfully!")
