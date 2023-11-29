import sqlite3
import random

con = sqlite3.connect("mtgopen.db")
db = con.cursor()

def GetLibraryIDs(gameID, player):
    data = [gameID, player]
    library = (db.execute("SELECT id FROM ingamecards WHERE game=? AND location='library' AND owner=? ORDER BY position;", data)).fetchall()
    libraryList = []
    for card in library:
        libraryList.append(card[0])
    return libraryList
        
def GetHandIDs(gameID, player):
    data = [gameID, player]
    hand = (db.execute("SELECT id FROM ingamecards WHERE game=? AND location='hand' AND owner=?;", data)).fetchall()
    handList = []
    for card in hand:
        handList.append(card[0])
    return handList

def IngameCardIDToName(id):
    data = [id]
    name = (db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printedid WHERE ingamecards.id=?;", data)).fetchall()[0]
    return name
    
def StartingLife(gameID, format, players):
    # set life
    life = 20
    if format=="Standard":
        for x in range(len(players)):
            data = [life, gameID]
            db.execute("UPDATE games SET life" + str(x) + "=? WHERE id=?;", data)

    con.commit()

def ShuffleLibrary(gameID, player):
    data = [gameID, player]
    rows = db.execute("SELECT COUNT(*) FROM ingamecards WHERE game=? AND location='library' AND owner=?;", data)
    rows = rows.fetchone()[0]

    randomNumbers = random.sample(range(rows), rows)
    data = [gameID, player]
    for row in (db.execute("SELECT id FROM ingamecards WHERE game=? AND location='library' AND owner=?;", data)).fetchall():
        data = [randomNumbers.pop(), row[0]]
        db.execute("UPDATE ingamecards SET position=? WHERE id=?;", data)
    con.commit()

def DrawLibraryHand(gameID, player, drawSize):
    data = [player, player, gameID, drawSize]
    db.execute("UPDATE ingamecards SET position='', location='hand', controller=? WHERE owner=? AND game=? ORDER BY position DESC LIMIT ?;", data)
    con.commit()

def HandToLibraryAll(gameID, player):
    data = [gameID, player]
    hand = (db.execute("SELECT id FROM ingamecards WHERE game=? AND (location='hand' OR location='library') AND owner=?;", data)).fetchall()
    randomNumbers = random.sample(range(len(hand)), len(hand))
    for card in hand:
        data = [randomNumbers.pop(), card[0]]
        db.execute("UPDATE ingamecards SET position=?, location='library' WHERE id=?;", data)
    con.commit()

def PrintHands(gameID, player):
    data = [player, gameID]
    hand = (db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printedid WHERE ingamecards.location='hand' AND controller=? AND game=?;", data)).fetchall()
    for card in hand:
        print(card[0])

def Action(gameID, player):
    answer = input(f"{player}: Will you take an action?)")
    print(answer)
        
def PriorityLoop(players):
    data = [gameID]
    priorityIndex = (db.execute("SELECT priority FROM games WHERE id=?;", data)).fetchone()[0]
    firstPriority = priorityIndex
    data = [gameID]
    db.execute("SELECT * FROM ingamecards WHERE id=? AND position='stack';", data)
    topStackOwner = None
    if db.fetchone() is not None:
        topStackOwner = (db.execute("SELECT owner FROM ingamecards WHERE id=? ORDER BY location LIMIT 1;", data)).fetchone()[0]
    
    while True:
        if passPriority[priorityIndex] == False:
            Action(gameID, players[priorityIndex])
        if priorityIndex == len(players) - 1:
            priorityIndex = 0
        else:
            priorityIndex = priorityIndex + 1
        # print("Are these equal? " + str(priorityIndex) + " and " + str(firstPriority))
        data = [priorityIndex, gameID]
        db.execute("UPDATE games SET priority=? WHERE id=?;", data)
        con.commit()
        if players[priorityIndex] == topStackOwner:
            break
        if priorityIndex == firstPriority:
            break
        

    
def DrainManaPools(gameID):
    for x in range(6):
        data = [gameID]
        db.execute("UPDATE games SET colorless_mana" + str(x) + "=0,white_mana" + str(x) + "=0,blue_mana" + str(x) + "=0,black_mana" + str(x) + "=0,red_mana" + str(x) + "=0,green_mana" + str(x) + "=0 WHERE id=?;", data)
    con.commit()
    
def Mulligan(gameID, players):
    # 2 dicts for mulligan decisions/reprecusions
    playerMulliganDecision = {}
    playerBottoms = {}
    playerReady = {}
    for player in players:
        playerMulliganDecision.update({player:True})
        playerBottoms.update({player:0})
        playerReady.update({player:False})
    anyMulligans = True

    while True:
        anyMulligans = False
        for player in players:
            if playerMulliganDecision[player] == True and playerReady[player] == False:
                                # add code to show if other player(s) is(are) ready
                if player == startingPlayer:
                    print("You go first")
                else:
                    print("Your oppontent goes first")

                print(str(player) + "'s draw:")
                data = [player, gameID]
                hand = db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printedid WHERE ingamecards.location='hand' AND controller=? AND game=?;", data)
                handList = hand.fetchall()
                for card in handList:
                    print(card[0])
                    # print the turn order for them to decide on the mulligsn
                    # also inform them of the decisions of the other player(s) (Your opponent kept a hand of x cards)
                if playerBottoms[player] + 1 == 1:
                    answer = input(f"{player}: Will you keep your hand? (you will return {(playerBottoms[player] + 1)} card to the bottom of your library.)")
                else:
                    answer = input(f"{player}: Will you keep your hand? (you will return {(playerBottoms[player] + 1)} cards to the bottom of your library.)")
                if answer=='y' or playerBottoms[player] >= 6:
                    playerMulliganDecision.update({player:False})
                else:
                    playerMulliganDecision.update({player:True})
                    playerBottoms.update({player:(playerBottoms[player] + 1)})
        for player in players:
            if playerMulliganDecision[player] == True:
                anyMulligans = True
                # put all cards back into deck, shuffle, then draw new hand
                HandToLibraryAll(gameID, player)
                ShuffleLibrary(gameID, player)
                DrawLibraryHand(gameID, player, 7)
            elif playerReady[player] == False:
                if playerBottoms[player] > 0:
                    # Get library into a list
                    library = GetLibraryIDs(gameID, player)
                    # get hand int a list
                    hand = GetHandIDs(gameID, player)
                    print(f"Put {playerBottoms[player]} cards on the bottom of your library: ")
                    for x in range(len(hand)):
                        name = IngameCardIDToName(hand[x])
                        print(f"{(x + 1)}: {name}")
                    bottomedCards = []
                    for x in range(playerBottoms[player]):
                        # place as many hand cards as needed into the library list at the 0 position and remove from the hand list

                        # CHECK TO MAKE SURE YOU DONT BOTTOM THE SAME CARD MULTIPLE TIMES

                        bottom = int(input(f"Card {x + 1}:"))
                        library.insert(0, hand.pop(bottom - 1))
                    # push the changes to the database
                    for x in range(len(library)):
                        data = [x, library[x]]
                        db.execute("UPDATE ingamecards SET location='library', position=? WHERE id=?;", data)
                    for card in hand:
                        data = [card]
                        db.execute("UPDATE ingamecards SET location='hand', position='' WHERE id=?;", data)
                    con.commit()
                playerReady[player] == True
        if not anyMulligans:
            break

def BeginningPhase(gameID):
    UntapPhase(gameID)
    UpkeepPhase(gameID)
    DrawPhase(gameID)
    PreCombatMainPhase(gameID)

def PreCombatMainPhase(gameID):
    # pre combat main phasey things happen 
    data = [gameID]
    db.execute("UPDATE games SET phase=11 WHERE id=?;", data)
    con.commit()

    # land and sorcery speed spells can be played/cast
    data = [gameID]
    db.execute("UPDATE games SET phase=12 WHERE id=?;", data)
    con.commit()
    hand = GetHandIDs(gameID, activePlayer)
    print("Hand: ")
    for x in range(len(hand)):
        name = IngameCardIDToName(hand[x])
        print(f"{(x + 1)}: {name[0]}")
    # something
    choice = int(input(f"Card:"))
    print(choice)
        
def UntapPhase(gameID):
    # CHANGE phase IN THE TABLE TO INTEGER AND ASSIGN 1-61 FOR ALL PHASES OF A MAGIC TURN

    data = [gameID]
    db.execute("UPDATE games SET phase=1 WHERE id=?", data)
    data = [gameID, gameID]
    db.execute("UPDATE ingamecards SET phased_out=0 WHERE game=? AND phased_out=1 AND controller=(SELECT active FROM games WHERE id=?);", data)
    con.commit()
    # phase out cards with phasing
    # check day/night cycle and change if necessary
    data = [gameID]
    db.execute("UPDATE games SET phase=2 WHERE id=?;", data)
                 
    #untap permanents
    data = [gameID]
    db.execute("UPDATE games SET phase=3 WHERE id=?;", data)
    data = [gameID, gameID]
    db.execute("UPDATE ingamecards SET tapped=0 WHERE game=? AND tapped=1 AND controller=(SELECT active FROM games WHERE id=?);", data)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=4 WHERE id=?;", data)
    DrainManaPools(gameID)

def UpkeepPhase(gameID):
    data = [gameID]
    db.execute("UPDATE games SET phase=5 WHERE id=?;", data)
    # upkeep things can thing
    # give active player priority
    data = [gameID]
    db.execute("UPDATE games SET phase=6 WHERE id=?;", data)
    data = [startingPlayerIndex, gameID]
    db.execute("UPDATE games SET priority=? WHERE id=?;", data)
    PriorityLoop(players)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=7 WHERE id=?;", data)
    DrainManaPools(gameID)

def DrawPhase(gameID):
    # active player draws
    data = [gameID]
    db.execute("UPDATE games SET phase=8 WHERE id=?;", data)
    DrawLibraryHand(gameID, activePlayer, 1)
    PrintHands(gameID, activePlayer)
    # give active player priority
    data = [gameID]
    db.execute("UPDATE games SET phase=9 WHERE id=?;", data)
    PriorityLoop(players)
    #drain mana from pools
    data = [gameID]
    db.execute("UPDATE games SET phase=10 WHERE id=?;", data)
    DrainManaPools(gameID)

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

if (gameType == "Standard"):
    # set players
    for x in range(len(players)):
        data = [players[x], gameID]
        db.execute("UPDATE games SET player" + str(x) + "=? WHERE id=?", data)

    # set life
    con.commit()
    StartingLife(gameID, gameType, players)

# assign decks to game

for x in range(len(players)):
    deck = db.execute("SELECT id FROM deck_cards WHERE deck=?;", (players[x],))
    deckList = list(deck.fetchall())
    for card in deckList:
        for item in card:
            data = [item, gameID, players[x]]
            db.execute("INSERT INTO ingamecards (printedid,game,owner,location,facedown) VALUES(?,?,?,'library',1);", data)

con.commit()

# Shuffle both libraries
for x in range(len(players)):
    ShuffleLibrary(gameID, players[x])

# Draw opening hands for both
for x in range(len(players)):
    DrawLibraryHand(gameID, players[x], 7)

# process mulligans
Mulligan(gameID, players)

# display opening hands
for x in range(len(players)):
    print(f"Player {players[x]}'s starting hand:")
    PrintHands(gameID, players[x])

# starting player begin the game
# update game table with turn 0, phase untap, priority, land, 
data = [startingPlayerIndex, gameID]
db.execute("UPDATE games SET active=? WHERE id=?;", data)
activePlayer = players[startingPlayerIndex]

# default all players to automatically pass priority (FOR NOW!!!)
passPriority = {}
for x in range(len(players)):
    passPriority.update({x:True})

# add turns taken to game table
BeginningPhase(gameID)