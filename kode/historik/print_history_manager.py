import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class DatabaseHandler:
    def __init__(self, database_name):
        """Initialiserer databaseforbindelsen."""
        self.database_name = database_name

    def opret_forbindelse(self):
        """Opretter og returnerer en forbindelse til databasen."""
        return sqlite3.connect(self.database_name)

    def hent_print_history(self):
        """Henter print historik fra databasen."""
        query = "SELECT * FROM print_history"
        forbindelse = self.opret_forbindelse()
        cursor = forbindelse.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        forbindelse.close()
        return records

    def opdater_print_history(self, print_id, new_file_name, new_quantity, new_total_cost):
        """Opdaterer print historikken."""
        query = """
        UPDATE print_history
        SET file_name = ?, quantity = ?, total_cost = ?
        WHERE id = ?
        """
        forbindelse = self.opret_forbindelse()
        cursor = forbindelse.cursor()
        cursor.execute(query, (new_file_name, new_quantity, new_total_cost, print_id))
        forbindelse.commit()
        forbindelse.close()


class PrintHistoryApp:
    def __init__(self, root, db_handler):
        self.root = root
        self.db_handler = db_handler
        self.root.title("Print History")
        self.root.geometry("800x600")

        # Mørkt tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Treeview for at vise tabellen
        self.tree = ttk.Treeview(self.root, columns=("ID", "Print Date", "File Name", "Quantity", "Material ID", "Machine ID", "Total Cost"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Print Date", text="Print Date")
        self.tree.heading("File Name", text="File Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Material ID", text="Material ID")
        self.tree.heading("Machine ID", text="Machine ID")
        self.tree.heading("Total Cost", text="Total Cost")
        
        self.tree.pack(pady=20, padx=20, expand=True, fill="both")

        # Knappen til at opdatere og reprint
        self.edit_button = ctk.CTkButton(self.root, text="Rediger", command=self.rediger_post)
        self.edit_button.pack(pady=10)

        self.reprint_button = ctk.CTkButton(self.root, text="Reprint", command=self.reprint_post)
        self.reprint_button.pack(pady=10)

        # Indlæs print-historik
        self.load_print_history()

    def load_print_history(self):
        """Indlæser print historik i Treeview."""
        records = self.db_handler.hent_print_history()
        for record in records:
            self.tree.insert("", "end", values=record)

    def rediger_post(self):
        """Rediger en post i databasen."""
        try:
            selected_item = self.tree.selection()[0]  # Få den valgte række
            print_id = int(self.tree.item(selected_item, "values")[0])  # Få ID'et for den valgte række

            # Indtast oplysninger til opdatering
            new_file_name = input("Indtast nyt filnavn: ")
            new_quantity = int(input("Indtast ny mængde: "))
            new_total_cost = float(input("Indtast ny samlet omkostning: "))
            
            # Opdater post
            self.db_handler.opdater_print_history(print_id, new_file_name, new_quantity, new_total_cost)
            messagebox.showinfo("Succes", "Posten blev opdateret!")
            self.tree.delete(selected_item)  # Fjern den gamle række
            self.load_print_history()  # Genindlæs historikken
        except Exception as e:
            messagebox.showerror("Fejl", f"Noget gik galt: {e}")

    def reprint_post(self):
        """Reprint en post."""
        try:
            selected_item = self.tree.selection()[0]  # Få den valgte række
            print_id = int(self.tree.item(selected_item, "values")[0])  # Få ID'et for den valgte række
            print("Reprint af post med ID:", print_id)
            # Du kan tilføje funktionalitet til at reprint her, f.eks. sende data til printeren
            messagebox.showinfo("Succes", f"Post med ID {print_id} blev reprintet!")
        except Exception as e:
            messagebox.showerror("Fejl", f"Noget gik galt: {e}")


# Eksempel på brug
if __name__ == "__main__":
    root = ctk.CTk()
    database = DatabaseHandler("manufacturing.db")
    app = PrintHistoryApp(root, database)
    root.mainloop()



