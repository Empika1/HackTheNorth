from music import *

#Drumloops are ordered from least intense to most intense
#They are stored as 2D arrays where the array length is the beat divisor
#So an array of length 4 means each beat is a quarter note
#Ordered as 0 = Kick, 1 = Snare, 2 = Hat, 3 = Crash

drumLoops = {
    "OneKick" : [[1]],
    "FourKicks" : [[1,1,1,1]],
    "Basic" : [[1,1,1,1],[0,1,0,1]],
    "HatOffbeat" : [[1,1,1,1],[0,1,0,1],[0,1,0,1,0,1,0,1]],
    "Hats" : [[1,1,1,1],[0,1,0,1],[1,1,1,1,1,1,1,1]],
    "FullRock" : [[1,1,1,1],[0,1,0,1],[1,1,1,1,1,1,1,1],[1]],
    "Flat" : [[1,0,0,1,1,0,0,0],[0,1,0,1],[0,1,0,1,0,1,0,1]],
    "BigRoll" : [[1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1],[1,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0],[0],[1]]
}

drumOutputs = [35, 38, 44, 49]

def pasteDrumLoop(id, timeline, time):
    loop = drumLoops[id]
    for beat in range(32):
        for track in range(len(loop)):
            if beat % (32 / len(loop[track])) == 0 and loop[track][int(beat / (32 / len(loop[track])))] == 1: 
                timeline.notes.append(Note(drumOutputs[track], time + beat/8, 70, 1))