import mido
import time
import pygame.midi

mido.set_backend("mido.backends.portmidi")

out = mido.open_output("LoopBe Internal MIDI")

class Note:
    def __init__(self, note, time, velocity, length): #length of 1 is a quarter note
        self.note = note
        self.time = time
        self.velocity = velocity
        self.length = length

class Timeline:
    def __init__(self, channel, notes = []):
        self.channel = channel
        self.notes = notes

class Piece:
    def __init__(self, bpms = [], timelines = []):
        self.bpms = bpms
        self.timelines = timelines

startTime = time.time()
def init():
    global startTime
    startTime = time.time()

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

def playTimeline(timeline, bpms, timelineOnI, timelineOffI): #kind of a coroutine. yields back to playPiece
    channel = timeline.channel
    notes = timeline.notes

    global startTime
    currentTime = time.time()
    if timelineOnI < len(notes):
        currentOnNote = notes[timelineOnI]
        if currentTime - startTime >= noteTimeToTime(currentOnNote.time, bpms):
            out.send(mido.Message('note_on', note=currentOnNote.note, velocity=currentOnNote.velocity, channel=channel))
            timelineOnI += 1
    if timelineOffI < len(notes):
        currentOffNote = notes[timelineOffI]
        if currentTime - startTime >= noteTimeToTime(currentOffNote.time + currentOffNote.length, bpms):
            out.send(mido.Message('note_off', note=currentOffNote.note, velocity=currentOffNote.velocity, channel=channel))
            timelineOffI += 1
    else:
        return (timelineOnI, timelineOffI, True)
    return (timelineOnI, timelineOffI, False)

done = False
def playPiece(piece, stopAutomatically = False):
    global done
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

def stopPlaying():
    global done
    done = True

