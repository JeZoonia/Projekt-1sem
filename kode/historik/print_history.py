import sqlite3

class DatabaseHandler:
    def __init__(self, database_name):
        """Initialiserer databaseforbindelsen."""
        self.database_name = database_name

    def opret_forbindelse(self):
        """Opretter og returnerer en forbindelse til databasen."""
        return sqlite3.connect(self.database_name)

    def opret_print_history_tabel(self):
        """Opretter 'print_history' tabellen med id som primær nøgle."""
        opret_tabel_query = """
        CREATE TABLE IF NOT EXISTS print_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            print_date TEXT NOT NULL,
            file_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            machine_id INTEGER NOT NULL,
            total_cost REAL NOT NULL,
            FOREIGN KEY (material_id) REFERENCES materials(material_id),
            FOREIGN KEY (machine_id) REFERENCES machines(machine_id)
        );
        """
        try:
            # Opretter forbindelse og kører forespørgslen
            forbindelse = self.opret_forbindelse()
            cursor = forbindelse.cursor()
            cursor.execute(opret_tabel_query)
            forbindelse.commit()
            print("Tabellen 'print_history' blev oprettet succesfuldt.")
        except Exception as e:
            print(f"Fejl ved oprettelse af tabellen: {e}")
        finally:
            forbindelse.close()

# Eksempel på brug
if __name__ == "__main__":
    # Initialiser DatabaseHandler med databasenavn
    database = DatabaseHandler("manufacturing.db")

    # Opret tabellen 'print_history'
    database.opret_print_history_tabel()










