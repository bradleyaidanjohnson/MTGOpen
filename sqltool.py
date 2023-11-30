import sqlite3
import random

con = sqlite3.connect("mtgopen.db")
db = con.cursor()

def GetLibraryIDs(gameID, playerIndex):
    data = [gameID, playerIndex]
    library = (db.execute("SELECT id FROM ingamecards WHERE game=? AND location='library' AND owner=? ORDER BY position;", data)).fetchall()
    libraryList = []
    for card in library:
        libraryList.append(card[0])
    return libraryList
        
def GetHandIDs(gameID, playerIndex):
    data = [gameID, playerIndex]
    hand = (db.execute("SELECT id FROM ingamecards WHERE game=? AND location='hand' AND owner=?;", data)).fetchall()
    handList = []
    for card in hand:
        handList.append(card[0])
    return handList

def IngameCardIDToName(id):
    data = [id]
    name = (db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printedid WHERE ingamecards.id=?;", data)).fetchone()[0]
    return name
    
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
    rows = db.execute("SELECT COUNT(*) FROM ingamecards WHERE game=? AND location='library' AND owner=?;", data)
    rows = rows.fetchone()[0]

    randomNumbers = random.sample(range(rows), rows)
    data = [gameID, playerIndex]
    for row in (db.execute("SELECT id FROM ingamecards WHERE game=? AND location='library' AND owner=?;", data)).fetchall():
        data = [randomNumbers.pop(), row[0]]
        db.execute("UPDATE ingamecards SET position=? WHERE id=?;", data)
    con.commit()

def DrawLibraryHand(gameID, playerIndex, drawSize):
    data = [playerIndex, playerIndex, gameID, drawSize]
    db.execute("UPDATE ingamecards SET position='', location='hand', controller=? WHERE owner=? AND game=? ORDER BY position DESC LIMIT ?;", data)
    con.commit()

def HandToLibraryAll(gameID, playerIndex):
    data = [gameID, playerIndex]
    hand = (db.execute("SELECT id FROM ingamecards WHERE game=? AND (location='hand' OR location='library') AND owner=?;", data)).fetchall()
    randomNumbers = random.sample(range(len(hand)), len(hand))
    for card in hand:
        data = [randomNumbers.pop(), card[0]]
        db.execute("UPDATE ingamecards SET position=?, location='library' WHERE id=?;", data)
    con.commit()

def PrintHands(gameID, playerIndex):
    data = [playerIndex, gameID]
    hand = (db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printedid WHERE ingamecards.location='hand' AND controller=? AND game=?;", data)).fetchall()
    for card in hand:
        print(card[0])

def Action(gameID, playerIndex):
    while True:
        try:
            answer = str(input(f"{playerNames[playerIndex]}: you have priority:\nH: Play a card from your Hand.\nP: Pass Priority.\nWhat would you like to do?\n"))
        except ValueError:
            print("Invalid response: please enter a letter")
            continue
        if answer == 'p':
            break
        elif answer == "h":
            print("play a card from hand")
            PlayCardHand(playerIndex)
            continue
        else:
            print("Invalid response: please choose one of the options")
            continue

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
            print("Card cannot be played, please pick again")
            continue
        
def PlayCard(id, playerIndex):
    # get card type
    # ADD COLUMN TO INGAMECARDS CALLED TYPE WHERE YOU CAN CHECK IF ANY TYPE CHANGES HAVE OCCURED CHECK THAT BEFORE YOU RUN THE PRINTED CARDS TYPE, IF NOT RUN THE PRINTED CARDS TYPE
    data = [id]
    cardType = (db.execute("SELECT Ntype from cards JOIN ingamecards ON cards.Nid=ingamecards.printedid WHERE ingamecards.id=?", data)).fetchone()[0]
    print(cardType)
    if "Land" in cardType:
        print("Card is a Land")
        data = [gameID]
        land = (db.execute("SELECT land" + str(playerIndex) + " FROM games WHERE id=?", data)).fetchone()[0]
        if land > 0:
            # change land location from hand to battlefield and tapped to 0
            data = [id]
            db.execute("UPDATE ingamecards SET location='battlefield', tapped=0 WHERE id=?", data)
            land -= 1
            data = [land, gameID]
            db.execute("UPDATE games SET land" + str(activePlayer) + " = ? WHERE id=?;", data)
            con.commit()
            print("Card played")
            return True
        else:
            print("You cannot play anymore lands this turn.")
            return False
    
        
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

def ActivePriority():   
    x = startingPlayerIndex
    while True:
        if passActivePriority[activePlayer] == False and x == startingPlayerIndex:
            Action(gameID, x)
        elif passPriority[x] == False:
            Action(gameID, x)
        if x == len(players) - 1:
            x = 0
        else:
            x += 1
        # print("Are these equal? " + str(priorityIndex) + " and " + str(firstPriority))
        data = [x, gameID]
        db.execute("UPDATE games SET priority=? WHERE id=?;", data)
        con.commit()
        if x == startingPlayerIndex:
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
                if x == startingPlayer:
                    print("You go first")
                else:
                    print("Your oppontent goes first")

                print(playerNames[x] + "'s draw:")
                data = [x, gameID]
                hand = db.execute("SELECT Nname FROM cards JOIN ingamecards ON cards.Nid = ingamecards.printedid WHERE ingamecards.location='hand' AND controller=? AND game=?;", data)
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

def BeginningPhase(gameID):
    # MAKE THIS A FUNCTION AT SOME POINT
    data = [gameID]
    db.execute("UPDATE games SET land" + str(activePlayer) + " = 1 WHERE id=?;", data)
    con.commit()

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
    ActivePriority()
    print("成功!")
        
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

print(playerNames)

# assign decks to game

for x in range(len(players)):
    deck = db.execute("SELECT id FROM deck_cards WHERE deck=?;", (players[x],))
    deckList = list(deck.fetchall())
    for card in deckList:
        for item in card:
            data = [item, gameID, x]
            db.execute("INSERT INTO ingamecards (printedid,game,owner,location,facedown) VALUES(?,?,?,'library',1);", data)

con.commit()

# Shuffle both libraries
for x in range(len(players)):
    ShuffleLibrary(gameID, x)

# Draw opening hands for both
for x in range(len(players)):
    DrawLibraryHand(gameID, x, 7)

# process mulligans
Mulligan(gameID, players)

# display opening hands
for x in range(len(players)):
    print(f"Player {players[x]}'s starting hand:")
    PrintHands(gameID, x)

# starting player begin the game
# update game table with turn 0, phase untap, priority, land, 
data = [startingPlayerIndex, gameID]
db.execute("UPDATE games SET active=? WHERE id=?;", data)
activePlayer = startingPlayerIndex

# default all players to automatically pass priority (FOR NOW!!!)
passPriority = {}
passActivePriority = {}
for x in range(len(players)):
    passPriority.update({x:True})
    passActivePriority.update({x:False})

# add turns taken to game table
BeginningPhase(gameID)