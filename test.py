import etb
import random
import string
import sqlite3
con = sqlite3.connect("mtgopen.db")
con.row_factory = sqlite3.Row
db = con.cursor()

class Card:

    dynamics = []

    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        self.name = name
        self.id = id
        self.game = game
        self.owner = owner
        self.controller = controller
        self.location = location
        self.position = position
        self.token = token
        self.tapped = tapped
        self.face_down = face_down
        self.flipped = flipped
        self.phased_out = phased_out
        self.color_identity = color_identity
        self.card_set = card_set
        self.card_type = card_type
        self.mana_cost = mana_cost
        self.cmc = cmc
        self.ability = ability
        self.color = color
        self.assoc_id = assoc_id
        self.gen_mana = gen_mana

    def __repr__(self):
        return self.name
    
    def enters_the_battlefield(self, card):
        self.position = ''
        self.location = 'battlefield'
        self.tapped = False
        self.face_down = False
        
        func_name = function_name_from_cardname(card.name)
        if func_name in dir(etb):
            print(self.dynamics)
            function = getattr(etb, func_name)
            new_self = function(self,card)
            print(new_self)
            self = new_self

        print(f"You played a {self.name} into the battlefield, is it tapped? {self.tapped}")

    def get_cost(self):
        cost_string = self.mana_cost


class Permanent(Card):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class InstSorc(Card):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Instant(InstSorc):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Sorcery(InstSorc):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)


class Land(Permanent):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Basic_Land(Land):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Creature(Permanent):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana, sum_sick, power, toughness):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)
        self.sum_sick = sum_sick
        self.power = power
        self.toughness = toughness

class Artifact(Permanent):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Enchantment(Permanent):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Battle(Permanent):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Planeswalker(Permanent):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana)

class Artifact_Creature(Creature, Artifact):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana, sum_sick, power, toughness):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana, sum_sick, power, toughness)

class Enchantment_Creature(Creature, Enchantment):
    
    def __init__(self,name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana, sum_sick, power, toughness):
        super().__init__(name,id,game,owner,controller,location,position,token,tapped,face_down,flipped,phased_out,color_identity,card_set,card_type,mana_cost,cmc,ability,color,assoc_id,gen_mana, sum_sick, power, toughness)

class Mana:
    def __init__(self, quantity, mana_type, player, source, destination, refundable, restrictions, duration, trigger):
        self.quantity = quantity
        self.mana_type = mana_type
        self.player = player
        self.source = source
        self.destination = destination
        self.refundable = refundable
        self.restrictions = restrictions
        self.duration = duration
        self.trigger = trigger

class Mana_Cost:
    def __init__(self, quantity, mana_type,):
        self.quantity = quantity
        self.mana_type = mana_type

class Spell:
    def __init__(self,text,source,targets,controller,position):
        self.text = text
        self.source = source
        self.targets = targets
        self.controller = controller
        self.position = position

players = []

for x in range(2):
    data = [x +1]
    players.append(db.execute("SELECT username FROM users WHERE id=?", data).fetchone()[0])

player_0_deck_data = db.execute("SELECT deck_cards.id FROM deck_cards JOIN decks ON decks.id=deck_cards.deck JOIN users on decks.id=users.id WHERE users.id=1").fetchall()
player_1_deck_data = db.execute("SELECT deck_cards.id FROM deck_cards JOIN decks ON decks.id=deck_cards.deck JOIN users on decks.id=users.id WHERE users.id=2").fetchall()

player_0_deck_ids = []
player_1_deck_ids = []

for item in player_0_deck_data:
    player_0_deck_ids.append(item[0])

for item in player_1_deck_data:
    player_1_deck_ids.append(item[0])

deck_0 = []
deck_1 = []

decks = [deck_0,deck_1]

mana_strings = ['W', 'U', 'B', 'R', 'G', 'C','UB', 'BR','RG','GW','WB','UR','BG','RW','GU','2W','2U','2B','2R','2G','PW', 'PU', 'PB', 'PR', 'PG', 'PGU', 'PRG', 'PRW', 'PGW', 'S']

