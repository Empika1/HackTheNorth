import mido
import time
import pygame.midi
import random

mido.set_backend("mido.backends.portmidi")

out = mido.open_output("LoopBe Internal MIDI")

melodyInstruments = {
    0 : "Piano",
    1 : "Bell",
    2 : "Brass",
    3 : "Bass"
}

def rollMelodyInstrument(intensity):
    di = intensity
    pick = random.choices([0,1,2,3],[1-di, 1-di, di, di])[0]
    return pick
melodyInstrument = rollMelodyInstrument(0)

harmonyInstruments = {
    4 : "Rhodes",
    5 : "Flute",
    6 : "Piano",
    7 : "Strings"
}

def rollHarmonyInstrument(intensity):
    di = intensity
    pick = random.choices([4,5,6,7],[1-di, di, di, 1-di/2])[0]
    return pick
harmonyInstrument = rollHarmonyInstrument(0)

drumInstruments = {
    8 : "Rock",
    9 : "Funk",
    10 : "Jazz",
    11 : "Thrower"
}

drumInstrument = random.randint(7,11)

class Note:
    def __init__(self, note, time, velocity, length): #length of 1 is a quarter note
        self.note = note
        self.time = time
        self.velocity = velocity
        self.length = length

class Timeline:
    def __init__(self, channel, notes):
        self.channel = channel
        self.notes = notes

class Piece:
    def __init__(self, bpms, timelines):
        self.bpms = bpms
        self.timelines = timelines

startTime = time.time() + 1
def init():
    global startTime
    startTime = time.time() + 1

def noteTimeToTime(noteTime, bpms):
    lastBpmNoteTime = 0
    lastBpmTime = 0
    lastBpm = -1
    for bpm in bpms:
        if noteTime >= bpm[1]:
            lastBpmNoteTime = bpm[1]
            if(lastBpm != -1):
                lastBpmTime = bpm[1] * 60 / lastBpm
            else:
                lastBpmTime = 0
            lastBpm = bpm[0]
        else:
            break
    return (noteTime - lastBpmNoteTime) * 60 / lastBpm + lastBpmTime

def stopCurrentNotes(timeline,timelineNum):
    global timelineOnIs, timelineOffIs
    channel = timeline.channel
    notes = timeline.notes
    for i in range(timelineOnIs[timelineNum] - timelineOffIs[timelineNum]):
        currentOffNote = notes[timelineOffIs[timelineNum]]
        out.send(mido.Message('note_off', note=currentOffNote.note, velocity=currentOffNote.velocity, channel=channel))
        timelineOffIs[timelineNum] += 1

def playTimeline(timeline, bpms, timelineOnI, timelineOffI): #kind of a coroutine. yields back to playPiece
    channel = timeline.channel
    notes = timeline.notes

    timelineOnI_ = timelineOnI
    timelineOffI_ = timelineOffI
    
    global startTime
    currentTime = time.time()
    if timelineOffI_ < len(notes):
        currentOffNote = notes[timelineOffI_]
        while currentTime - startTime > noteTimeToTime(currentOffNote.time + currentOffNote.length, bpms):
            out.send(mido.Message('note_off', note=currentOffNote.note, velocity=currentOffNote.velocity, channel=channel))
            timelineOffI_ += 1
            if timelineOffI_ < len(notes):
                currentOffNote = notes[timelineOffI_]
            else:
                break
    else:
        return (timelineOnI_, timelineOffI_, True)
    if timelineOnI_ < len(notes):
        currentOnNote = notes[timelineOnI_]
        while currentTime - startTime > noteTimeToTime(currentOnNote.time, bpms):
            out.send(mido.Message('note_on', note=currentOnNote.note, velocity=currentOnNote.velocity, channel=channel))
            timelineOnI_ += 1
            if timelineOnI_ < len(notes):
                currentOnNote = notes[timelineOnI_]
            else:
                break
    return (timelineOnI_, timelineOffI_, False)

done = False
def playPiece(piece, stopAutomatically = False):
    global done, timelineOnIs, timelineOffIs
    timelines = piece.timelines
    bpms = piece.bpms

    timelineOnIs = [0] * len(timelines)
    timelineOffIs = [0] * len(timelines)
    dones = [False] * len(timelines)
    while True:
        for i in range(len(timelines)):
            timelineOnIs[i], timelineOffIs[i], dones[i] = playTimeline(timelines[i], bpms, timelineOnIs[i], timelineOffIs[i])
        if done or (stopAutomatically and all(dones)):
            break

def stopPlaying(piece):
    global done
    done = True
    for i, timeline in enumerate(piece.timelines):
        stopCurrentNotes(timeline, i)

