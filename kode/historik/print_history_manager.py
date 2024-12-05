import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk  # Import ttk for Treeview
import customtkinter as ctk
import sqlite3

# Opretter en klasse til at håndtere databasen
class PrintHistoryDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS PrintHistoryData')
        self.cursor.execute('''
        CREATE TABLE PrintHistoryData (
            PrintNumber INTEGER PRIMARY KEY,
            PrintDate TEXT,
            MachineName TEXT,
            MaterialName TEXT,
            Volume REAL,
            TotalCost REAL
        )
        ''')
        self.conn.commit()

    def insert_data(self, data_to_insert):
        for record in data_to_insert:
            self.cursor.execute('''
            INSERT OR IGNORE INTO PrintHistoryData (PrintNumber, PrintDate, MachineName, MaterialName, Volume, TotalCost) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', record)
        self.conn.commit()

    def update_data(self, print_number, volume, total_cost):
        # Opdaterer Volume og TotalCost baseret på PrintNumber
        self.cursor.execute('''
        UPDATE PrintHistoryData
        SET Volume = ?, TotalCost = ?
        WHERE PrintNumber = ?
        ''', (volume, total_cost, print_number))
        self.conn.commit()

    def get_all_data(self):
        # Henter alle data fra tabellen
        self.cursor.execute('SELECT * FROM PrintHistoryData')
        return self.cursor.fetchall()

    def close_connection(self):
        self.conn.close()

# GUI med customtkinter
class PrintHistoryManagerApp:
    def __init__(self, root):
        self.db = PrintHistoryDatabase('manufacturing.db')
        self.db.create_table()

        self.root = root
        self.root.title("Print History Manager")
        self.root.geometry("800x600")

        # Brug ttk.Treeview i stedet for customtkinter
        self.table = ttk.Treeview(self.root, columns=("PrintNumber", "PrintDate", "MachineName", "MaterialName", "Volume", "TotalCost"), show="headings")
        self.table.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Opsætning af kolonner
        self.table.heading("PrintNumber", text="PrintNumber")
        self.table.heading("PrintDate", text="PrintDate")
        self.table.heading("MachineName", text="MachineName")
        self.table.heading("MaterialName", text="MaterialName")
        self.table.heading("Volume", text="Volume")
        self.table.heading("TotalCost", text="TotalCost")

        # Knapper
        self.reprint_button = ctk.CTkButton(self.root, text="Reprint", command=self.reprint_data)
        self.reprint_button.grid(row=1, column=0, padx=10, pady=10)

        self.edit_button = ctk.CTkButton(self.root, text="Edit", command=self.edit_data)
        self.edit_button.grid(row=2, column=0, padx=10, pady=10)

        # Indsæt nogle testdata (kun første gang, eller hvis data er tomme)
        data_to_insert = [
            (1, '2024-12-05', 'Ultimaker 3', 'ABS', 2.0, 40.84),
            (2, '2024-12-05', 'Ultimaker 3', 'ABS', 5.0, 453.51),
            (3, '2024-12-05', 'ProX 950', 'Accura Xtreme', 2.0, 163.24),
            (4, '2024-12-05', 'EOSm100', 'SSL316', 3.0, 3.01),
            (5, '2024-12-05', 'EOSm100', 'SSL316', 3.0, 15.06),
            (6, '2024-12-05', 'EOSm100', 'SSL316', 333.0, 1671.24),
            (7, '2024-12-05', 'Ultimaker 3', 'ABS', 44.0, 2036.36),
            (8, '2024-12-05', 'Ultimaker 3', 'ABS', 44.0, 2036.36),
            (9, '2024-12-05', 'Ultimaker 3', 'ABS', 3.0, 122.91),
            (10, '2024-12-05', 'Ultimaker 3', 'ABS', 3.0, 122.91),
        ]
        self.db.insert_data(data_to_insert)

        self.load_data()

    def load_data(self):
        # Henter alle data fra databasen og viser dem i tabellen
        data = self.db.get_all_data()
        print("Loaded data:", data)  # Debugging output

        if not data:
            print("No data found in the database.")  # Debugging output

        for row in data:
            self.table.insert('', 'end', values=row)

    def reprint_data(self):
        # Reprint den valgte række (simpelthen ved at printe den ud i terminalen)
        selected_item = self.table.selection()
        if selected_item:
            print_number = self.table.item(selected_item, "values")[0]
            print(f"Reprinting data for PrintNumber: {print_number}")
        else:
            print("No item selected")

    def edit_data(self):
        # Redigerer data for den valgte række
        selected_item = self.table.selection()
        if selected_item:
            # Henter værdierne fra den valgte række
            selected_values = self.table.item(selected_item, "values")
            print_number = selected_values[0]
            volume = selected_values[4]
            total_cost = selected_values[5]

            # Bekræftelse på redigering
            new_volume = simpledialog.askfloat("Edit Volume", "Enter new volume:", initialvalue=volume)
            if new_volume is not None:
                new_total_cost = new_volume * 40.84  # Beregn ny total cost (eksempel)
                self.db.update_data(print_number, new_volume, new_total_cost)

                # Opdater tabellen
                self.table.item(selected_item, values=(print_number, selected_values[1], selected_values[2], selected_values[3], new_volume, new_total_cost))

                print(f"Data updated for PrintNumber {print_number}. New Volume: {new_volume}, New TotalCost: {new_total_cost}")
        else:
            print("No item selected")

# Main application
if __name__ == "__main__":
    root = ctk.CTk()
    app = PrintHistoryManagerApp(root)
    root.mainloop()
