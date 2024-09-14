import threading
import time
import tkinter as tk
from tkinter import ttk
import rhythm
import music
from music import Note, Timeline, Piece, noteTimeToTime, playPiece, init, stopPlaying

def onSyncopationChange(value):
    rhythm.syncopation = float(value) / 100

def onSpeedChange(value):
    rhythm.speed = float(value) / 100

def onSporadicnessChange(value):
    rhythm.sporadicness = float(value) / 100

# Create the main window
root = tk.Tk()
root.title("Tkinter Sliders Example")

# Create a frame to hold the sliders
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Create and place sliders with labels
ttk.Label(frame, text="Syncopation").grid(row=0, column=0, padx=5, pady=5)
slider1 = ttk.Scale(frame, from_=0, to=100, orient='horizontal', command=onSyncopationChange)
slider1.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame, text="Speed").grid(row=1, column=0, padx=5, pady=5)
slider2 = ttk.Scale(frame, from_=0, to=100, orient='horizontal', command=onSpeedChange)
slider2.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame, text="Sporadicness").grid(row=2, column=0, padx=5, pady=5)
slider3 = ttk.Scale(frame, from_=0, to=100, orient='horizontal', command=onSporadicnessChange)
slider3.grid(row=2, column=1, padx=5, pady=5)

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