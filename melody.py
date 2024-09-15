import random
from chords import *

jumpiness = 0
repetetiveness = 0

currentMelodyLog = []
#Not working yet obv
savedMelodies = [
    [],
    [],
    [],
    []
]
replayingPos = 0
loopedMelody = []

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

def generateNextNote(lastNote, time, chord, key, nextChord):
    global savedMainMelody, currentMelodyLog, replayingPos, savedSecondaryMelody, loopedMelody
    #Add in the notes from the current chord (always playable)
    noteChoices = chord
    note = 99
    
    #Set the interval map to remove notes not in key
    if key == "Major":
        iMap = majorKeyIntervalMap
    else:
        iMap = minorKeyIntervalMap
    
    #Essentially find a random note in the key and maybe add it to the list of possible notes
    noteChecking = random.randrange(0,12)
    while iMap[noteChecking] == 0:
        noteChecking = random.randrange(0,12)
    
    if noteChecking not in chord:
        if random.random() < 0.15 + creativity/2 + dissonance:
            noteChoices.append(noteChecking)
    
    # Key steps
    noteChecking = lastNote + 1
    noteChecking = noteChecking % 12
    while iMap[noteChecking] == 0:
        noteChecking += 1
        noteChecking = noteChecking % 12
    noteChoices.append(noteChecking)

    if time % 4 >= 3:
        noteChoices.append(int((chord[0]+nextChord[0])/2))
    
    if note == 99:
        while note - lastNote > 4:
            note = random.choice(noteChoices)
    
    return note