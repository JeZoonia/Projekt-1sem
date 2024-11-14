import sqlite3

connection = sqlite3.connect("ntb.db")
con = connection.cursor()

b = con.execute("SELECT * FROM bruger")
print(b)
#try:
   # con.execute("INSERT INTO bruger VALUES ('casper02', 'cas02')")
   # connection.commit()


#except Exception as e:
#    print(f'Fejl ved indsættelse af data: {e}')