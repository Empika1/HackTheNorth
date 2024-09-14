from music import *
import random

#ALL 0-1
dissonance = 0
creativity = 0
minorPreference = 0
majorPreference = 1

key = random.choices([["Major","Minor"],[majorPreference,minorPreference]])
# if key == "Major":
#     majorPreference = 1
#     minorPreference = 0
# if key == "Minor":
#     majorPreference = 0
#     minorPreference = 1

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

def findChordWeightings(interval):
    
    majorWeight = 0
    minorWeight = 0
    dimWeight = 0
    augWeight = 0
    
    if majorKeyChordMap[interval] == "Major":
        majorWeight += majorPreference
    if majorKeyChordMap[interval] == "Minor":
        minorWeight += majorPreference
        
    if minorKeyChordMap[interval] == "Major":
        majorWeight += minorPreference
    if minorKeyChordMap[interval] == "Minor":
        minorWeight += minorPreference
        
    if majorWeight + minorWeight == 0:
        majorWeight = 1
        minorWeight = 1
        
    dimWeight = minorWeight * dissonance
    augWeight = majorWeight * dissonance
    
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
    ma = majorPreference
    mi = minorPreference
    
    presets = {
        "greatPick" : 2-d/2,
        "decentPick" : 0.75-d/4-c/4,
        "boringPick" : 1-c/4,
        "unlikelyPick" : 0.25+d/4,
        "creativePick" : 0.25+c/2,
        "badCreativePick" : 0+c/2,
        "dissonantPick" : 0.1+d/2,
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

    weight -= (majorPreference * (1-majorKeyIntervalMap[interval])) * (1-d)
    weight -= (minorPreference * (1-majorKeyIntervalMap[interval])) * (1-d)
        
    if weight < 0:
        weight = 0
        
    return weight
        
    
    

def makeMegaWeightMap():

    megaWeightMapQualities = [
        #this is gibberish and completely subjective
        ["g", "bd", "c", "u", "u", "e", "bd", "e", "bd", "c", "u", "bd"],
        ["b", "bd", "e", "e", "e", "e", "bd", "e", "c", "u", "u", "bd"],
        ["b", "bd", "c", "u", "e", "e", "bd", "e", "c", "u", "u", "bd"],
        ["b", "bd", "c", "u", "e", "e", "bd", "e", "c", "u", "e", "g"]
    ]
    
    megaWeightMap = []
    
    for i in range(0,len(megaWeightMapQualities)):
        
        tempList = []
        
        for j in range(0,len(megaWeightMapQualities[i])):
            
            tempList.append(convertChordToWeight(j, i, megaWeightMapQualities[i][j]))
            
        megaWeightMap.append(tempList)
    
    print(megaWeightMap)
    return megaWeightMap
            
            
            


def decideNextChord(currentChordInterval, currentChordType, nextPositionInProgression):
    megaMap = makeMegaWeightMap()
    weights = megaMap[nextPositionInProgression]
    
    options = [0,1,2,3,4,5,6,7,8,9,10,11]
    pick = random.choices(options, weights)[0]
    chordType = pickChordType(pick)
    return [pick, chordType]

def generateProgression():
    prog = []
    cur = decideNextChord(0,0,0)
    for i in range(0,3):
        prog.append(cur)
        cur = decideNextChord(cur[0],cur[1],i+1)
    prog.append(cur)
    
    return prog

def getNotesFromChord(c):
    chordType = c[1]
    notes = chords[chordType]
    for i in range(len(notes)):
        notes[i] += c[0]
        
    return notes

progression = generateProgression()

for i in range(len(progression)):
    chord = progression[i]
    print(getNotesFromChord(chord))