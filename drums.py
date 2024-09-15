from music import *

#Drumloops are ordered from least intense to most intense
#They are stored as 2D arrays where the array length is the beat divisor
#So an array of length 4 means each beat is a quarter note
#Ordered as 0 = Kick, 1 = Snare, 2 = Hat, 3 = Crash

intensity = 0

drumLoops = [
    [[1]],
    [[1,1,1,1]],
    [[1,1,1,1],[0,1,0,1]],
    [[1,1,1,1],[0,1,0,1],[0,1,0,1,0,1,0,1]],
    [[1,1,1,1],[0,1,0,1],[1,1,1,1,1,1,1,1]],
    [[1,0,0,1,1,0,0,0],[0,1,0,1],[0,1,0,1,0,1,0,1]],
    [[1,1,1,1],[0,1,0,1],[1,1,1,1,1,1,1,1],[1]],
    [[1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0],[0],[1]]
]

drumOutputs = [35, 38, 44, 49]

def chooseDrumLoop():
    pick = int(intensity * (len(drumLoops)-1))
    if pick != len(drumLoops)-1 and pick != 0:
        pick += random.randint(0,2)-1
    return drumLoops[pick]

def pasteDrumLoop(loop, timeline, time):
    for beat in range(32):
        for track in range(len(loop)):
            if beat % (32 / len(loop[track])) == 0 and loop[track][int(beat / (32 / len(loop[track])))] == 1: 
                timeline.notes.append(Note(drumOutputs[track], time + beat/8, 70, 1))