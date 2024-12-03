import sqlite3
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('manufacturing.db')
cursor = conn.cursor()

# Drop table if it exists (for testing purposes)
cursor.execute('DROP TABLE IF EXISTS PrintHistory')

# Create Print History table
cursor.execute('''
CREATE TABLE PrintHistory (
    PrintNumber INTEGER PRIMARY KEY AUTOINCREMENT,
    PrintFileName TEXT NOT NULL,
    Date TEXT NOT NULL,
    ProcessID INTEGER,
    MachineID INTEGER,
    MaterialID INTEGER,
    MaterialUsed REAL NOT NULL, -- in cm^3
    TotalCost REAL NOT NULL,
    Status TEXT NOT NULL CHECK(Status IN ('success', 'fail')),
    FOREIGN KEY (ProcessID) REFERENCES Processes(ProcessID),
    FOREIGN KEY (MachineID) REFERENCES Machines(MachineID),
    FOREIGN KEY (MaterialID) REFERENCES Materials(MaterialID)
)
''')

# Function to add a print record
def add_print_history(print_file_name, process_name, machine_name, material_name, material_used_cm3, status):
    conn = sqlite3.connect('manufacturing.db')
    cursor = conn.cursor()

    # Fetch IDs
    cursor.execute("SELECT ProcessID FROM Processes WHERE ProcessName = ?", (process_name,))
    process_id = cursor.fetchone()

    cursor.execute("SELECT MachineID FROM Machines WHERE MachineName = ?", (machine_name,))
    machine_id = cursor.fetchone()

    cursor.execute("SELECT MaterialID FROM Materials WHERE MaterialName = ?", (material_name,))
    material_id = cursor.fetchone()

    if not process_id or not machine_id or not material_id:
        print("Invalid process, machine, or material name.")
        conn.close()
        return

    process_id = process_id[0]
    machine_id = machine_id[0]
    material_id = material_id[0]

    # Fetch cost per unit
    cursor.execute('''
        SELECT Cost, Unit
        FROM MachineMaterialCost
        WHERE MachineID = ? AND MaterialID = ?
    ''', (machine_id, material_id))

    cost_data = cursor.fetchone()

    if not cost_data:
        print("No cost data found for the selected machine and material.")
        conn.close()
        return

    cost_per_unit, unit = cost_data

    # Convert material used to the correct unit
    if unit == '$/10kg':
        material_used_in_unit = material_used_cm3 / 10000  # Convert to kg
    elif unit == '$/kg':
        material_used_in_unit = material_used_cm3 / 1000  # Convert to kg
    elif unit == '$/L':
        material_used_in_unit = material_used_cm3 / 1000  # Convert to liters
    else:
        print(f"Unsupported unit: {unit}.")
        conn.close()
        return

    # Calculate total cost
    total_cost = material_used_in_unit * cost_per_unit

    # Insert into PrintHistory
    cursor.execute('''
        INSERT INTO PrintHistory (
            PrintFileName, Date, ProcessID, MachineID, MaterialID, MaterialUsed, TotalCost, Status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (print_file_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), process_id, machine_id, material_id,
          material_used_cm3, total_cost, status))

    conn.commit()
    conn.close()
    print("Print history record added successfully.")

# Example usage
add_print_history("example_file.stl", "FDM", "Ultimaker 3", "ABS", 1500, "success")
add_print_history("failed_file.stl", "SLA", "Form2", "Clear Resin", 2000, "fail")

# Query to verify the data
cursor.execute("SELECT * FROM PrintHistory")
for row in cursor.fetchall():
    print(row)

# Close connection
conn.close()



