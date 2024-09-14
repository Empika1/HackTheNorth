import random
from chords import *

def generateNextNote(lastNote, time, chord, key):
    note = random.choice(chord)
    
    #Prioritize starting on roots
    if time % 4 == 0:
        note = 0
    
    #If creativity is high reroll same notes
    if lastNote == note:
        if random.random() < creativity:
            note = random.choice(chord)
    
    if key == "Major":
        iMap = majorKeyIntervalMap
    else:
        iMap = minorKeyIntervalMap
    
    noteChecking = 1
    while iMap[noteChecking] == 0 and random.random() > dissonance:
        noteChecking = random.randrange(0,12)
    
    if noteChecking not in chord:
        if random.random() < 0.5 + creativity/2:
            note = noteChecking
    
    return note