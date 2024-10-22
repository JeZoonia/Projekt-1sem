import matplotlib.pyplot as plt
import numpy as np

def plot_pris_per_print(total_pris, max_antal_print):
    """
    Plotter prisen pr. print som funktion af antallet af print.
    
    Args:
    total_pris (float): Den samlede pris for en batch print.
    max_antal_print (int): Det maksimale antal print, vi vil plotte for.
    """
    
    if max_antal_print <= 0:
        print("Antal print skal være større end nul.")
        return
    
    # Opret en række af print fra 1 til max_antal_print
    x = np.arange(1, max_antal_print + 1)
    
    # Beregn prisen pr. print for hvert x (pris pr. print = total_pris / x)
    y = total_pris / x
    
    # Plot grafen
    plt.plot(x, y, label="Pris pr. print")
    
    # Tilføj labels og titel
    plt.title("Pris pr. print som funktion af antal print")
    plt.xlabel("Antal print (x)")
    plt.ylabel("Pris pr. print (DKK)")
    
    # Tilføj et gitter og en legend
    plt.grid(True)
    plt.legend()
    
    # Vis grafen
    plt.show()

# Inputs fra brugeren
total_pris = float(input("Indtast den samlede pris for en batch print (i DKK): "))
max_antal_print = int(input("Indtast det maksimale antal print du vil plotte for: "))

# Kald funktionen for at plotte grafen
plot_pris_per_print(total_pris, max_antal_print)
