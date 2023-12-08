import sqlite3
import random
import re
import string
import activateAbilities
from EntersTheBattlefield import *

con = sqlite3.connect("mtgopen.db")
con.row_factory = sqlite3.Row
db = con.cursor()

def GetLibraryIDs(gameID, playerIndex):
    data = [gameID, playerIndex]
    library = (db.execute("SELECT id FROM ingamecards WHERE game_id=? AND location='library' AND owner=? ORDER BY position;", data)).fetchall()
    libraryList = []
    for card in library:
        libraryList.append(card[0])
    return libraryList
        
def GetHandIDs(gameID, playerIndex):
    data = [gameID, playerIndex]
    hand = (db.execute("SELECT id FROM ingamecards WHERE game_id=? AND location='hand' AND owner=?;", data)).fetchall()
    handList = []
    for card in hand:
        handList.append(card[0])
    return handList

def GetBattlefieldIDs(gameID, playerIndex):
    data = [gameID, playerIndex]
    battlefield = (db.execute("SELECT id FROM ingamecards WHERE game_id=? AND location='battlefield' AND owner=?;", data)).fetchall()
    battlefieldList = []
    for card in battlefield:
        battlefieldList.append(card[0])
    return battlefieldList

def GetManaSources(gameID, playerIndex):
    data = [gameID, playerIndex]
    manaSources = (db.execute("SELECT id FROM ingamecards JOIN cards ON ingamecards.printed_id=cards.Nid WHERE game_id=? AND location='battlefield' AND owner=? AND Ngenerated_mana IS NOT NULL;", data)).fetchall()
    manaSourcesList = []
    for card in manaSources:
        manaSourcesList.append(card[0])
    return manaSourcesList

def UndoTempTaps(id):
    print("insert UndoTempTaps code here")
    return    

