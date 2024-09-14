from music import *
import random

rhythms = [ #1 bar rhythm patterns
    [4],
    [2, 2],
    [3, 1],
    [1, 3],
    [2, 1, 1],
    [1, 1, 2],
    [1, 2, 1],
    [1, 1, 1, 1],
    [1.5, 1.5, 1],
    [1, 1, 1, 0.5, 0.5],
    [0.5, 0.5, 1, 1, 1],
    [1, 1, 0.5, 0.5, 1],
    [1, 0.5, 0.5, 1, 1],
    [1, 1, 0.5, 0.5, 0.5, 0.5],
    [0.5, 0.5, 1, 0.5, 0.5, 1],
    [0.5, 0.5, 0.5, 0.5, 1, 1],
    [1, 0.5, 0.5, 1, 0.5, 0.5],
    [1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1],
    [0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5],
    [0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5],
    [0.5, 1, 0.5, 1, 1],
    [1, 1, 0.5, 1, 0.5],
    [0.5, 1, 0.5, 0.5, 1, 0.5],
    [1, 0.5, 1, 0.5, 1],
]

intensity = 0
def generateMelodyRhythm():
    global rhythms, intensity

    allowedVariance = 0.1
    retries = 10

    for i in range(retries):
        potentialIndex = random.randint(0, len(rhythms) - 1)
        indexIntensity = potentialIndex / (len(rhythms) - 1)
        if abs(indexIntensity - intensity) <= allowedVariance or i == retries - 1:
            return rhythms[potentialIndex]
    
timeline1 = Timeline(0, [])
timeline2 = Timeline(1, [])
for i in range(40):
    timeline2.notes.append(Note(36, i, 70, 1))
piece = Piece([(120, 0)], [timeline1, timeline2])
for i in range(10):
    rhythm = generateMelodyRhythm()
    for j in range(len(rhythm)):
        noteTime = 0 if len(timeline1.notes) == 0 else timeline1.notes[-1].time + timeline1.notes[-1].length
        note = Note(60, noteTime, 50 + (5 if noteTime % 4 == 0 else 0) + (5 if noteTime % 2 == 0 else 0), rhythm[j])
        timeline1.notes.append(note)
    intensity += 0.1
playPiece(piece)