import sqlite3

class DatabaseHandler:
    def __init__(self, database_navn):
        """Initialiserer databaseforbindelsen."""
        self.database_navn = database_navn

    def opret_forbindelse(self):
        """Opretter og returnerer en forbindelse til databasen."""
        return sqlite3.connect(self.database_navn)

    def opret_print_history_tabel(self):
        """Opretter 'print_history' tabellen med den korrekte struktur, herunder 'mængde' kolonne."""
        opret_tabel_query = """
        CREATE TABLE IF NOT EXISTS print_history (
             PrintID INTEGER PRIMARY KEY AUTOINCREMENT,
            print_dato TEXT NOT NULL,
            filnavn TEXT NOT NULL,
            mængde INTEGER NOT NULL,
            materiale_id INTEGER NOT NULL,
            maskine_id INTEGER NOT NULL,
            samlet_omkostning REAL NOT NULL,
            print_varighed TEXT,
            status TEXT,
            FOREIGN KEY (materiale_id) REFERENCES materialer(materiale_id),
            FOREIGN KEY (maskine_id) REFERENCES maskiner(maskine_id)
        );
        """
        try:
            forbindelse = self.opret_forbindelse()
            cursor = forbindelse.cursor()
            cursor.execute(opret_tabel_query)
            forbindelse.commit()
            print("Tabellen 'print_history' blev oprettet eller opdateret succesfuldt.")
        except Exception as e:
            print(f"Fejl ved oprettelse af tabellen: {e}")
        finally:
            forbindelse.close()

# Eksempel på brug
if __name__ == "__main__":
    # Initialiser DatabaseHandler med databasenavn
    database = DatabaseHandler("manufacturing.db")

    # Opret tabellen 'print_history' med den korrekte struktur
    database.opret_print_history_tabel()

