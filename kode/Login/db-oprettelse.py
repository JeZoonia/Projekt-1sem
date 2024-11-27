import sqlite3





connection = sqlite3.connect("adgang.db")
con = connection.cursor()


try: 
    con.execute("CREATE TABLE bruger(brugernavn, adgangskode, type_id)")
    con.execute("CREATE TABLE type(type_id, type_navn)")

except:
    print("allerede oprettet")


try: 
    con.execute("""INSERT INTO bruger VALUES 
                ('Admin', "123", 1),
                ("Casper", "123", 2)""")
    
    con.execute(""" INSERT INTO type VALUES
                (1, "admin"),
                (2, "standard")""")
    connection.commit()

except:
    print ("brugere tilføjet")