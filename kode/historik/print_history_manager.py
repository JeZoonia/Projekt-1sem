import sqlite3
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from tkinter import ttk

class DatabaseHandler:
    def __init__(self, database_navn):
        """Initialiserer databaseforbindelsen."""
        self.database_navn = database_navn

    def opret_forbindelse(self):
        """Opretter og returnerer en forbindelse til databasen."""
        return sqlite3.connect(self.database_navn)

    def hent_print_historik(self):
        """Henter print historik fra databasen."""
        query = "SELECT * FROM print_history"
        forbindelse = self.opret_forbindelse()
        cursor = forbindelse.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        forbindelse.close()
        return records

    def opdater_print_historik(self, print_id, ny_mængde):
        """Opdaterer kun mængde i print historikken."""
        query = """
        UPDATE print_history
        SET mængde = ?
        WHERE PrintID = ?
        """
        forbindelse = self.opret_forbindelse()
        cursor = forbindelse.cursor()
        cursor.execute(query, (ny_mængde, print_id))
        forbindelse.commit()
        forbindelse.close()

class PrintHistoryApp:
    def __init__(self, root, db_handler):
        self.root = root
        self.db_handler = db_handler
        self.root.title("Print Historik")
        self.root.geometry("800x600")

        # Mørkt tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Treeview for at vise tabellen med den rigtige rækkefølge af kolonner
        self.tree = ttk.Treeview(self.root, columns=("PrintID", "Mængde", "Filnavn", "Print Varighed", "Print Dato", "Samlet Omkostning", "Status", "Maskine ID", "Materiale ID"), show="headings")
        self.tree.heading("PrintID", text="PrintID")
        self.tree.heading("Mængde", text="Mængde")
        self.tree.heading("Filnavn", text="Filnavn")
        self.tree.heading("Print Varighed", text="Print Varighed")
        self.tree.heading("Print Dato", text="Print Dato")
        self.tree.heading("Samlet Omkostning", text="Samlet Omkostning")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Maskine ID", text="Maskine ID")
        self.tree.heading("Materiale ID", text="Materiale ID")

        self.tree.pack(pady=20, padx=20, expand=True, fill="both")

        # Knappen til at opdatere og reprint
        self.rediger_knap = ctk.CTkButton(self.root, text="Rediger", command=self.rediger_post)
        self.rediger_knap.pack(pady=10)

        self.annuller_knap = ctk.CTkButton(self.root, text="Annuller", command=self.annuller_redigering)
        self.annuller_knap.pack(pady=10)

        self.reprint_knap = ctk.CTkButton(self.root, text="Reprint", command=self.reprint_post)
        self.reprint_knap.pack(pady=10)

        # Indlæs print-historik
        self.load_print_history()

    def load_print_history(self):
        """Indlæser print historik i Treeview."""
        records = self.db_handler.hent_print_historik()

        # Ryd Treeview før indlæsning af nye data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Tilføj hver række til Treeview med den korrekte rækkefølge af kolonner
        for record in records:
            try:
                # Tilføj data til Treeview, men kun hvis der er nok data i record
                self.tree.insert("", "end", values=(
                    record[0],  # PrintID
                    record[7],  # Mængde
                    record[2],  # Filnavn
                    record[3],  # Print Varighed
                    record[4],  # Print Dato
                    record[5],  # Samlet Omkostning
                    record[6],  # Status
                    record[1],  # Maskine ID
                    record[8] if len(record) > 8 else "N/A"   # Materiale ID (hvis findes)
                ))
            except IndexError:
                messagebox.showerror("Fejl", f"Datafejl ved indlæsning af post: {record}")

    def rediger_post(self):
        """Rediger kun mængde i databasen."""
        try:
            selected_item = self.tree.selection()[0]  # Få den valgte række
            print_id = int(self.tree.item(selected_item, "values")[0])  # Få PrintID for den valgte række

            # Brug Tkinter simpledialog for at få ny mængde
            ny_mængde = simpledialog.askinteger("Rediger mængde", "Indtast ny mængde:")

            if ny_mængde is not None:  # Hvis brugeren indtaster noget
                # Opdater mængde i databasen
                self.db_handler.opdater_print_historik(print_id, ny_mængde)
                messagebox.showinfo("Succes", "Mængden blev opdateret!")
                self.load_print_history()  # Genindlæs historikken
            else:
                messagebox.showwarning("Fejl", "Mængden skal udfyldes!")

        except Exception as e:
            messagebox.showerror("Fejl", f"Noget gik galt: {e}")

    def reprint_post(self):
        """Reprint en post."""
        try:
            selected_item = self.tree.selection()[0]  # Få den valgte række
            print_id = int(self.tree.item(selected_item, "values")[0])  # Få PrintID for den valgte række
            print("Reprint af post med PrintID:", print_id)
            # Du kan tilføje funktionalitet til at reprint her, f.eks. sende data til printeren
            messagebox.showinfo("Succes", f"Post med PrintID {print_id} blev reprintet!")
        except Exception as e:
            messagebox.showerror("Fejl", f"Noget gik galt: {e}")

    def annuller_redigering(self):
        """Funktion til at annullere redigering."""
        messagebox.showinfo("Annulleret", "Redigering blev annulleret!")

# Eksempel på brug
if __name__ == "__main__":
    root = ctk.CTk()
    database = DatabaseHandler("manufacturing.db")
    app = PrintHistoryApp(root, database)
    root.mainloop()













