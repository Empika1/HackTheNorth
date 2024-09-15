from music import *
import random

#ALL 0-1
dissonance = 0
creativity = 0.5
majorness = 0

sampleMinorProgressions = [
    
]

sampleMajorProgressions = [
    
]

key = random.choices(["Major","Minor"],[majorness,1-majorness])[0]
# if key == "Major":
#     majorPreference = 1
#     1-majorness = 0
# if key == "Minor":
#     majorPreference = 0
#     1-majorness = 1

chordList = ["Major", "Minor", "Diminished", "Augmented"]
chords = {
    "Major" : [0,4,7],
    "Minor" : [0,3,7],
    "Diminished" : [0,3,6],
    "Augmented" : [0,4,8]
}

majorKeyChordMap = ["Major", "Any", "Minor", "Any", "Minor", "Major", "Any", "Major", "Any", "Minor", "Any", "Minor"]
minorKeyChordMap = ["Minor", "Any", "Minor", "Major", "Any", "Minor", "Any", "Minor", "Major", "Any", "Major", "Any"]

majorKeyIntervalMap = [1,0,1,0,1,1,0,1,0,1,0,1]
minorKeyIntervalMap = [1,0,1,1,0,1,0,1,1,0,1,0]

def capNote(note):
    if note >= 12:
        note -= 12
    return note

def findChordWeightings(interval):
    
    majorWeight = 0
    minorWeight = 0
    dimWeight = 0
    augWeight = 0
    
    if majorKeyChordMap[interval] == "Major":
        majorWeight += majorness
    if majorKeyChordMap[interval] == "Minor":
        minorWeight += majorness
        
    if minorKeyChordMap[interval] == "Major":
        majorWeight += 1-majorness
    if minorKeyChordMap[interval] == "Minor":
        minorWeight += 1-majorness
        
    if majorWeight + minorWeight == 0:
        majorWeight = 1
        minorWeight = 1
        
    dimWeight = minorWeight * dissonance/2
    augWeight = majorWeight * dissonance/2
    
    return [majorWeight, minorWeight, dimWeight, augWeight]
    
def pickChordType(interval):
    weights = findChordWeightings(interval)
    pick = random.choices(chordList, weights)[0]
    return pick

def convertChordToWeight(interval, positionInProgression, quality):
    pip = positionInProgression
    
    weight = 0 
    
    c = creativity
    d = dissonance
    ma = majorness
    mi = 1-majorness
    
    presets = {
        "greatPick" : 2-d/2,
        "decentPick" : 1.5-d/4-c/4,
        "boringPick" : 0.75-c/4,
        "unlikelyPick" : 0+d/4+c/4,
        "creativePick" : 0+c*2,
        "badCreativePick" : 0+c/2,
        "dissonantPick" : 0+d/2,
        "badDissonantPick" : 0+d/4
    }
    
    abbreviationsToPresets = {
        "g" : "greatPick",
        "e" : "decentPick",
        "b" : "boringPick",
        "c" : "creativePick",
        "bc" : "badCreativePick",
        "d" : "dissonantPick",
        "bd" : "badDissonantPick",
        "u" : "unlikelyPick",
    }
    
    weight += presets[abbreviationsToPresets[quality]]

    weight -= (majorness * (1-majorKeyIntervalMap[interval])) * (1-d)
    weight -= (1-majorness * (1-majorKeyIntervalMap[interval])) * (1-d)
        
    if weight < 0:
        weight = 0
        
    return weight
        
    
    

def makeMegaWeightMap():

    megaWeightMapMajorQualities = [
        #this is gibberish and completely subjective
        ["g", "bd", "c", "d", "c", "c", "bd", "c", "bd", "d", "bd", "bd"],
        ["b", "bd", "c", "d", "c", "g", "bd", "e", "d", "c", "d", "c"],
        ["b", "bd", "c", "d", "c", "e", "bd", "g", "d", "u", "bd", "bd"],
        ["e", "bd", "c", "d", "u", "g", "bd", "g", "d", "u", "d", "d"]
    ]
    
    megaWeightMapMinorQualities = [
        #this is gibberish and completely subjective
        ["g", "bd", "c", "c", "d", "c", "bd", "c", "bd", "d", "d", "bd"],
        ["b", "bd", "c", "g", "d", "e", "bd", "g", "c", "d", "c", "bd"],
        ["b", "bd", "c", "e", "d", "e", "bd", "e", "c", "d", "c", "bd"],
        ["b", "bd", "c", "e", "d", "e", "bd", "g", "c", "d", "c", "d"]
    ]
    
    if key == "Major":
        megaMap = megaWeightMapMajorQualities
    if key == "Minor":
        megaMap = megaWeightMapMinorQualities
    
    megaWeightMap = []
    
    for i in range(0,len(megaMap)):
        
        tempList = []
        
        for j in range(0,len(megaMap[i])):
            
            tempList.append(convertChordToWeight(j, i, megaMap[i][j]))
            
        megaWeightMap.append(tempList)

    return megaWeightMap
            
            
            


def decideNextChord(currentChordInterval, currentChordType, nextPositionInProgression):
    megaMap = makeMegaWeightMap()
    weights = megaMap[nextPositionInProgression]
    
    options = [0,1,2,3,4,5,6,7,8,9,10,11]
    pick = random.choices(options, weights)[0]
    if pick == currentChordInterval and random.randrange(0,10) > (creativity*10):
        pick = random.choices(options, weights)[0]
    chordType = pickChordType(pick)
    return [pick, chordType]

def generateProgression(useSamples = False):
    prog = []
    cur = decideNextChord(0,0,0)
    for i in range(0,3):
        prog.append(cur)
        cur = decideNextChord(cur[0],cur[1],i+1)
    prog.append(cur)
    
    if useSamples == True:
        
        if key == "Major":
            prog = random.choice(sampleMajorProgressions)
            
        if key == "Minor":
            prog = random.choice(sampleMinorProgressions)
    
    return prog

def getNotesFromChord(c):
    chordType = c[1]
    notes = chords[chordType]
    newnotes = []
    for i in range(len(notes)):
        newnotes.append(notes[i] + c[0])
        
    return newnotes