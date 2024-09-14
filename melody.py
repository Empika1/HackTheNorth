import random
from chords import *

def generateNextNote(lastNote, time, chord, key):
    noteChoices = chord
    note = 99
    
    if key == "Major":
        iMap = majorKeyIntervalMap
    else:
        iMap = minorKeyIntervalMap
    
    noteChecking = random.randrange(0,12)
    while iMap[noteChecking] == 0:
        noteChecking = random.randrange(0,12)
    
    if noteChecking not in chord:
        if random.random() < 0.15 + creativity/2:
            noteChoices.append(noteChecking)
    
    #Prioritize starting on roots
    if time % 4 == 0:
        note = chord[0]
    
    if time % 4 >= 3 and key == "Minor":
        noteChoices.append(11)
    
    if time % 4 >= 3 and key == "Major":
        noteChoices.append(10)
    
    if note == 99:
        note = random.choice(noteChoices)
    
    return note