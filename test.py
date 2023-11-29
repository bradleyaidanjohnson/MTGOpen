import sqlite3
con = sqlite3.connect("mtgopen.db")
db = con.cursor()
players = (1,2)
gameType = "Standard"
db.execute("INSERT INTO games (player0) VALUES(?)", (players[0],))
con.commit()
gameID =  db.lastrowid
print(type(gameID))