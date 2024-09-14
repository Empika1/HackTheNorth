import random
from sympy.utilities.iterables import multiset_permutations
import math

#all from 0 to 1
speed = 0
syncopation = 0
sporadicness = 0 #0 = very repetitive, 1 = very sporadic

def determineNotePulse(noteTime): #higher number = more syncopation
    epsilon = 0.0001
    for i in range(1, 7):
        if abs(noteTime % (4 / 2 ** i)) < epsilon:
            return i
    return 7    

def determineSyncopation(rhythm): #takes 1 beat rhythm
    totalSyncopation = 0
    for i in range(len(rhythm)):
        notePulse = determineNotePulse(rhythm[i])
        noteLength = (rhythm[i + 1] if i < len(rhythm) - 1 else 4) - rhythm[i]
        noteLengthMultiplier = math.log2(noteLength) + 3
        totalSyncopation += (notePulse * noteLengthMultiplier) ** 2
    return totalSyncopation

def determineSpeed(rhythm): #takes 1 beat rhythm
    shortestNoteLength = 4
    for i in range(len(rhythm)):
        noteLength = (rhythm[i + 1] if i < len(rhythm) - 1 else 4) - rhythm[i]
        shortestNoteLength = min(shortestNoteLength, noteLength)
    totalSpeed = 0
    for i in range(len(rhythm)):
        noteLength = (rhythm[i + 1] if i < len(rhythm) - 1 else 4) - rhythm[i]
        if noteLength == shortestNoteLength:
            totalSpeed += 1 / shortestNoteLength
    return totalSpeed

def all4BeatRhythms(divisor):
    rhythmsUnformatted = []
    numThings = round(4 / divisor - 1)
    for divisions in range(1, numThings + 1):
        things = ['|*'] * divisions + ['*'] * (numThings - divisions)
        rhythmsUnformatted += list(multiset_permutations(things))
    rhythms = []
    rhythms.append([0]) #not added otherwise
    for rhythmUnjoined in rhythmsUnformatted:
        rhythm = []
        rhythm.append(0)
        for i in range(len(rhythmUnjoined)):
            if rhythmUnjoined[i] == '|*':
                rhythm.append(i * divisor + divisor)
        rhythms.append(rhythm)
    # rhythms = list(set(map(tuple, rhythms)))
    # print(rhythms[-1])
    return rhythms

rhythms = [(i, determineSyncopation(i), determineSpeed(i)) for i in all4BeatRhythms(0.25)]
minSyncopation = min(rhythms, key=lambda x: x[1])[1]
maxSyncopation = max(rhythms, key=lambda x: x[1])[1]
minSpeed = min(rhythms, key=lambda x: x[2])[2]
maxSpeed = max(rhythms, key=lambda x: x[2])[2]

# file = open("rhythms.txt", "a")
# for i in rhythms:
#     print(i, file=file)
# print("~~", file=file)
# rhythms.sort(key=lambda x: x[1])
# for i in rhythms:
#     print(i, file=file)
# print("~~", file=file)
# rhythms.sort(key=lambda x: x[2])
# for i in rhythms:
#     print(i, file=file)

def generateMelodyRhythm():
    global rhythms, syncopation, speed, minSyncopation, maxSyncopation, minSpeed, maxSpeed
    print(speed, syncopation)

    initialAllowedSyncopationVariance = 0
    initialAllowedSpeedVariance = 0
    retries = 100000

    for i in range(retries + 1):
        allowedSyncopationVariance = (initialAllowedSyncopationVariance * (1 - i / retries) + 1 * (i / retries)) ** 4
        allowedSpeedVariance = (initialAllowedSpeedVariance * (1 - i / retries) + 1 * (i / retries)) ** 4

        potentialIndex = random.randint(0, len(rhythms) - 1)
        indexSyncopation = (rhythms[potentialIndex][1] - minSyncopation) / (maxSyncopation - minSyncopation)
        indexSpeed = (rhythms[potentialIndex][2] - minSpeed) / (maxSpeed - minSpeed)
        if (abs(indexSyncopation - syncopation) <= allowedSyncopationVariance and
            abs(indexSpeed - speed) <= allowedSpeedVariance):
            # print(allowedSyncopationVariance, allowedSpeedVariance)
            return rhythms[potentialIndex][0]

phrases = [
    "AAAA",
    # "AABB",
    # "ABAB",
    # "ABAC",
    # "AABC",
    # "ABCD"
]

def generate4BarRhythm():
    global sporadicness, phrases

    initialAllowedRepetitivenessVariance = 0

    phrase = None
    retries = 15
    for i in range(retries + 1):
        allowedVariance = (initialAllowedRepetitivenessVariance * (1 - i / retries) + 1 * (i / retries)) ** 3
        potentialIndex = random.randint(0, len(phrases) - 1)
        if (abs(potentialIndex / len(phrases) - sporadicness) <= allowedVariance):
            phrase = phrases[potentialIndex]
            break
    rhythm = []
    melodiesForPhrases = {}
    for i in range(len(phrase)):
        if phrase[i] not in melodiesForPhrases:
            melodiesForPhrases[phrase[i]] = generateMelodyRhythm()
        rhythm += [x + i * 4 for x in melodiesForPhrases[phrase[i]]]
    return rhythm

# timeline1 = Timeline(0, [])
# timeline2 = Timeline(1, [])
# piece = Piece([(120, 0)], [timeline1, timeline2])
# for i in range(160):
#     timeline2.notes.append(Note(36, i, 120, 1))
# for i in range(10):
#     rhythm = generate4BarRhythm()
#     for j in range(len(rhythm)):
#         noteLen = (rhythm[j + 1] if j < len(rhythm) - 1 else 16) - rhythm[j]
#         note = Note(60, rhythm[j] + 16 * i, 70, noteLen)
#         timeline1.notes.append(note)
# init()
# playPiece(piece)