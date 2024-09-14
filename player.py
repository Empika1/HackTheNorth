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
import sv_ttk

# Create the main window
root = tk.Tk()
root.title("AutOST")

sv_ttk.set_theme("dark")

sliders = ["Syncopation", "Speed", "Sporadicness", "Dissonance", "Creativity", "Majorness", "Jumpiness"]

def onSyncopationChange(value):
    rhythm.syncopation = float(value) / 100

def onSpeedChange(value):
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
    slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=function)
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

    #melody rhythm vars
    melodyBuffer = 0.5 #seconds
    nextRhythmBarToGenerate = 0

    #chord vars
    chordBuffer = 0.25 #seconds
    progressions = [chords.generateProgression()] #last progression is the currently playing one
    nextChordBarToGenerate = 0
    rootNote = 44 + random.randint(0,7)

    #melody vars

    #drum vars

    while not done:
        #general
        currentTime = 0
        timeInto = 0
        currentBeat = 0
        currentBar = 0
        current4Bar = 0
        def getTimes(): #if i want to call this multiple times in the loop?
            nonlocal currentTime, timeInto, currentBeat, currentBar, current4Bar
            currentTime = time.time() #avoids weird shit
            timeInto = currentTime - music.startTime
            while timeInto > noteTimeToTime(currentBeat, piece.bpms):
                currentBeat += 1
            currentBar = currentBeat // 4
            current4Bar = currentBar // 4
        getTimes()

        #add melody rhythm
        if timeInto + melodyBuffer >= noteTimeToTime(nextRhythmBarToGenerate * 4, piece.bpms):
            nextRhythmBarToGenerate += 1
            nextRhythm = generateMelodyRhythm()
            for j in range(len(nextRhythm)):
                noteLen = (nextRhythm[j + 1] if j < len(nextRhythm) - 1 else 4) - nextRhythm[j]
                note = Note(60, nextRhythm[j] + currentBar * 4, 70, noteLen)
                timeline1.notes.append(note)
        
        #add chords        
        if timeInto + chordBuffer > noteTimeToTime(nextChordBarToGenerate * 4, piece.bpms):
            nextChordBarToGenerate += 1
            notes = getNotesFromChord(progressions[-1][nextChordBarToGenerate % 4])
            print("chordin")
            noteTime = nextChordBarToGenerate * 4
            note = Note(rootNote + notes[0], noteTime, 55, 4)
            timeline2.notes.append(note)
            note = Note(rootNote + notes[1], noteTime, 55, 4)
            timeline2.notes.append(note) 
            note = Note(rootNote + notes[2], noteTime, 55, 4)
            timeline2.notes.append(note)

        #add melody

        #add drums

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

editThread = threading.Thread(target=editMusic)
editThread.start()

playThread = threading.Thread(target=play)
playThread.start()

root.mainloop()