starting_player_index = random.randint(0,(len(decks)-1))

for deck in decks:
    for x in range(len(player_0_deck_ids)):
        data = [player_0_deck_ids[x]]
        card_info_object = db.execute("SELECT * FROM cards WHERE Nid=?", data).fetchall()[0]
        if "Instant" in card_info_object['Ntype']:
            deck.append(Instant(card_info_object['Nname'],card_info_object['Nid'],card_info_object['Ngame'],card_info_object['Nowner'],card_info_object['Ncontroller'],card_info_object['Nlocation'],card_info_object['Nposition'],card_info_object['Ntoken'],card_info_object['Ntapped'],card_info_object['Nface_down'],card_info_object['Nflipped'],card_info_object['Nphased_out'],card_info_object['Ncolor_identity'],card_info_object['Ncard_set'],card_info_object['Ncard_type'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassoc_id'],card_info_object['Ngen_mana']))
        elif "Sorcery" in card_info_object['Ntype']:
            deck.append(Sorcery(card_info_object['Nname'],card_info_object['Nid'],card_info_object['Ngame'],card_info_object['Nowner'],card_info_object['Ncontroller'],card_info_object['Nlocation'],card_info_object['Nposition'],card_info_object['Ntoken'],card_info_object['Ntapped'],card_info_object['Nface_down'],card_info_object['Nflipped'],card_info_object['Nphased_out'],card_info_object['Ncolor_identity'],card_info_object['Ncard_set'],card_info_object['Ncard_type'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassoc_id'],card_info_object['Ngen_mana']))
        elif "Planeswalker" in card_info_object['Ntype']:
            deck.append(Planeswalker(card_info_object['Nname'],card_info_object['Nid'],card_info_object['Ngame'],card_info_object['Nowner'],card_info_object['Ncontroller'],card_info_object['Nlocation'],card_info_object['Nposition'],card_info_object['Ntoken'],card_info_object['Ntapped'],card_info_object['Nface_down'],card_info_object['Nflipped'],card_info_object['Nphased_out'],card_info_object['Ncolor_identity'],card_info_object['Ncard_set'],card_info_object['Ncard_type'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassoc_id'],card_info_object['Ngen_mana']))
        elif "Battle" in card_info_object['Ntype']:
            deck.append(Battle(card_info_object['Nname'],card_info_object['Nid'],card_info_object['Ngame'],card_info_object['Nowner'],card_info_object['Ncontroller'],card_info_object['Nlocation'],card_info_object['Nposition'],card_info_object['Ntoken'],card_info_object['Ntapped'],card_info_object['Nface_down'],card_info_object['Nflipped'],card_info_object['Nphased_out'],card_info_object['Ncolor_identity'],card_info_object['Ncard_set'],card_info_object['Ncard_type'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassoc_id'],card_info_object['Ngen_mana']))
        elif "Enchantment" in card_info_object['Ntype']:
            deck.append(Enchantment(card_info_object['Nname'],card_info_object['Nid'],card_info_object['Ngame'],card_info_object['Nowner'],card_info_object['Ncontroller'],card_info_object['Nlocation'],card_info_object['Nposition'],card_info_object['Ntoken'],card_info_object['Ntapped'],card_info_object['Nface_down'],card_info_object['Nflipped'],card_info_object['Nphased_out'],card_info_object['Ncolor_identity'],card_info_object['Ncard_set'],card_info_object['Ncard_type'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassoc_id'],card_info_object['Ngen_mana']))
        elif "Basic Land" in card_info_object['Ntype']:
            deck.append(Basic_Land(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana']))
        elif "Land" in card_info_object['Ntype']:
            deck.append(Land(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana']))
        elif "Artifact Creature" in card_info_object['Ntype']:
            deck.append(Artifact_Creature(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana'], True, card_info_object['Npower'], card_info_object['Ntoughness']))
        elif "Enchantment Creature" in card_info_object['Ntype']:
            deck.append(Enchantment_Creature(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana'], True, card_info_object['Npower'], card_info_object['Ntoughness']))
        elif "Creature" in card_info_object['Ntype']:
            deck.append(Creature(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana'], True, card_info_object['Npower'], card_info_object['Ntoughness']))
        elif "Enchantment" in card_info_object['Ntype']:
            deck.append(Enchantment(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana']))
        elif "Artifact" in card_info_object['Ntype']:
            deck.append(Artifact(card_info_object['Nname'],card_info_object['Nid'],0,0,0,'library',x,False,False,True,False,False,card_info_object['Ncolor_identity'],card_info_object['Nset'],card_info_object['Ntype'],card_info_object['Nmana_cost'],card_info_object['Ncmc'],card_info_object['Nability'],card_info_object['Ncolor'],card_info_object['Nassociated_id'],card_info_object['Ngenerated_mana']))
    
    # Shuffle deck
    random.shuffle(deck)

def function_name_from_cardname(cardname):
    cardname = cardname.lower()
    cardname = cardname.replace(" ", "_")
    # print(f"printing the changed name as {cardname}")
    return cardname


def find_deck_ids(player_index):
    deck = []
    for x in range(len(decks[player_index])):
        if decks[player_index][x].location == 'library':
            deck.append(x)
    return deck
    random.shuffle(deck)

def find_hand_ids(player_index):
    hand = []
    for x in range(len(decks[player_index])):
        if decks[player_index][x].location == 'hand':
            hand.append(x)
    return hand

def shuffle_library(player_index):
    deck = find_deck_ids(player_index)
    random.shuffle(deck)
    for x in range(len(deck)):
        decks[player_index][deck[x]].position = x
    decks[player_index].sort(key=lambda x: x.position, reverse=True)

def draw_library_hand(player_index, cards):
    deck = find_deck_ids(player_index)
    for y in range(cards):
        decks[player_index][deck[len(deck) - y - 1]].location = 'hand'
        decks[player_index][deck[len(deck) - y - 1]].position = ''

def hand_to_library_all(playerIndex):
    library = []
    for card in decks[playerIndex]:
        if card.location == 'library':
            library.append(card)

    maxPos = max(card.position for card in library)
    print(maxPos)

    for card in decks[playerIndex]:
        if card.location == 'hand':
            card.location = 'library'

def drain_mana_pools():
    for mana in mana_pool:
        if mana.duration == '':
            del mana

def priority_loop():
    global priority
    firstPriority = priority
    top_stack_owner = ''
    if stack:
        top_stack_owner = stack[-1].owner
    
    while True:
        if pass_priority[priority] == False:
            action(priority)
        if priority == len(players) - 1:
            priority = 0
        else:
            priority = priority + 1
        priority = priority
        if players[priority] == top_stack_owner:
            break
        if priority == firstPriority:
            break

def active_priority():   
    x = active_player_index
    while True:
        if pass_active_priority[active_player_index] == False and x == active_player_index:
            action(x)
        elif pass_priority[x] == False:
            action(x)
        if x == len(players) - 1:
            x = 0
        else:
            x += 1
        priority = x
        if x == active_player_index:
            break

def action(player_index):
    while True:
        try:
            answer = str(input(f"{players[player_index]}: you have priority:\nH: Play a card from your Hand.\nB: Interact with a card on the Battlefield.\nP: Pass Priority.\nWhat would you like to do?\n"))
        except ValueError:
            print("Invalid response: please enter a letter")
            continue
        if answer == 'p':
            break
        elif answer == "h":
            play_card_hand(player_index)
            continue
        elif answer == "b":
            BattlefieldInteraction(player_index)
            continue
        else:
            print("Invalid response: please choose one of the options")
            continue

def play_card_hand(player_index):
    # get hand int a list
    hand = find_hand_ids(player_index)
    while True:
        print(f"Pick a card: ")
        for y in range(len(hand)):
            name = decks[player_index][hand[y]]
            print(f"{(y + 1)}: {name}")
        print("Or P to cancel.")
        answer = input(f"Pick an option:")
        if answer == 'p':
            break
        chosen_ingamecard_index = hand[int(answer) - 1]
        if play_card(chosen_ingamecard_index, player_index):
            break
        else:
            print("Card was not played, please pick again")
            continue

def play_card(card_index, player_index):
    # get card type
    # ADD COLUMN TO INGAMECARDS CALLED TYPE WHERE YOU CAN CHECK IF ANY TYPE CHANGES HAVE OCCURED CHECK THAT BEFORE YOU RUN THE PRINTED CARDS TYPE, IF NOT RUN THE PRINTED CARDS TYPE
    if "Land" in decks[player_index][card_index].card_type:
        global land
        if land > 0:
            # change land location from hand to battlefield and tapped to 0
            enters_the_battlefield(player_index, card_index)
            land -= 1
            return True
        else:
            print("You cannot play anymore lands this turn.")
            return False
    else:
        if PayMana(card_index, player_index):
            if CastSpell(card_index, player_index):
                return True
            else:
                return False
        else:
            if PayCardCost(card_index, player_index):
                # CastSpell(id)
                data = [card_index]
                db.execute("UPDATE ingamecards SET location='battlefield', tapped=0, face_down=0 WHERE id=?", data)
                return True
            else:
                return False
            
def pay_mana_from_pool(card_index, player_index):
    cost = decks[player_index][card_index].get_cost()
            
def enters_the_battlefield(player_index, card_index):
    for deck in decks:
        for card in deck:
            if card.location == 'battlefield' or card==decks[player_index][card_index]:
                card.enters_the_battlefield(decks[player_index][card_index])
    pass

def beginning_phase():
    untap_phase()
    upkeep_phase()
    draw_phase()
    pre_combat_main_phase()

def untap_phase():
    # CHANGE phase IN THE TABLE TO INTEGER AND ASSIGN 1-61 FOR ALL PHASES OF A MAGIC TURN
    # phase out cards that are phased in/ phase out cards with phasing
    global land
    land = 1
    for deck in decks:
        for card in deck:
            if card.phased_out == True and card.controller == active_player_index:
                card.phased_out = False

    # phase out cards with phasing
    # check day/night cycle and change if necessary
    if day_night > 0:
        pass # change day to night with spell count
                 
    #untap permanents
    for deck in decks:
        for card in deck:
            if card.tapped == True and card.controller == active_player_index:
                card.tapped = False
                
    for deck in decks:
        for card in deck:
            if 'Creature' in card.card_type:
                if card.sum_sick == True and card.controller == active_player_index:
                    card.sum_sick = False
    #drain mana from pools
    drain_mana_pools()

def upkeep_phase():
    # upkeep things can thing
    # give active player priority
    global priority
    priority = active_player_index
    priority_loop()
    #drain mana from pools
    drain_mana_pools()

def draw_phase():
    # active player draws
    global active_player_index
    if turn_number > 0:
        draw_library_hand(active_player_index, 1)
    # give active player priority
    priority_loop()
    #drain mana from pools
    drain_mana_pools()

def pre_combat_main_phase():
    # pre combat main phasey things happen 

    # land and sorcery speed spells can be played/cast
    active_priority()
    #drain mana from pools
    drain_mana_pools()
    combat_phase()

def combat_phase():
    beginning_of_combat_phase()
    if declare_attackers_phase():
        DeclareBlockersPhase()
        CombatDamagePhase()
    EndOfCombatPhase()
    PostCombatMainPhase()

def beginning_of_combat_phase():
    # "At beginning of combat" triggered abilities trigger. A

    #     The active player gets priority to cast instants, spells with flash, and to use activated abilities. B

    priority_loop()
    #drain mana from pools
    drain_mana_pools()

def declare_attackers_phase():
    attackers_declared = False
    # The active player declares his attackers. If no attackers are declared, the Declare Blockers and Combat Damage steps are skipped.
    if declare_attackers(active_player_index):
        attackers_declared = True

    # Triggered abilities that trigger off attackers being declared trigger. A

    # The active player gets priority to cast instants, spells with flash, and to use activated abilities. B
    priority_loop()
    #drain mana from pools
    drain_mana_pools()
    return attackers_declared

def declare_attackers(playerIndex):
    attackers = get_attack_ready_ids(playerIndex)
    attackTargets = GetAttackTargets(playerIndex)
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
                print(f"{x +1}: {attackers[x]} (Declared)")
            else:
                print(f"{x +1}: {attackers[x]} (Undeclared)")
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

def get_attack_ready_ids(player_index):
    attack_ready_index_list = []
    for x in range(len(decks[player_index])):
        if card.location == 'battlefield' and 'Creature' in card.type and not card.sum_sick and not card.tapped and controller==player_index:
            attack_ready_index_list.append(card)
    
    for row in attackReadyList:
        attack_ready_index_list.append(row['id'])
    return attack_ready_index_list

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

def mulligan(decks):
    # 2 dicts for mulligan decisions/reprecusions
    playerMulliganDecision = {}
    playerBottoms = {}
    playerReady = {}
    for x in range(len(decks)):
        playerMulliganDecision.update({x:True})
        playerBottoms.update({x:0})
        playerReady.update({x:False})
    anyMulligans = True

    while True:
        anyMulligans = False
        for x in range(len(decks)):
            if playerMulliganDecision[x] == True and playerReady[x] == False:
                                # add code to show if other player(s) is(are) ready
                if x == starting_player_index:
                    print("You go first")
                else:
                    print("Your opponent goes first")

                print(players[x] + "'s draw:")
                hand = []
                for card in decks[x]:
                    if card.location == 'hand':
                        hand.append(card)
                for card in hand:
                    print(card)
                    # print the turn order for them to decide on the mulligsn
                    # also inform them of the decisions of the other player(s) (Your opponent kept a hand of x cards)
                if playerBottoms[x] == 0:
                    answer = input(f"{players[x]}: Will you keep your hand? (you will return {(playerBottoms[x] + 1)} card to the bottom of your library.)")
                else:
                    answer = input(f"{players[x]}: Will you keep your hand? (you will return {(playerBottoms[x] + 1)} cards to the bottom of your library.)")
                if answer=='y' or playerBottoms[x] >= 6:
                    playerMulliganDecision.update({x:False})
                else:
                    playerMulliganDecision.update({x:True})
                    playerBottoms.update({x:(playerBottoms[x] + 1)})
        for x in range(len(players)):
            if playerMulliganDecision[x] == True:
                anyMulligans = True
                # put all cards back into deck, shuffle, then draw new hand
                hand_to_library_all(x)
                shuffle_library(x)
                draw_library_hand(x, 7)
            elif playerReady[x] == False:
                if playerBottoms[x] > 0:
                    # Get library into a list
                    library = find_deck_ids(x)
                    # get hand int a list
                    hand = find_hand_ids(x)
                    print(f"Put {playerBottoms[x]} cards on the bottom of your library: ")
                    for y in range(len(hand)):
                        name = (decks[x][hand[y]].name)
                        print(f"{(y + 1)}: {name}")
                    bottomedCards = []
                    for y in range(playerBottoms[x]):
                        # place as many hand cards as needed into the library list at the 0 position and remove from the hand list

                        # CHECK TO MAKE SURE YOU DONT BOTTOM THE SAME CARD MULTIPLE TIMES

                        bottom = int(input(f"Card {y + 1}:"))
                        library.insert(0, hand.pop(bottom - 1))
                    # push the changes to the database
                    for y in range(len(library)):
                        for card in decks[x]:
                            if card.id == library[y].id:
                                card.location == 'library'
                                card.position == y
                    for y in range(len(hand)):
                        for card in decks[x]:
                            if card.id == hand[y].id:
                                card.location == 'hand'
                                card.position == ''
                playerReady[x] == True
        if not anyMulligans:
            break

# Draw opening hands for both
for x in range(len(decks)):
    draw_library_hand(x, 7)

# process mulligans
mulligan(decks)

turn_number = 0
active_player_index = starting_player_index

pass_priority = {}
pass_active_priority = {}
for x in range(len(players)):
    pass_priority.update({x:True})
    pass_active_priority.update({x:False})

mana_pool = []
day_night = 0
priority = None
stack = []
beginning_phase()