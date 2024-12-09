import sqlite3

class PrintHistoryDatabase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS PrintHistoryData')
        self.cursor.execute('''CREATE TABLE PrintHistoryData ( PrintNumber INTEGER PRIMARY KEY,PrintDate TEXT, MachineName TEXT,
         MaterialName TEXT,Volume REAL,TotalCost REAL)''')
        print("Table 'PrintHistoryData' created successfully.")
    def insert_data(self, data_to_insert):
        for record in data_to_insert:
            self.cursor.execute('''
            INSERT OR IGNORE INTO PrintHistoryData (PrintNumber, PrintDate, MachineName, MaterialName, Volume, TotalCost) 
            VALUES (?, ?, ?, ?, ?, ?)
            ''', record)
        self.conn.commit()
        print("Data inserted into the database.")

    def close_connection(self):
        self.conn.close()
        print("Database connection closed.")
data_to_insert = [ (1, '2024-12-05', 'Ultimaker 3', 'ABS', 2.0, 40.84),
    (2, '2024-12-05', 'Ultimaker 3', 'ABS', 5.0, 453.51),
    (3, '2024-12-05', 'ProX 950', 'Accura Xtreme', 2.0, 163.24),
    (4, '2024-12-05', 'EOSm100', 'SSL316', 3.0, 3.01),
    (5, '2024-12-05', 'EOSm100', 'SSL316', 3.0, 15.06),
    (6, '2024-12-05', 'EOSm100', 'SSL316', 333.0, 1671.24),
    (7, '2024-12-05', 'Ultimaker 3', 'ABS', 44.0, 2036.36),
    (8, '2024-12-05', 'Ultimaker 3', 'ABS', 44.0, 2036.36),
    (9, '2024-12-05', 'Ultimaker 3', 'ABS', 3.0, 122.91),
    (10, '2024-12-05', 'Ultimaker 3', 'ABS', 3.0, 122.91),]
db = PrintHistoryDatabase('manufacturing.db')
db.create_table()
db.insert_data(data_to_insert)
db.close_connection()
