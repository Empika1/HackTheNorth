import random
from chords import *

jumpiness = 0

currentMelodyLog = []
savedMelody = []
replayingPos = 0

def findNearestNote(note, iMap):
    octaveFactor = 0
    while note >= 12:
        note -= 12
        octaveFactor += 1
        
    if iMap[note] == 1:
        return note
    else:
        if iMap[note-1] == 1:
            return note-1+octaveFactor*12
        if iMap[note+1] == 1:
            return note+1+octaveFactor*12

def generateNextNote(lastNote, time, chord, key):
    global savedMelody, currentMelodyLog, replayingPos
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
    noteChecking = lastNote + 1
    noteChecking = noteChecking % 12
    while iMap[noteChecking] == 0:
        noteChecking += 1
        noteChecking = noteChecking % 12
    noteChoices.append(noteChecking)
    
    #Prioritize starting on roots
    if time % 4 == 0 or random.random() > creativity/4 + 0.8:
        note = chord[0]
        if note + 12 - lastNote <= 2:
            note += 12
    
    if time % 16 >= 15 and key == "Minor":
        noteChoices.append(11)
    
    if time % 16 >= 15 and key == "Major":
        noteChoices.append(10)
    
    if note == 99:
        while note - lastNote > 4:
            note = random.choice(noteChoices)
    
    if time % 16 < 4:
        currentMelodyLog.append(note)
    elif len(savedMelody) == 0 and time % 16 < 8:
        savedMelody = currentMelodyLog
    if time % 16 < 12 and time % 16 >= 8:
        note = findNearestNote(chord[0] + savedMelody[replayingPos], iMap)
        replayingPos += 1
    
    return note