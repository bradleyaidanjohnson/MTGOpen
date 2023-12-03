import sqlite3

con = sqlite3.connect("mtgopen.db")
con.row_factory = sqlite3.Row
db = con.cursor()

def CheckForActivatedAbility(id, playerIndex, destID):
    print("debug04")
    data = [id]
    priorityIndex = (db.execute("SELECT priority FROM games JOIN ingamecards ON ingamecards.game=games.id WHERE ingamecards.id=?", data)).fetchone()[0]
    data = [id]
    cardInfo = (db.execute("SELECT * FROM ingamecards JOIN cards ON ingamecards.printed_id=cards.Nid JOIN games ON ingamecards.game=games.id JOIN users on users.id=games.player" + str(priorityIndex) + " WHERE ingamecards.id=?", data)).fetchone()

    # "(SELECT priority FROM games WHERE id=?) CASE WHEN '0' THEN player0 WHEN '1' THEN player1 WHEN '2' THEN player2 WHEN '3' THEN player3 WHEN '4' THEN player4 WHEN '5' THEN player5"

    if "Basic" in cardInfo["Ntype"]:
        BasicLand(cardInfo, destID)
        return True
    else:
        return False


def BasicLand(cardInfo, destID):
    if cardInfo["tapped"] == 1:
        print("Land is tapped")
        if manaEventExists():
            UndoMana()
            print("Land Untapped")
            return
        else:
            print("Land cannot be untapped")
        return
    else:
        data = [cardInfo["id"]]
        db.execute("UPDATE ingamecards SET tapped=1 WHERE id=?", data)
        data = [cardInfo["game"], cardInfo["priority"], cardInfo["Ngenerated_mana"], cardInfo["id"], destID]
        db.execute("INSERT INTO mana_pool (game_id, player_index, mana, source_ingamecard_id, dest_ingamecard_id) VALUES (?,?,?,?,?)", data)
        con.commit()
        print("Card tapped for mana")

# CheckForActivatedAbility(1,1,1)