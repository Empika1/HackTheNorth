from music import *
from chords import *
from drums import *
from rhythm import *
import random
from melody import *

rootNote = 40 + random.randint(0,7)

timeline1 = Timeline(0, []) 
timeline2 = Timeline(1, [])
timeline3 = Timeline(3, [])
progression = generateProgression()

intensity = 0
#for i in range(40):
    #timeline2.notes.append(Note(36, i, 70, 1))

piece = Piece([(random.randint(85,110), 0)], [timeline1, timeline2, timeline3])

for i in range(8):
    pasteDrumLoop("FullRock", timeline3, i*4)

rhythms = [generateMelodyRhythm(),generateMelodyRhythm()]

for i in range(8):
    notes = getNotesFromChord(progression[i%4])
    noteTime = 0 if len(timeline2.notes) == 0 else timeline2.notes[-1].time + timeline2.notes[-1].length
    note = Note(rootNote + notes[0], noteTime, 35 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), 4)
    timeline2.notes.append(note)
    note = Note(rootNote + notes[1], noteTime, 35 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), 4)
    timeline2.notes.append(note) 
    note = Note(rootNote + notes[2], noteTime, 35 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), 4)
    timeline2.notes.append(note)
    
    #MELODY
    lastNote = 99
    rhythm = rhythms[i%2]
    for j in range(len(rhythm)):
        noteLen = (rhythm[j + 1] if j < len(rhythm) - 1 else 4) - rhythm[j]
        nextNote = generateNextNote(lastNote, rhythm[j] + 4 * i, notes, key)
        note = Note(rootNote + 12 + nextNote, rhythm[j] + 4 * i, 70, noteLen)
        lastNote = nextNote
        timeline1.notes.append(note)
        
init()
playPiece(piece, True)