def IngameCardIDToName(id):
    data = [id]
    name = (db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printed_id WHERE ingamecards.id=?;", data)).fetchone()[0]
    return name

def IngameCardIDToObject(id):
    data = [id]
    cardObject = (db.execute("SELECT * FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printed_id WHERE ingamecards.id=?;", data)).fetchall()[0]
    return cardObject

def IngameCardIDToCostString(id):
    data = [id]
    costString = (db.execute("SELECT Nmana_cost FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printed_id WHERE ingamecards.id=?;", data)).fetchone()[0]
    return costString

def EntersTheBattlefield(gameID):
    data = [gameID]
    cardDetails = (db.execute("SELECT * FROM ingamecards JOIN cards ON ingamecards.printed_id=cards.Nid WHERE ingamecards.id=?", data).fetchall())[0]
    if 'Creature' in cardDetails['Ntype']:
        print("creature etb")
    elif 'Land' in cardDetails['Ntype']:
        print("land etb")

    strinngNew = cardDetails['Nname']
    pattern = re.compile('[\W_]+')
    strinngNew = pattern.sub('', strinngNew)

    print(strinngNew)
    
    r = getattr(EntersTheBattlefield, strinngNew)
    r(gameID=gameID, id=cardDetails['id'])
    
def TappedCheck(cardIndex):
    data = [cardIndex]
    if (db.execute("SELECT tapped FROM ingamecards WHERE id=?", data)).fetchone()[0] ==0:
        return False
    else:
        return True

def TapLand(id, playerIndex, destID):
    if activateAbilities.CheckForActivatedAbility(id=id, playerIndex=playerIndex, destID=destID):
        return True
    else:
        return False
            
def UntapLand(id, playerIndex):
    if activateAbilities.CheckForActivatedAbility(id, playerIndex):
        return True
    else:
        return False

def MoveCard(id, destString, positionINT, tapped, facedown):
    data = [destString, positionINT, tapped, facedown, id]
    db.execute("UPDATE ingamecards SET location=?, position=?, tapped=?, face_down=? WHERE id=?", data)
    con.commit()

def DiscardHandToGraveyard(id):
    data = [gameID]
    graveyardPosition = int((db.execute("SELECT position FROM ingamecards WHERE game_id=?", data)).fetchone()[0])
    data = [(graveyardPosition + 1), id]
    db.execute("UPDATE ingamecards SET location='graveyard', position=?, face_down=0 WHERE id=?", data)
    con.commit()
    
def StartingLife(gameID, format, players):
    # set life
    life = 20
    if format=="Standard":
        for x in range(len(players)):
            data = [life, gameID]
            db.execute("UPDATE games SET life" + str(x) + "=? WHERE id=?;", data)

    con.commit()

def ShuffleLibrary(gameID, playerIndex):
    data = [gameID, playerIndex]
    rows = db.execute("SELECT COUNT(*) FROM ingamecards WHERE game_id=? AND location='library' AND owner=?;", data)
    rows = rows.fetchone()[0]

    randomNumbers = random.sample(range(rows), rows)
    data = [gameID, playerIndex]
    for row in (db.execute("SELECT id FROM ingamecards WHERE game_id=? AND location='library' AND owner=?;", data)).fetchall():
        data = [randomNumbers.pop(), row[0]]
        db.execute("UPDATE ingamecards SET position=? WHERE id=?;", data)
    con.commit()

def DrawLibraryHand(gameID, playerIndex, drawSize):
    data = [playerIndex, playerIndex, gameID, drawSize]
    db.execute("UPDATE ingamecards SET position='', location='hand', controller=? WHERE owner=? AND game_id=? AND location='library' ORDER BY position DESC LIMIT ?;", data)
    con.commit()

def HandToLibraryAll(gameID, playerIndex):
    data = [gameID, playerIndex]
    hand = (db.execute("SELECT id FROM ingamecards WHERE game_id=? AND (location='hand' OR location='library') AND owner=?;", data)).fetchall()
    randomNumbers = random.sample(range(len(hand)), len(hand))
    for card in hand:
        data = [randomNumbers.pop(), card[0]]
        db.execute("UPDATE ingamecards SET position=?, location='library' WHERE id=?;", data)
    con.commit()

def PrintHands(gameID, playerIndex):
    data = [playerIndex, gameID]
    hand = (db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printed_id WHERE ingamecards.location='hand' AND controller=? AND game_id=?;", data)).fetchall()
    for card in hand:
        print(card[0])

def Action(gameID, playerIndex):
    while True:
        try:
            answer = str(input(f"{playerNames[playerIndex]}: you have priority:\nH: Play a card from your Hand.\nB: Interact with a card on the Battlefield.\nP: Pass Priority.\nWhat would you like to do?\n"))
        except ValueError:
            print("Invalid response: please enter a letter")
            continue
        if answer == 'p':
            break
        elif answer == "h":
            PlayCardHand(playerIndex)
            continue
        elif answer == "b":
            BattlefieldInteraction(playerIndex)
            continue
        else:
            print("Invalid response: please choose one of the options")
            continue

def BattlefieldInteraction(playerIndex):
    # get hand int a list
    battlefield = GetBattlefieldIDs(gameID, playerIndex)
    while True:
        print(f"Pick a card: ")
        for y in range(len(battlefield)):
            name = IngameCardIDToName(battlefield[y])
            if TappedCheck(battlefield[y]):
                print(f"{(y + 1)}: {name} (Tapped)")
            else:
                print(f"{(y + 1)}: {name} (Untapped)")
        print("Or P to cancel.")
        answer = input(f"Pick an option:")
        if answer == 'p':
            break
        chosenInGameCardID = battlefield[int(answer) - 1]
        if ActivateAbility(chosenInGameCardID, playerIndex):
            break
        else:
            print("Nothing happened, please pick again")
            continue
        return
        
def PlayCardHand(playerIndex):
    # get hand int a list
    hand = GetHandIDs(gameID, playerIndex)
    while True:
        print(f"Pick a card: ")
        for y in range(len(hand)):
            name = IngameCardIDToName(hand[y])
            print(f"{(y + 1)}: {name}")
        print("Or P to cancel.")
        answer = input(f"Pick an option:")
        if answer == 'p':
            break
        chosenInGameCardID = hand[int(answer) - 1]
        if PlayCard(chosenInGameCardID, playerIndex):
            break
        else:
            print("Card was not played, please pick again")
            continue
        
def ActivateAbility(chosenInGameCardID, playerIndex):
    if activateAbilities.CheckForActivatedAbility(id=chosenInGameCardID, playerIndex=playerIndex):
        return True
    else:
        return False              

def PlayCard(id, playerIndex):
    # get card type
    # ADD COLUMN TO INGAMECARDS CALLED TYPE WHERE YOU CAN CHECK IF ANY TYPE CHANGES HAVE OCCURED CHECK THAT BEFORE YOU RUN THE PRINTED CARDS TYPE, IF NOT RUN THE PRINTED CARDS TYPE
    data = [id]
    cardType = (db.execute("SELECT Ntype from cards JOIN ingamecards ON cards.Nid=ingamecards.printed_id WHERE ingamecards.id=?", data)).fetchone()[0]
    if "Land" in cardType:
        data = [gameID]
        land = (db.execute("SELECT land FROM games WHERE id=?", data)).fetchone()[0]
        if land > 0:
            # change land location from hand to battlefield and tapped to 0
            data = [id]
            db.execute("UPDATE ingamecards SET location='battlefield', tapped=0, face_down=0 WHERE id=?", data)
            EntersTheBattlefield(id)
            land -= 1
            data = [land, gameID]
            db.execute("UPDATE games SET land = ? WHERE id=?;", data)
            con.commit()
            print("Card played")
            return True
        else:
            print("You cannot play anymore lands this turn.")
            return False
    elif "Creature" in cardType:
        if PayMana(id, playerIndex):
            if CastSpell(id, playerIndex):
                return True
            else:
                return False
        else:
            if PayCardCost(id, playerIndex):
                # CastSpell(id)
                data = [id]
                db.execute("UPDATE ingamecards SET location='battlefield', tapped=0, face_down=0 WHERE id=?", data)
                return True
            else:
                return False

def CastSpell(id, playerIndex):
    # Place on top of the stack (copy)
    stackTopIndex = GetStackTopIndex(gameID)
    if stackTopIndex == None:
        data = [id, gameID, playerIndex, 0]
        db.execute("INSERT INTO stacks (ingamecard_id,game_id,owner_id,position) VALUES(?,?,?,?);", data)
    else:
        data = [id, gameID, playerIndex, (stackTopIndex + 1)]
        db.execute("INSERT INTO stacks (ingamecard_id,game_id,owner_id,position) VALUES(?,?,?,?);", data)
    stackID = db.lastrowid
    con.commit()
    # Pass priority till it returns true or false
    PriorityLoop()
    # Remove from the stack
    if GetStackTopIndex(gameID) == stackID:
        data = [stackID]
        db.execute("DELETE FROM stacks WHERE id=?", data)
        con.commit()
        # Move "physical" card to battlefield or graveyard or hand or wherever
        # MoveCard(id, "battlefield", '',0,0)
        data = [id]
        db.execute("UPDATE ingamecards SET location='battlefield', tapped=0, face_down=0, sum_sick=1 WHERE id=?", data)
        EntersTheBattlefield(id)
        # return bool
        return True
    else:
        print("Card countered or something")
        return False

def GetStackTopIndex(gameID):
        data = [gameID]
        index = (db.execute("SELECT id FROM stacks WHERE game_id=? ORDER BY position DESC LIMIT 1", data)).fetchone()
        if index != None:
            index = index[0]
        return index
    
def PayMana(id, playerIndex):
    # manaSources = GetManaSources(gameID, playerIndex)
    while True:
        
        data = [gameID, playerIndex, id]
        manaPoolDB = (db.execute("SELECT mana FROM mana_pool WHERE game_id=? AND player_index=? AND (dest_ingamecard_id IS NULL OR dest_ingamecard_id=?) AND (spent IS NULL OR spent=0)", data)).fetchall()

        name = IngameCardIDToName(id)
        manaString = IngameCardIDToCostString(id)
        # Compare price to pool
        while True:
            for x in range(len(manaPoolDB)):
                if manaString[len(manaString) - 3:] in manaPoolDB[x]:
                    manaString = re.sub(manaString[len(manaString) - 3:],'',manaString)
                    manaPoolDB.pop(x)
                    if not manaString:
                        return True
                    continue
            break
        
        manaSources = GetManaSources(gameID, playerIndex)
        print(f"To cast {name} you need to pay {manaString}\nTap lands for mana:")
        for y in range(len(manaSources)):
            cardObject = IngameCardIDToObject(manaSources[y])
            if cardObject['tapped'] == 0:
                print(f"{(y + 1)}: {cardObject['Nname']} (Untapped)")
            else:
                print(f"{(y + 1)}: {cardObject['Nname']} (Tapped)")
        print("Or C to cancel.")
        answer = input(f"Pick an option:")
        if answer == 'c':
            UndoTempTaps(id)
            break
        chosenInGameCardID = manaSources[int(answer) - 1]
        if TapLand(chosenInGameCardID, playerIndex, id):
            continue
        else:
            print("Card was not played, please pick again")
            continue
        
    print("erm")
"""
    # this needs to be a loop through tuples
    canCast = False
    availableMana = GetAvailableMana(playerIndex)
    castCost = GetCastCost(id)
    while True:
        if availableMana['SW'] > 0:
            if castCost['SW'] > 0:
                castCost.update({'SW':(castCost['SW'] - availableMana['SW'])})

        if GetCastCost(id) <= GetAvailableMana(playerIndex):
            return True
        else:
            return False
"""        
def GetCastCost(id):
    castCosts = {'W':0, 'U':0, 'B':0, 'R':0, 'G':0, 'C':0,'UB':0, 'BR':0,'RG':0,'GW':0,'WB':0,'UR':0,'BG':0,'RW':0,'GU':0,'2W':0,'2U':0,'2B':0,'2R':0,'2G':0,'PW':0, 'PU':0, 'PB':0, 'PR':0, 'PG':0, 'PGU':0, 'PRG':0, 'PRW':0, 'PGW':0, 'S':0}
    xInstances = 0
    data = [id]
    castCostsString = (db.execute("SELECT Nmana_cost FROM cards JOIN ingamecards ON cards.Nid=ingamecards.printed_id WHERE ingamecards.id=?", data)).fetchone()[0]
    for x in range(len(castCostsString)):
        if castCostsString[x] == '{':
            if castCostsString[x + 1] == 'W' and castCostsString[x + 2] == '}':
                castCosts.update({'W':(castCosts['W'] + 1)})
            elif castCostsString[x + 1] == 'U' and castCostsString[x + 2] == '}':
                castCosts.update({'U':(castCosts['U'] + 1)})
            elif castCostsString[x + 1] == 'B' and castCostsString[x + 2] == '}':
                castCosts.update({'B':(castCosts['B'] + 1)})
            elif castCostsString[x + 1] == 'R' and castCostsString[x + 2] == '}':
                castCosts.update({'R':(castCosts['R'] + 1)})
            elif castCostsString[x + 1] == 'G' and castCostsString[x + 2] == '}':
                castCosts.update({'G':(castCosts['G'] + 1)})
            elif castCostsString[x + 1] == 'X' and castCostsString[x + 2] == '}':
                xInstances += 1
            elif castCostsString[x + 1].isdigit() and castCostsString[x + 2] == '}':
                castCosts.update({'?':(castCosts['C'] + int(castCostsString[x + 1]))})
    if xInstances > 0:
        xValue = GetXCastValue(id)
        xCost = xValue * xInstances
        castCosts.update({'C':(castCosts['C'] + xCost)})
    print(castCosts)
    return castCosts

def GetXCastValue(id):
    cardName = IngameCardIDToName(id)
    while True:
        try:
            xCastValue = int(input(f"X value for {cardName}?"))
        except ValueError:
            print("Invalid response: please enter a number")
            continue
        if xCastValue < 0:
            print("Invalid response: please enter a value greater than 0")
            continue
        else:
            break
    return xCastValue
        
def GetAvailableMana(playerIndex):
    manaPoolDict = {'W':0, 'U':0, 'B':0, 'R':0, 'G':0, 'C':0, 'SW':0, 'SU':0, 'SB':0, 'SR':0, 'SG':0, 'SC':0}
    data = [gameID,playerIndex]
    manaPoolDB = (db.execute("SELECT mana FROM mana WHERE game_id=? AND player_index=?", data)).fetchall()
    for item in manaPoolDB:
        print(item)
    if manaPoolDB is not None:
        for x in range(len(manaPoolDB)):
            if 'W' in manaPoolDB[x]:
                manaPoolDict.update({'W':(manaPoolDict['W'])})

            # NOT WORKIUNG
            # SOME MAGIC TO EXTRACT A READABLE MANA DICT
        

        print("Thar be Mana")
    else:
        print("no mana in pool")
    return manaPoolDict
        
def PriorityLoop():
    data = [gameID]
    priorityIndex = (db.execute("SELECT priority FROM games WHERE id=?;", data)).fetchone()[0]
    firstPriority = priorityIndex
    data = [gameID]
    topOfTheStack = (db.execute("SELECT * FROM stacks WHERE id=? LIMIT 1;", data)).fetchone()
    topStackOwner = ''
    if topOfTheStack != None:
        topStackOwner = topOfTheStack['owner_id']
    
    while True:
        if passPriority[priorityIndex] == False:
            Action(gameID, players[priorityIndex])
        if priorityIndex == len(players) - 1:
            priorityIndex = 0
        else:
            priorityIndex = priorityIndex + 1
        data = [priorityIndex, gameID]
        db.execute("UPDATE games SET priority=? WHERE id=?;", data)
        con.commit()
        if players[priorityIndex] == topStackOwner:
            break
        if priorityIndex == firstPriority:
            break

def ActivePriority():   
    x = activePlayerIndex
    while True:
        if passActivePriority[activePlayerIndex] == False and x == activePlayerIndex:
            Action(gameID, x)
        elif passPriority[x] == False:
            Action(gameID, x)
        if x == len(players) - 1:
            x = 0
        else:
            x += 1
        data = [x, gameID]
        db.execute("UPDATE games SET priority=? WHERE id=?;", data)
        con.commit()
        if x == activePlayerIndex:
            break
        

def DrainManaPools(gameID, phaseInt):
    for x in range(6):
        data = [phaseInt, gameID, phaseInt]
        db.execute("UPDATE mana_pool SET dest_event_id=? WHERE game_id=? AND (dest_ingamecard_id IS null OR dest_ingamecard_id = '') AND (dest_event_id IS null OR dest_event_id = '') AND ((mana_drain IS null OR mana_drain = '') OR mana_drain=?)", data)
        con.commit()
    
def Mulligan(gameID, players):
    # 2 dicts for mulligan decisions/reprecusions
    playerMulliganDecision = {}
    playerBottoms = {}
    playerReady = {}
    for x in range(len(players)):
        playerMulliganDecision.update({x:True})
        playerBottoms.update({x:0})
        playerReady.update({x:False})
    anyMulligans = True

    while True:
        anyMulligans = False
        for x in range(len(players)):
            if playerMulliganDecision[x] == True and playerReady[x] == False:
                                # add code to show if other player(s) is(are) ready
                if x == startingPlayerIndex:
                    print("You go first")
                else:
                    print("Your opponent goes first")

                print(playerNames[x] + "'s draw:")
                data = [x, gameID]
                hand = db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printed_id WHERE ingamecards.location='hand' AND controller=? AND game_id=?;", data)
                handList = hand.fetchall()
                for card in handList:
                    print(card[0])
                    # print the turn order for them to decide on the mulligsn
                    # also inform them of the decisions of the other player(s) (Your opponent kept a hand of x cards)
                if playerBottoms[x] == 0:
                    answer = input(f"{playerNames[x]}: Will you keep your hand? (you will return {(playerBottoms[x] + 1)} card to the bottom of your library.)")
                else:
                    answer = input(f"{playerNames[x]}: Will you keep your hand? (you will return {(playerBottoms[x] + 1)} cards to the bottom of your library.)")
                if answer=='y' or playerBottoms[x] >= 6:
                    playerMulliganDecision.update({x:False})
                else:
                    playerMulliganDecision.update({x:True})
                    playerBottoms.update({x:(playerBottoms[x] + 1)})
        for x in range(len(players)):
            if playerMulliganDecision[x] == True:
                anyMulligans = True
                # put all cards back into deck, shuffle, then draw new hand
                HandToLibraryAll(gameID, x)
                ShuffleLibrary(gameID, x)
                DrawLibraryHand(gameID, x, 7)
            elif playerReady[x] == False:
                if playerBottoms[x] > 0:
                    # Get library into a list
                    library = GetLibraryIDs(gameID, x)
                    # get hand int a list
                    hand = GetHandIDs(gameID, x)
                    print(f"Put {playerBottoms[x]} cards on the bottom of your library: ")
                    for y in range(len(hand)):
                        name = IngameCardIDToName(hand[y])
                        print(f"{(y + 1)}: {name}")
                    bottomedCards = []
                    for y in range(playerBottoms[x]):
                        # place as many hand cards as needed into the library list at the 0 position and remove from the hand list

                        # CHECK TO MAKE SURE YOU DONT BOTTOM THE SAME CARD MULTIPLE TIMES

                        bottom = int(input(f"Card {y + 1}:"))
                        library.insert(0, hand.pop(bottom - 1))
                    # push the changes to the database
                    for y in range(len(library)):
                        data = [y, library[y]]
                        db.execute("UPDATE ingamecards SET location='library', position=? WHERE id=?;", data)
                    for card in hand:
                        data = [card]
                        db.execute("UPDATE ingamecards SET location='hand', position='' WHERE id=?;", data)
                    con.commit()
                playerReady[x] == True
        if not anyMulligans:
            break

def NextTurn(gameID):
    global activePlayerIndex
    if activePlayerIndex == len(players) - 1:
        activePlayerIndex = 0
    else:
        activePlayerIndex += 1
        
    data = [gameID]
    turnNumber = int((db.execute("SELECT turn_number FROM games WHERE id=?;", data)).fetchone()[0])
    data = [activePlayerIndex, (turnNumber + 1), gameID]
    print(turnNumber)
    db.execute("UPDATE games SET active=?, turn_number=? WHERE id=?;", data)
    BeginningPhase(gameID)
    
def BeginningPhase(gameID):
    # MAKE THIS A FUNCTION AT SOME POINT
    data = [gameID]
    db.execute("UPDATE games SET land= 1 WHERE id=?;", data)
    con.commit()

    UntapPhase(gameID)
    UpkeepPhase(gameID)
    DrawPhase(gameID)
    PreCombatMainPhase(gameID)

def EndingPhase(gameID):
    EndPhase(gameID)
    CleanupPhase(gameID)
    NextTurn(gameID)
    # print("成功!")

def EndPhase(gameID):
    # "At the beginning of the end step" or "At the beginning of the next end step" triggered abilities trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=52 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=53 WHERE id=?;", data)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=54 WHERE id=?;", data)
    DrainManaPools(gameID,56)

def CleanupPhase(gameID):
    # The active player discards down to his maximum hand size (usually seven).
    data = [gameID]
    db.execute("UPDATE games SET phase=55 WHERE id=?;", data)
    DiscardPhase(gameID, activePlayerIndex)
    # Simultaneously remove all damage from permanents and end all "until end of turn" or "this turn" effects.
    data = [gameID]
    db.execute("UPDATE games SET phase=56 WHERE id=?;", data)
    # Check for state-based actions and triggered abilities, such as those that trigger "at the beginning of the next cleanup step". A
    data = [gameID]
    db.execute("UPDATE games SET phase=57 WHERE id=?;", data)
    # If no state-based actions or triggered abilities occur, unused mana empties from each player's mana pool and the cleanup step ends.
    data = [gameID]
    db.execute("UPDATE games SET phase=58 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=59 WHERE id=?;", data)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=60 WHERE id=?;", data)
    DrainManaPools(gameID,62)
    # Repeat the cleanup step.

def DiscardPhase(gameID, playerIndex):
    while len(GetHandIDs(gameID, playerIndex)) > 7:
        hand = GetHandIDs(gameID, playerIndex)
        print(f"Discard to Hand Size: ")
        for y in range(len(hand)):
            name = IngameCardIDToName(hand[y])
            print(f"{(y + 1)}: {name}")
        answer = input(f"Pick an option:")
        chosenInGameCardID = hand[int(answer) - 1]
        DiscardHandToGraveyard(chosenInGameCardID)
    return
    
def PostCombatMainPhase(gameID):
    # pre combat main phasey things happen 
    data = [gameID]
    db.execute("UPDATE games SET phase=49 WHERE id=?;", data)
    con.commit()

    # land and sorcery speed spells can be played/cast
    data = [gameID]
    db.execute("UPDATE games SET phase=50 WHERE id=?;", data)
    con.commit()
    ActivePriority()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=51 WHERE id=?;", data)
    DrainManaPools(gameID,53)
    EndingPhase(gameID)

def CombatPhase(gameID):
    BeginningofCombatPhase(gameID)
    if DeclareAttackersPhase(gameID):
        DeclareBlockersPhase(gameID)
        CombatDamagePhase(gameID)
    EndOfCombatPhase(gameID)
    PostCombatMainPhase(gameID)

def BeginningofCombatPhase(gameID):
    # "At beginning of combat" triggered abilities trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=14 WHERE id=?;", data)
    con.commit()
    #     The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=15 WHERE id=?;", data)
    con.commit()
    PriorityLoop()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=16 WHERE id=?;", data)
    DrainManaPools(gameID,16)

def DeclareAttackersPhase(gameID):
    attackersDeclared = False
    # The active player declares his attackers. If no attackers are declared, the Declare Blockers and Combat Damage steps are skipped.
    data = [gameID]
    db.execute("UPDATE games SET phase=17 WHERE id=?;", data)
    if DeclareAttackers(gameID, activePlayerIndex):
        attackersDeclared = True

    # Triggered abilities that trigger off attackers being declared trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=18 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=19 WHERE id=?;", data)
    PriorityLoop()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=20 WHERE id=?;", data)
    DrainManaPools(gameID,20)
    return attackersDeclared

def DeclareAttackers(gameID, playerIndex):
    attackers = GetAttackReadyIDs(gameID, playerIndex)
    attackTargets = GetAttackTargets(gameID, playerIndex)
    print("Choose an creature who will attack:")
    while True:
        for x in range(len(attackers)):
            data = [attackers[x]]
            print(attackers[x])
            if not ((db.execute("SELECT COUNT(*) FROM attackers JOIN ingamecards ON ingamecards.id=attackers.ingamecard_id WHERE ingamecards.id=?", data)).fetchone())[0]:
                declared = False
            else:
                declared = True
                data = [attackers[x]]
            if declared:
                print(f"{x +1}: {IngameCardIDToName(attackers[x])} (Declared)")
            else:
                print(f"{x +1}: {IngameCardIDToName(attackers[x])} (Undeclared)")
        print("P to cancel all attacks")
        print("A to confirm attacks")
        answer = input("Please choose:")
        if answer == 'p':
            data = [gameID]
            db.execute("DELETE FROM attackers WHERE game_id=?", data)
            con.commit()
            break
        if answer == 'a':
            break
        else:
            # pick attack target code
            if len(attackTargets) == 1:
                data = [attackers[int(answer) - 1], gameID, attackTargets[0]]
                db.execute("INSERT INTO attackers (ingamecard_id, game_id, target) VALUES (?,?,?)", data)
                con.commit()
                continue
            else:
                # multiple attack choices code
                continue
    data = [gameID]
    if not (db.execute("SELECT COUNT(*) FROM attackers WHERE game_id=?", data)).fetchone()[0]:
        return False
    else:
        return True

def GetAttackReadyIDs(gameID, playerIndex):
    data =[gameID, playerIndex]
    attackReadyIDList = []
    attackReadyList = (db.execute("SELECT id FROM ingamecards JOIN cards ON cards.Nid=ingamecards.printed_id WHERE location='battlefield' AND Ntype LIKE '%Creature%' AND sum_sick=0 AND tapped=0 AND game_id=? AND controller=?", data).fetchall())
    for row in attackReadyList:
        attackReadyIDList.append(row['id'])
    return attackReadyIDList

def GetAttackTargets(gameID, playerIndex):
    data = [gameID, playerIndex]
    # attackTargetList = db.execute("SELECT id GOTTA THINKNABOUT THISNONE LOL")
    if playerIndex == 0:
        attackTargetList = [1]
    else:
        attackTargetList = [0]
    return attackTargetList


def DeclareBlockers(gameID):
    # NOT CURRENTLY FUNCTIONING FOR PLANESWALKERS NOT MULTIPLAYER
    beingAttacked = GetTargets(gameID)
    for x in range(len(beingAttacked)):
        blockers = GetBlockReady(gameID, beingAttacked[x])
        attackers = GetAttackers(gameID=gameID)
        print(attackers)
        print("Choose an creature who will block:")
        while True:
            for x in range(len(blockers)):
                data = [blockers[x]]
                if not (db.execute("SELECT COUNT(*) FROM blockers WHERE id=?", data).fetchone())[0]:
                    declared = False
                else:
                    declared = True
                    data = [blockers[x]]
                if declared:
                    print(f"{x +1}: {IngameCardIDToName(blockers[x])} (Declared)")
                else:
                    print(f"{x +1}: {IngameCardIDToName(blockers[x])} (Undeclared)")
            print("P to cancel all attacks")
            print("B to confirm blocks")
            answer = input("Please choose:")
            if answer == 'p':
                # NOT CURRRENTLY EXTENSIBLE TO MULTIPLAYER
                data = [gameID, beingAttacked[x]]
                db.execute("DELETE blockers WHERE game_id=?", data)
                break
            if answer == 'b':
                break
            data = [blockers[int(answer) - 1]]
            if not db.execute("SELECT COUNT(*) FROM blockers WHERE id=?", data).fetchone():
                # Cancel attack code
                data = [gameID, data]
                db.execute("DELETE blockers WHERE game_id=? AND id=?", data)
                continue
            else:
                # pick who to block code
                while True:
                    print("Who will they block?")
                    for x in range(len(attackers)):
                        print(f"{x + 1}: {IngameCardIDToName(attackers[x])}")
                    print("P to cancel all attacks")
                    answer2 = input("Please choose:")
                    if answer2 == 'p':
                        break
                    data = [blockers[int(answer) - 1], gameID, attackers[int(answer2) - 1]]
                    db.execute("INSERT INTO blockers (ingamecard_id, game_id, target) VALUES (?,?,?)", data)
                    con.commit()
                    break
                continue
    
def GetTargets(gameID):
    data = [gameID]
    targetList = (db.execute("SELECT target FROM attackers WHERE game_id=?", data).fetchall())
    playersString = ['0','1','2','3','4','5',]
    beingAttackedList = []
    for row in targetList:
        if row['target'] in playersString:
            beingAttackedList.append(int(row['target']))
    return beingAttackedList

def GetBlockReady(gameID, playerIndex):
    data =[gameID, playerIndex]
    blockReadyIDList = []
    blockReadyList = (db.execute("SELECT id FROM ingamecards JOIN cards ON cards.Nid=ingamecards.printed_id WHERE location='battlefield' AND Ntype LIKE '%Creature%' AND tapped=0 AND game_id=? AND controller=?", data).fetchall())
    for row in blockReadyList:
        blockReadyIDList.append(row['id'])
    return blockReadyIDList

def GetAttackers(**kwargs):
    # NOT CURRENTLY WORKING FOR PLANESWALKERS NOT MULTIPLAYER
    # make **kwargs so it works to get ALL attacking creature OR JUST the attacking creatures that 1 player may block
    blocked = kwargs.get('blocked', False)
    if not blocked:
        data =[kwargs['gameID']]
        attackerIDList = []
        attackerList = (db.execute("SELECT ingamecard_id FROM attackers WHERE game_id=?", data).fetchall())
        for row in attackerList:
            attackerIDList.append(row['ingamecard_id'])
        return attackerIDList
    
    else:
        data =[kwargs['gameID']]
        attackerIDList = []
        attackerList = (db.execute("SELECT attackers.ingamecard_id FROM attackers JOIN blockers ON blockers.target=attackers.ingamecard_id WHERE attackers.game_id=?", data).fetchall())
        for row in attackerList:
            attackerIDList.append(row['ingamecard_id'])
        return attackerIDList

def DeclareBlockersPhase(gameID):
    # The defending player declares his blockers and which attacking creatures they will block.
    data = [gameID]
    db.execute("UPDATE games SET phase=21 WHERE id=?;", data)
    DeclareBlockers(gameID)
    # For each attacking creature that has become blocked, the active player declares the order that combat damage will be assigned to blockers.
    data = [gameID]
    db.execute("UPDATE games SET phase=22 WHERE id=?;", data)
    ActiveDeclareDamageOrder()
    # For each blocking creature, the defending player declares the order that combat damage will be assigned to attackers.
    data = [gameID]
    db.execute("UPDATE games SET phase=23 WHERE id=?;", data)
    DefendingDeclareDamageOrder()
    # Triggered abilities that trigger off blockers being declared trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=24 WHERE id=?;", data)
    # Triggered abilities that trigger off blockers being declared trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=25 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=26 WHERE id=?;", data)
    PriorityLoop()
    # If a spell or ability causes a creature on the battlefield to block an attacking creature, players declare that creature's relative placement in the order that combat damage will be assigned to and by that creature's blockers.
    data = [gameID]
    db.execute("UPDATE games SET phase=27 WHERE id=?;", data)
    # If a creature is put onto the battlefield blocking, the active player declares its relative placement in the order that combat damage will be assigned for that creature's blockers.
    data = [gameID]
    db.execute("UPDATE games SET phase=28 WHERE id=?;", data)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=29 WHERE id=?;", data)

def ActiveDeclareDamageOrder():
    attackList = GetAttackers(gameID=gameID)
    multipleBlockersList = []
    for attacker in attackList:
        blockingCreatures = 0
        data = [attacker]
        blockingCreatures = (db.execute("SELECT COUNT(*) FROM blockers WHERE target=?", data)).fetchone()[0]
        if blockingCreatures > 1:
            # add to a list
            multipleBlockersList.append(attacker)
    
    if len(multipleBlockersList) > 1:
        # damage order code
        pass
    else:
        return
    
def DefendingDeclareDamageOrder():
    pass
    
def CombatDamagePhase(gameID):
    FirstDoubleStrikeCombatDamagePhase(gameID)
    NonFirstDoubleStrikeCombatDamagePhase(gameID)

def FirstDoubleStrikeCombatDamagePhase(gameID):
    # If no attacking or blocking creatures have first or double strike, then skip this substep.
    while True:
        return
    data = [gameID]
    db.execute("UPDATE games SET phase=30 WHERE id=?;", data)
    # All attacking creatures with first or double strike assign combat damage to their blockers.
    data = [gameID]
    db.execute("UPDATE games SET phase=31 WHERE id=?;", data)
    # All unblocked creatures with first or double strike assign combat damage to defending player or declared planeswalkers.
    data = [gameID]
    db.execute("UPDATE games SET phase=32 WHERE id=?;", data)
    # All defending creatures with first or double strike assign combat damage to their attackers.
    data = [gameID]
    db.execute("UPDATE games SET phase=33 WHERE id=?;", data)
    # All assigned damage is dealt simultaneously. This does not use the stack, and may not be responded to.
    data = [gameID]
    db.execute("UPDATE games SET phase=34 WHERE id=?;", data)
    # "Deals combat damage" and "is dealt combat damage" triggered abilities trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=35 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=36 WHERE id=?;", data)
    PriorityLoop()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=37 WHERE id=?;", data)
    DrainManaPools(gameID,37)

def NonFirstDoubleStrikeCombatDamagePhase(gameID):
    #  All attacking creatures without first strike assign combat damage to their blockers.
    data = [gameID]
    db.execute("UPDATE games SET phase=38 WHERE id=?;", data)
    AssignDamageBlockers(gameID)
    # All unblocked creatures without first strike assign combat damage to defending player or declared planeswalkers.
    data = [gameID]
    db.execute("UPDATE games SET phase=39 WHERE id=?;", data)
    AssignDamagePlayWalkers(gameID)
    # All defending creatures without first strike assign combat damage to their attackers.
    data = [gameID]
    db.execute("UPDATE games SET phase=40 WHERE id=?;", data)
    AssignDamageAttackers(gameID)
    # All assigned damage is dealt simultaneously. This does not use the stack, and may not be responded to.
    data = [gameID]
    db.execute("UPDATE games SET phase=41 WHERE id=?;", data)
    DealDamage(gameID)
    # "Deals combat damage" and "is dealt combat damage" triggered abilities trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=42 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=43 WHERE id=?;", data)
    PriorityLoop()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=44 WHERE id=?;", data)
    DrainManaPools(gameID,46)

def AssignDamageBlockers(gameID):
    # get list of attacking cards
    blockedAttackers = GetAttackers(gameID=gameID, blocked=True) # fix function so it foesnt givr all attackers always
    attBloList = []

    for attacker in blockedAttackers:
        blockers = GetBlockers(gameID=gameID, attacker=attacker)
        attbloKVP = {attacker:blockers}
        attBloList.append(attbloKVP)

    # REDO. GET KVP of a List of {attackers:[ListofBlockers]}  move through each one in a 2d loop assigning damage to the end of the block list   
    for attackerKVP in attBloList:
        for key in attackerKVP:
            data = [key]
            power = int(db.execute("SELECT power from ingamecards WHERE id=?", data).fetchone())
            for x in range(len(attackerKVP['key'])):
                data = [attackerKVP['key'][x]]
                blockerToughnessDamage = db.execute("SELECT toughness,damage_taken FROM ingamecards WHERE id=?", data).fetchall()
                remainingToughness = blockerToughnessDamage['toughness'] - blockerToughnessDamage['damage_taken']
                if power>remainingToughness:
                    # deal only the necessary damage
                    data = [remainingToughness, attackerKVP['key'][x]]
                    db.execute("UPDATE ingamecards SET damage_assigned=? WHERE id=?", data)
                    com.commit()
                    power -= remainingToughness
                else:
                    data = [power, attackerKVP['key'][x]]
                    db.execute("UPDATE ingamecards SET damage_assigned=? WHERE id=?", data)
                    com.commit()

def GetBlockers(**kwargs):
    attacker = kwargs.get('blocked', '')
    # NOT CURRENTLY WORKING FOR PLANESWALKERS NOT MULTIPLAYER
    # make **kwargs so it works to get ALL attacking creature OR JUST the attacking creatures that 1 player may block
    if attacker == '':
        data =[kwargs['gameID']]
        blockerListID = []
        blockerList = (db.execute("SELECT ingamecard_id FROM blockers WHERE game_id=?", data).fetchall())
        for row in blockerList:
            blockerListID.append(row['ingamecard_id'])
        return blockerListID
    else:
        data =[kwargs['gameID'], attacker]
        blockerListID = []
        blockerList = (db.execute("SELECT ingamecard_id FROM blockers WHERE game_id=? AND target=?", data).fetchall())
        for row in blockerList:
            blockerListID.append(row['ingamecard_id'])
        return blockerListID
        

def AssignDamagePlayWalkers(gameID):
    # get list of attacking cards    

    # REDO. GET KVP of a List of {attackers:[Player/Planeswalker]}  move through each one in a loop assigning damage  
    
    data = [gameID]
    attackerList = [] # attackers with no blockers
    # run loop putting assigned damage on each ingamecard of blocking
    for blocker in blockerList:
        pass
        # assign damage to players/planeswalkers
    
def AssignDamageAttackers(gameID):
    # REDO. GET KVP of a List of {blockers:[ListofAttackers]}  move through each one in a 2d loop assigning damage to the end of the block list   

    # get list of attacking cards    
    data = [gameID]
    blockerList = [] # attackers with blockers
    # run loop putting assigned damage on each ingamecard of blocking
    for blocker in blockerList:
        pass
        # assign damage to attackers
    
def DealDamage(gameID):
    # check for all with game_id and assigned damage
    data = [gameID]
    blockerList = [] # ingamecards and players with assigned damage
    # move assigned damage to damage_taken

    # work out what needs to visit the graveyard

    # excess damage for trample DO LATER
    pass

def EndOfCombatPhase(gameID):
    # "At end of combat" effects trigger. A
    data = [gameID]
    db.execute("UPDATE games SET phase=45 WHERE id=?;", data)
    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    data = [gameID]
    db.execute("UPDATE games SET phase=46 WHERE id=?;", data)
    # All creatures and planeswalkers are removed from combat.
    data = [gameID]
    db.execute("UPDATE games SET phase=47 WHERE id=?;", data)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=48 WHERE id=?;", data)
    DrainManaPools(gameID,13)
        

def PreCombatMainPhase(gameID):
    # pre combat main phasey things happen 
    data = [gameID]
    db.execute("UPDATE games SET phase=11 WHERE id=?;", data)
    con.commit()

    # land and sorcery speed spells can be played/cast
    data = [gameID]
    db.execute("UPDATE games SET phase=12 WHERE id=?;", data)
    con.commit()
    ActivePriority()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=13 WHERE id=?;", data)
    DrainManaPools(gameID,13)
    CombatPhase(gameID)
        
def UntapPhase(gameID):
    # CHANGE phase IN THE TABLE TO INTEGER AND ASSIGN 1-61 FOR ALL PHASES OF A MAGIC TURN

    data = [gameID]
    db.execute("UPDATE games SET phase=1 WHERE id=?", data)
    data = [gameID, gameID]
    db.execute("UPDATE ingamecards SET phased_out=0 WHERE game_id=? AND phased_out=1 AND controller=(SELECT active FROM games WHERE id=?);", data)
    con.commit()
    # phase out cards with phasing
    # check day/night cycle and change if necessary
    data = [gameID]
    db.execute("UPDATE games SET phase=2 WHERE id=?;", data)
                 
    #untap permanents
    data = [gameID]
    db.execute("UPDATE games SET phase=3 WHERE id=?;", data)
    data = [gameID, gameID]
    db.execute("UPDATE ingamecards SET tapped=0 WHERE game_id=? AND tapped=1 AND controller=(SELECT active FROM games WHERE id=?);", data)
    db.execute("UPDATE ingamecards SET sum_sick=0 WHERE game_id=? AND controller=(SELECT active FROM games WHERE id=?);", data)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=4 WHERE id=?;", data)
    DrainManaPools(gameID,4)

def UpkeepPhase(gameID):
    data = [gameID]
    db.execute("UPDATE games SET phase=5 WHERE id=?;", data)
    # upkeep things can thing
    # give active player priority
    data = [gameID]
    db.execute("UPDATE games SET phase=6 WHERE id=?;", data)
    data = [activePlayerIndex, gameID]
    db.execute("UPDATE games SET priority=? WHERE id=?;", data)
    PriorityLoop()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=7 WHERE id=?;", data)
    DrainManaPools(gameID,7)

def DrawPhase(gameID):
    # active player draws
    global activePlayerIndex
    data = [gameID]
    db.execute("UPDATE games SET phase=8 WHERE id=?;", data)
    if int((db.execute("SELECT turn_number FROM games WHERE id=?", data)).fetchone()[0]) > 0:
        DrawLibraryHand(gameID, activePlayerIndex, 1)
    # give active player priority
    data = [gameID]
    db.execute("UPDATE games SET phase=9 WHERE id=?;", data)
    PriorityLoop()
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=10 WHERE id=?;", data)
    DrainManaPools(gameID,10)

monoWhiteDeck = ["631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "631590", "636994", "636994", "636994", "636994","534751", "534751", "534751",
"534751", "534760", "534760", "534760", "534760", "534781", "534781", "534781", 
"534781", "534783", "534783", "534783", "534783", "540850", "548581", "583608", 
"583608", "583608", "583608", "585695", "602563", "602563", "602563", "607043",
"607043", "607043", "607043", "615394", "615394", "615394", "615394", "629532", "629532","544465","544465","544465","544465"]

# for x in range(2):
    # for card in monoWhiteDeck:
        # print(card)
        # db.execute("INSERT INTO deck_cards (id,deck,position) VALUES(?,?,'library');", card, (x+1))

players = (1,2)
gameType = "Standard"
db.execute("INSERT INTO games (player0) VALUES(?)", (players[0],))
con.commit()
gameID =  db.lastrowid
startingPlayerIndex = random.randrange(len(players))
startingPlayer = players[startingPlayerIndex]
playerNames = {}

if (gameType == "Standard"):
    # set players
    for x in range(len(players)):
        data = [players[x], gameID]
        db.execute("UPDATE games SET player" + str(x) + "=? WHERE id=?", data)
        data = [gameID]
        playerName = (db.execute("SELECT username FROM users JOIN games ON users.id=games.player" + str(x) + " WHERE games.id=?", data)).fetchone()[0]
        playerNames.update({x:playerName})

    # set life
    con.commit()
    StartingLife(gameID, gameType, players)

# assign decks to game

for x in range(len(players)):
    deck = db.execute("SELECT id FROM deck_cards WHERE deck=?;", (players[x],))
    deckList = list(deck.fetchall())
    for card in deckList:
        for item in card:
            data = [item, gameID, x]
            db.execute("INSERT INTO ingamecards (printed_id,game_id,owner,location,face_down) VALUES(?,?,?,'library',1);", data)

con.commit()

# Shuffle both libraries
for x in range(len(players)):
    ShuffleLibrary(gameID, x)

# Draw opening hands for both
for x in range(len(players)):
    DrawLibraryHand(gameID, x, 7)

# process mulligans
Mulligan(gameID, players)
"""
# display opening hands
for x in range(len(players)):
    print(f"Player {players[x]}'s starting hand:")
    PrintHands(gameID, x)
"""
# starting player begin the game
# update game table with turn 0, phase untap, priority, land, 
data = [startingPlayerIndex, gameID]
db.execute("UPDATE games SET active=?, turn_number=0 WHERE id=?;", data)
activePlayerIndex = startingPlayerIndex

# default all players to automatically pass priority (FOR NOW!!!)
passPriority = {}
passActivePriority = {}
for x in range(len(players)):
    passPriority.update({x:True})
    passActivePriority.update({x:False})

# add turns taken to game table
BeginningPhase(gameID)