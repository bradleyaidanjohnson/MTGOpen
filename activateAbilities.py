import sqlite3

con = sqlite3.connect("mtgopen.db")
con.row_factory = sqlite3.Row
db = con.cursor()

def CheckForActivatedAbility(**kwargs):
    data = [kwargs['id']]
    priorityIndex = (db.execute("SELECT priority FROM games JOIN ingamecards ON ingamecards.game_id=games.id WHERE ingamecards.id=?", data)).fetchone()[0]
    data = [kwargs['id']]
    cardInfo = (db.execute("SELECT * FROM ingamecards JOIN cards ON ingamecards.printed_id=cards.Nid JOIN games ON ingamecards.game_id=games.id JOIN users on users.id=games.player" + str(priorityIndex) + " WHERE ingamecards.id=?", data)).fetchone()

    abilityString = str(cardInfo["Nability"])
    abilities = []
    
    start = 0
    end = 0
    while True:
        newLineIndex = abilityString.find('£',start)
        if  newLineIndex == -1:
            abilities.append(abilityString[start:])
            break
        else:
            end = newLineIndex
            abilities.append(abilityString[start:end])
            start = end + 1

    # print(abilities)
    activatedAbilityPresent = False
    activatedAbilities = []

    for ability in abilities:
        if ability.find(':') >= 0:
            activatedAbilityPresent = True
            activatedAbilities.append(ability)
        
    if activatedAbilityPresent:
        while True:
            print(f"Pick an ability card: ")
            for y in range(len(activatedAbilities)):
                actAbilString = activatedAbilities[y]
                print(f"{(y + 1)}: {actAbilString}")
            print("Or P to cancel.")
            answer = input(f"Pick an option:")
            if answer == 'p':
                break
            chosenAbility = int(answer) - 1
            print(chosenAbility)
            break

    

    if "Basic" in cardInfo["Ntype"]:
        BasicLand(cardInfo, kwargs['destID'])
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
        data = [cardInfo["game_id"], cardInfo["priority"], cardInfo["Ngenerated_mana"], cardInfo["id"], destID]
        db.execute("INSERT INTO mana_pool (game_id, player_index, mana, source_ingamecard_id, dest_ingamecard_id) VALUES (?,?,?,?,?)", data)
        con.commit()
        print("Card tapped for mana")

# CheckForActivatedAbility(1,1,1)