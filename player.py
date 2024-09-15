import random
import threading
import time
import tkinter as tk
from tkinter import ttk
import rhythm
from rhythm import generateMelodyRhythm
import music
from music import Note, Timeline, Piece, noteTimeToTime, playPiece, init, stopPlaying
import chords
from chords import getNotesFromChord
import melody
from melody import generateNextNote
import sv_ttk
import drums

# Create the main window
root = tk.Tk()
root.title("AutOST")

sv_ttk.set_theme("dark")

sliders = ["Syncopation", "Speed", "Sporadicness", "Dissonance", "Creativity", "Majorness", "Jumpiness"]

def onSyncopationChange(value):
    rhythm.syncopation = float(value) / 100

def onSpeedChange(value):
    print(value)
    rhythm.speed = float(value) / 100

def onSporadicnessChange(value):
    rhythm.sporadicness = float(value) / 100

def onDissonanceChange(value):
    chords.dissonance = float(value) / 100

def onCreativityChange(value):
    chords.creativity = float(value) / 100

def onMajornessChange(value):
    chords.majorness = float(value) / 100

def onJumpinessChange(value):
    pass

functions = [
    onSyncopationChange,
    onSpeedChange,
    onSporadicnessChange,
    onDissonanceChange,
    onCreativityChange,
    onMajornessChange,
    onJumpinessChange
]

for i in functions:
    i(0)

# Create a frame to hold the sliders
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#add the sliders
for(i, slider) in enumerate(sliders):
    function = functions[i]
    ttk.Label(root, text=slider).grid(row=i, column=0, padx=5, pady=5)
    slider = ttk.Scale(root, from_=0, to=100, orient='horizontal')
    slider.bind("<ButtonRelease-1>", lambda _, function_=function, slider_=slider: function_(slider_.get()))
    slider.grid(row=i, column=1, padx=5, pady=5)

timeline1 = Timeline(0, [])
timeline2 = Timeline(1, [])
timeline3 = Timeline(2, [])
piece = Piece([(120, 0)], [timeline1, timeline2, timeline3])

def editMusic():
    global timeline1, timeline2, timeline3, piece, done

    #general vars
    currentBeat = 0
    currentBar = 0
    current4Bar = 0

    oldDissonance = chords.dissonance
    oldCreativity = chords.creativity
    oldMajorness = chords.majorness

    #melody rhythm vars
    melodyBuffer = 0.75 #seconds
    nextRhythmBarToGenerate = 0

    #chord vars
    chordBuffer = 0.25
    progressions = [chords.generateProgression()] #last progression is the currently playing one
    nextChordBarToGenerate = 0
    rootNote = 44 + random.randint(0,7)

    #melody vars
    melodyBuffer = 0.5
    nextNoteToGenerateIndex = 0

    #drum vars
    drumBuffer = 0.25
    nextDrumBarToGenerate = 0

    while not done:
        #general
        #print("1", progressions)
        currentTime = 0
        timeInto = 0
        currentBeat = 0
        currentBar = 0
        current4Bar = 0
        #print("2", progressions)
        def getTimes(): #if i want to call this multiple times in the loop?
            nonlocal currentTime, timeInto, currentBeat, currentBar, current4Bar
            #print("3", progressions)
            currentTime = time.time() #avoids weird shit
            #print("4", progressions)
            timeInto = currentTime - music.startTime
            #print("5", progressions)
            while timeInto > noteTimeToTime(currentBeat, piece.bpms):
                #print("6", progressions)
                currentBeat += 1
            #print("7", progressions)
            currentBar = currentBeat // 4
            #print("8", progressions)
            current4Bar = currentBar // 4
        getTimes()

        oldDissonance = chords.dissonance
        oldCreativity = chords.creativity
        oldMajorness = chords.majorness

        #print("9", progressions)

        #add melody rhythm
        if timeInto + melodyBuffer >= noteTimeToTime(nextRhythmBarToGenerate * 4, piece.bpms):
            #print("10", progressions)
            nextRhythmBarToGenerate += 1
            #print("11", progressions)
            nextRhythm = generateMelodyRhythm()
            #print("12", progressions)
            for j in range(len(nextRhythm)):
                #print("13", progressions)
                noteLen = (nextRhythm[j + 1] if j < len(nextRhythm) - 1 else 4) - nextRhythm[j]
                #print("14", progressions)
                note = Note(60, nextRhythm[j] + currentBar * 4, 70, noteLen)
                #print("15", progressions)
                timeline1.notes.append(note)
                #print("16", progressions)
            chordNotes = getNotesFromChord(progressions[-1][nextChordBarToGenerate % 4])
            #print("17", progressions)
        #print("18", progressions)
        
        #add chords   
        if timeInto + chordBuffer >= noteTimeToTime(nextChordBarToGenerate * 4, piece.bpms):
            #print("19", progressions)
            nextChordBarToGenerate += 1
            #print("20", progressions)
            chordNotes = getNotesFromChord(progressions[-1][nextChordBarToGenerate % 4])
            #print("21", progressions)
            noteTime = nextChordBarToGenerate * 4
            #print("22", progressions)
            note = Note(rootNote + chordNotes[0], noteTime, 55, 4)
            #print("23", progressions)
            timeline2.notes.append(note)
            #print("24", progressions)
            note = Note(rootNote + chordNotes[1], noteTime, 55, 4)
            #print("25", progressions)
            timeline2.notes.append(note)
            #print("26", progressions)
            note = Note(rootNote + chordNotes[2], noteTime, 55, 4)
            #print("27", progressions)
            timeline2.notes.append(note)
            #print("28", progressions)
        #print("29", progressions)

        #add melody
        if nextNoteToGenerateIndex <= len(timeline1.notes) - 1:
            #print("30", progressions)
            thisNoteO = timeline1.notes[nextNoteToGenerateIndex]
            #print("31", progressions)
            if (len(timeline1.notes) > 0 and timeInto + melodyBuffer >= noteTimeToTime(thisNoteO.time, piece.bpms)):
                #print("32", progressions)
                lastNoteO = None
                #print("33", progressions)
                try:
                    lastNoteO = timeline1.notes[nextNoteToGenerateIndex - 1]
                    #print("34", progressions)
                except:
                    #print("35", progressions)
                    pass
                #print("36", progressions)

                lastNote = lastNoteO.note - 12 - rootNote if lastNoteO else 99
                #print("37", progressions)
                chordNotes = chords.getNotesFromChord(progressions[-1][int(thisNoteO.time % 4)])
                #print("38", progressions)
                thisNote = generateNextNote(lastNote, thisNoteO.time, chordNotes, chords.key)
                #print("39", progressions)
                thisNoteO.note = thisNote + 12 + rootNote
                #print("40", progressions)
                nextNoteToGenerateIndex += 1
                #print("41", progressions)
        #print("42", progressions)

        #add drums
        if timeInto + drumBuffer >= noteTimeToTime(nextDrumBarToGenerate * 4, piece.bpms):
            nextDrumBarToGenerate += 1
            drums.pasteDrumLoop("FullRock", timeline3, nextDrumBarToGenerate*4)

def play():
    global timeline1, piece
    init()
    playPiece(piece)

done = False
def on_closing():
    global editThread, playThread, done
    done = True
    root.destroy()
    editThread.join()
    stopPlaying()
    playThread.join()

root.protocol("WM_DELETE_WINDOW", on_closing)

random.seed(0)
editThread = threading.Thread(target=editMusic)
editThread.start()

playThread = threading.Thread(target=play)
playThread.start()

root.mainloop()