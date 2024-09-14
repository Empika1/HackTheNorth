import threading
import time
import tkinter as tk
from tkinter import ttk
import rhythm
import music
from music import Note, Timeline, Piece, noteTimeToTime, playPiece, init, stopPlaying
import chords
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

# Create a frame to hold the sliders
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

#add the sliders
for(i, slider) in enumerate(sliders):
    function = functions[i]
    ttk.Label(root, text=slider).grid(row=i, column=0, padx=5, pady=5)
    slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=function)
    slider.grid(row=i, column=1, padx=5, pady=5)

timeline1 = Timeline(0)
piece = Piece([(120, 0)], [timeline1])
def editMusic():
    global timeline1, piece, done
    buffer = 0.5 #seconds

    barTime = 0
    while not done:
        if len(timeline1.notes) <= 1 or time.time() - music.startTime + buffer > noteTimeToTime(timeline1.notes[-1].time, piece.bpms):
            nextRhythm = rhythm.generateMelodyRhythm()
            barTime += 4
            for j in range(len(nextRhythm)):
                noteLen = (nextRhythm[j + 1] if j < len(nextRhythm) - 1 else 4) - nextRhythm[j]
                note = Note(60, nextRhythm[j] + barTime, 70, noteLen)
                timeline1.notes.append(note)

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