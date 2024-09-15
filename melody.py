import random
from chords import *

jumpiness = 0
repetetiveness = 0

currentMelodyLog = []
#Not working yet obv
savedMelodies = [
    
    #Beginning motif, plays at the start of progressions
    [],
    
    #Second bar first note
    99,
    
    #Ending motif first half
    [],
    
    #Ending motif second half
    []
]

def saveMelodicPhrase(noteList, slot):
    savedMelodies[slot] = noteList

currentPhrase = []

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

def generateNextNote(lastNote, time, chord, key, nextChord, speed):
    global currentPhrase, savedMelodies
    #Add in the notes from the current chord (always playable)
    noteChoices = chord
    note = 99
    if time % 32 == 0: 
        currentPhrase = []
        savedMelodies = [[],[],[],[]]
    if time % 16 == 4 and len(currentPhrase) > 0:
        saveMelodicPhrase(currentPhrase, 0)
        currentPhrase = []
    
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
    # noteChecking = lastNote + 1
    # noteChecking = noteChecking % 12
    # while iMap[noteChecking] == 0:
    #     noteChecking += 1
    #     noteChecking = noteChecking % 12
    # noteChoices.append(noteChecking)
    
    # while random.random() < speed*2/3:
    #     #noteChoices.append(noteChecking)
    #     noteChoices.append(lastNote)

    if time % 4 >= 3:
        noteChoices.append(int((chord[0]+nextChord[0])/2))
        noteChoices.append(int((chord[0]+nextChord[0])/2))
        
    if note == 99:
        note = random.choice(noteChoices)
        if note - lastNote > 6 + int(jumpiness*6):
            note = random.choice(noteChoices)
    
    if time % 16 < 4 and len(savedMelodies[0]) > 0:
        note = savedMelodies[0][0]
        savedMelodies[0].pop(0)
        print(savedMelodies)
    else:
        currentPhrase.append(note)
    
    if time % 16 == 4 and savedMelodies[1] == 99:
        savedMelodies[1] = note
    else:
        while note == savedMelodies[1]:
            note = random.choice(noteChoices)
    
    if time % 32 >= 28:
        note = 0
    return note