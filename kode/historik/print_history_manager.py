import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

class PrintHistoryPage:
    def __init__(self, db_name='manufacturing.db'):
        """Initialize the class with a database connection."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Connect to the SQLite database."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Connected to database for Print History.")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def add_print_history(self, machine_id, material_id, print_time, cost, result):
        print_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
        INSERT INTO print_history (MachineID, MaterialID, PrintTime, PrintDate, Cost, Result)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (machine_id, material_id, print_time, print_date, cost, result))
        self.conn.commit()
        print("New print history record added.")

    def get_all_print_history(self):
        query = "SELECT * FROM print_history"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records

    def search_print_history(self, machine_id=None, material_id=None, result=None):
        conditions = []
        params = []
        if machine_id:
            conditions.append("MachineID = ?")
            params.append(machine_id)
        if material_id:
            conditions.append("MaterialID = ?")
            params.append(material_id)
        if result:
            conditions.append("Result = ?")
            params.append(result)

        query = "SELECT * FROM print_history"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        self.cursor.execute(query, params)
        records = self.cursor.fetchall()
        return records

    def delete_print_history(self, print_id):
        query = "DELETE FROM print_history WHERE PrintID = ?"
        self.cursor.execute(query, (print_id,))
        self.conn.commit()
        print(f"Print history record with PrintID {print_id} deleted.")

    def update_print_history(self, print_id, machine_id, material_id, print_time, cost, result):
        query = '''
        UPDATE print_history 
        SET MachineID = ?, MaterialID = ?, PrintTime = ?, Cost = ?, Result = ? 
        WHERE PrintID = ?
        '''
        self.cursor.execute(query, (machine_id, material_id, print_time, cost, result, print_id))
        self.conn.commit()
        print(f"Print history record with PrintID {print_id} updated.")

# Tkinter GUI for interacting with PrintHistoryPage
class PrintHistoryApp:
    def __init__(self, root, ph_page):
        self.ph_page = ph_page
        self.root = root
        self.root.title("Print History Manager")

        self.label = tk.Label(root, text="Print History Manager", font=("Arial", 16))
        self.label.pack(pady=10)

        self.edit_button = tk.Button(root, text="Edit Record", command=self.edit_record)
        self.edit_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Records", command=self.view_records)
        self.view_button.pack(pady=5)

        self.search_button = tk.Button(root, text="Search Records", command=self.search_records)
        self.search_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Record", command=self.delete_record)
        self.delete_button.pack(pady=5)

    def edit_record(self):
        print_id = simpledialog.askinteger("Input", "Enter Print ID to edit")
        if print_id:
            # Retrieve the current record details
            records = self.ph_page.search_print_history(print_id=print_id)
            if records:
                record = records[0]  # We assume only one record is returned
                # Pre-fill the fields with existing values
                machine_id = simpledialog.askinteger("Input", f"Machine ID (Current: {record[1]})", initialvalue=record[1])
                material_id = simpledialog.askinteger("Input", f"Material ID (Current: {record[2]})", initialvalue=record[2])
                print_time = simpledialog.askfloat("Input", f"Print Time (Current: {record[3]})", initialvalue=record[3])
                cost = simpledialog.askfloat("Input", f"Cost (Current: {record[5]})", initialvalue=record[5])
                result = simpledialog.askstring("Input", f"Result (Current: {record[6]})", initialvalue=record[6])

                # Update the record
                self.ph_page.update_print_history(print_id, machine_id, material_id, print_time, cost, result)
                messagebox.showinfo("Success", f"Record {print_id} updated successfully!")
            else:
                messagebox.showerror("Error", "Record not found!")
        
    def view_records(self):
        records = self.ph_page.get_all_print_history()
        record_window = tk.Toplevel(self.root)
        record_window.title("All Records")
        
        for record in records:
            tk.Label(record_window, text=str(record)).pack()

    def search_records(self):
        machine_id = simpledialog.askinteger("Input", "Enter Machine ID (optional)")
        material_id = simpledialog.askinteger("Input", "Enter Material ID (optional)")
        result = simpledialog.askstring("Input", "Enter Result (optional)")

        search_results = self.ph_page.search_print_history(machine_id, material_id, result)
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Results")

        for record in search_results:
            tk.Label(search_window, text=str(record)).pack()

    def delete_record(self):
        print_id = simpledialog.askinteger("Input", "Enter Print ID to delete")
        self.ph_page.delete_print_history(print_id)
        messagebox.showinfo("Success", f"Record {print_id} deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    ph_page = PrintHistoryPage()  # Initialize the database handler
    app = PrintHistoryApp(root, ph_page)  # Initialize the Tkinter app
    root.mainloop()

    ph_page.close()  # Close the database connection when the app is closed

