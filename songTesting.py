from music import *
from chords import *
from drums import *
import random

timeline1 = Timeline(0, [])
timeline2 = Timeline(1, [])
timeline3 = Timeline(3, [])
progression = generateProgression()


intensity = 0
#for i in range(40):
    #timeline2.notes.append(Note(36, i, 70, 1))

piece = Piece([(120, 0)], [timeline1, timeline2, timeline3])

pasteDrumLoop("FullRock", timeline3, 0)
pasteDrumLoop("FullRock", timeline3, 4)
pasteDrumLoop("FullRock", timeline3, 8)
pasteDrumLoop("FullRock", timeline3, 12)

for i in range(4):
    notes = getNotesFromChord(progression[i%4])
    noteTime = 0 if len(timeline1.notes) == 0 else timeline1.notes[-1].time + timeline1.notes[-1].length
    note = Note(48 + notes[0], noteTime, 35 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), 4)
    timeline1.notes.append(note)
    note = Note(48 + notes[1], noteTime, 35 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), 4)
    timeline1.notes.append(note) 
    note = Note(48 + notes[2], noteTime, 35 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), 4)
    timeline1.notes.append(note)

playPiece(piece)