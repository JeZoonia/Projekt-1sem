import sqlite3
from datetime import datetime

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
        """
        Add a new record to the print history.
        Args:
        - machine_id (int): ID of the machine used.
        - material_id (int): ID of the material used.
        - print_time (float): Time spent printing (in hours).
        - cost (float): Cost of the print.
        - result (str): Outcome of the print (e.g., "success" or "fail").
        """
        print_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = '''
        INSERT INTO print_history (MachineID, MaterialID, PrintTime, PrintDate, Cost, Result)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, (machine_id, material_id, print_time, print_date, cost, result))
        self.conn.commit()
        print("New print history record added.")

    def get_all_print_history(self):
        """
        Retrieve all records from the print history.
        Returns:
        - List of tuples containing print history records.
        """
        query = "SELECT * FROM print_history"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records

    def search_print_history(self, machine_id=None, material_id=None, result=None):
        """
        Search print history based on specific criteria.
        Args:
        - machine_id (int, optional): Filter by machine ID.
        - material_id (int, optional): Filter by material ID.
        - result (str, optional): Filter by result (e.g., "success").
        Returns:
        - List of tuples matching the criteria.
        """
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
        """
        Delete a specific print history record by PrintID.
        Args:
        - print_id (int): ID of the print history record to delete.
        """
        query = "DELETE FROM print_history WHERE PrintID = ?"
        self.cursor.execute(query, (print_id,))
        self.conn.commit()
        print(f"Print history record with PrintID {print_id} deleted.")

# Example Usage
if __name__ == "__main__":
    ph_page = PrintHistoryPage()

    # Adding a new print history record
    ph_page.add_print_history(machine_id=1, material_id=2, print_time=3.5, cost=150.00, result="success")

    # Retrieving all print history records
    history = ph_page.get_all_print_history()
    print("\nAll Print History Records:")
    for record in history:
        print(record)

    # Searching print history
    search_results = ph_page.search_print_history(machine_id=1, result="success")
    print("\nSearch Results:")
    for record in search_results:
        print(record)

    # Deleting a print history record
    ph_page.delete_print_history(print_id=1)

    ph_page.close()









