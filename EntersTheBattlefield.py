import sqlite3
con = sqlite3.connect("mtgopen.db")
db = con.cursor()

def CavernofSouls(**kwargs):
    creatureType = input("Please enter a creature type:")
    print(f"Chosen creature type is {creatureType}")
    return False

def KnightErrantofEos(**kwargs):
    "Look at the top 6 cards of ur library, reveal up to 2 creature cards with mana value C or less where X is the number of creatures that convoked this card"

def IntrepidAdversary(**kwargs):
    "may pay {1}{W} anytnumber of times, to put on valor counters"

def BrutalCathar(**kwargs):
    "exile creature till leaves"