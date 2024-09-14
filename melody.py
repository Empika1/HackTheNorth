import random
from chords import *

jumpiness = 0

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
        if random.random() < 0.05 + creativity/2:
            noteChoices.append(noteChecking)
    
    # Key steps
    # noteChecking = lastNote + 1
    # if noteChecking >= len(iMap) - 1:
    #     noteChecking = 0
    # if noteChecking < 0:
    #     noteChecking = 12 - noteChecking
    # while iMap[noteChecking] == 0:
    #     noteChecking += 1
    #     if noteChecking >= len(iMap) - 1:
    #         noteChecking = 0
    #     if noteChecking < 0:
    #         noteChecking = 12 - noteChecking
    # noteChoices.append(noteChecking)
    
    #Prioritize starting on roots
    if time % 4 == 0 or random.random() > creativity/4 + 0.8:
        note = chord[0]
    
    if time % 16 >= 15 and key == "Minor":
        noteChoices.append(11)
    
    if time % 16 >= 15 and key == "Major":
        noteChoices.append(10)
    
    if note == 99:
        note = random.choice(noteChoices)
    
    return note