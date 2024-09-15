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
import cv2
from PIL import Image, ImageTk 
import groqstuff

# Create the main window
root = tk.Tk()
root.title("AutOST")

sv_ttk.set_theme("dark")

sliders = ["Syncopation", "Speed", "Dissonance", "Creativity", "Majorness", "Intensity"]

def onSyncopationChange(value):
    rhythm.syncopation = float(value) / 100

def onSpeedChange(value):
    rhythm.speed = float(value) / 100

def onDissonanceChange(value):
    chords.dissonance = float(value) / 100

def onCreativityChange(value):
    chords.creativity = float(value) / 100

def onMajornessChange(value):
    chords.majorness = float(value) / 100

def onIntensityChange(value):
    drums.intensity = float(value) / 100

functions = [
    onSyncopationChange,
    onSpeedChange,
    onDissonanceChange,
    onCreativityChange,
    onMajornessChange,
    onIntensityChange
]

for i in functions:
    i(0)

# Create a frame to hold the sliders
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

sliderScales = []
#add the sliders
lastI = 0
for(i, slider) in enumerate(sliders):
    function = functions[i]
    ttk.Label(root, text=slider).grid(row=i, column=0, padx=10, pady=10)
    slider = ttk.Scale(root, from_=0, to=100, orient='horizontal')
    slider.bind("<ButtonRelease-1>", lambda _, function_=function, slider_=slider: function_(slider_.get()))
    slider.grid(row=i, column=1, padx=10, pady=10)
    sliderScales.append(slider)
    lastI = i + 1

editThread = None
playThread = None
# groqThread = None
def start():
    global editThread, playThread, groqThread
    #random.seed(0)
    editThread = threading.Thread(target=editMusic)
    editThread.start()

    playThread = threading.Thread(target=play)
    playThread.start()

    # groqThread = threading.Thread(target=updateVideo)
    # groqThread.start()

done = False
def onClosing():
    global editThread, playThread, groqThread, done, piece
    done = True
    root.destroy()
    editThread.join()
    stopPlaying(piece)
    playThread.join()
    # groqThread.join()

def clamp(val, min, max):
    if val < min:
        return min
    if val > max:
        return max
    return val

def moveTheSliders(dict):
    global sliderScales
    rhythm.syncopation = clamp(dict['Fear'] / 100 - dict['Calmness'] / 200, 0, 1)
    rhythm.speed = clamp(dict['Happiness'] / 300 + dict['Fear'] / 300 + dict['Anger'] / 300 - dict['Calmness'] / 200, 0, 1)
    chords.dissonance = clamp(dict['Fear'] / 250 + dict['Anger'] / 250, 0, 1)
    chords.creativity = clamp(dict['Calmness'] / 200, 0, 1)
    if dict['Happiness'] > 50:
        chords.majorness = 1
    else:
        chords.majorness = 0
    drums.intensity = clamp(dict['Happiness'] / 300 + dict['Fear'] / 300 + dict['Anger'] / 100 - dict['Calmness'] / 400, 0, 1)
    sliderScales[0].set(int(rhythm.syncopation * 100))
    sliderScales[1].set(int(rhythm.speed * 100))
    sliderScales[2].set(int(chords.dissonance * 100))
    sliderScales[3].set(int(chords.creativity * 100))
    sliderScales[4].set(int(chords.majorness * 100))
    sliderScales[5].set(int(drums.intensity * 100))


frame = None
def groqIt():
    global frame
    img_name = "pic.png"
    cv2.imwrite(img_name, frame)
    dict = None
    while not dict:
        desc = groqstuff.list_emotions(img_name)
        dict = groqstuff.json_to_dict(desc)
    dict['Fear'] = ((dict['Fear'] / 100) ** 0.5) * 100
    dict['Anger'] = ((dict['Anger'] / 100) ** 0.5) * 100
    dict['Happiness'] = ((dict['Happiness'] / 100) ** 2) * 100
    dict['Calmness'] = ((dict['Calmness'] / 100) ** 2) * 100
    print(dict)
    moveTheSliders(dict)
    determineEmoji(dict)

logoFrame = ttk.Frame(root, width="400", height="160")
logoFrame.pack_propagate(False)
logo = ttk.Label(logoFrame)

playButton = ttk.Button(root, text="Play", command=start)
playButton.grid(row=lastI, column=0, padx=10, pady=10)

quitButton = ttk.Button(root, text="Quit", command=onClosing)
quitButton.grid(row=lastI, column=1, padx=10, pady=10)

groqEmojiFrame = ttk.Frame(root)
groqButton = ttk.Button(groqEmojiFrame, text="Determine Emotion with Groq", command=groqIt)
groqButton.grid(row=0, column=0, padx=10, pady=0)
emojiLabel = ttk.Label(groqEmojiFrame, text=":)", font=('TkDefaultFont', 16))
emojiLabel.grid(row=0, column=1, padx=10, pady=0)
groqEmojiFrame.grid(row=lastI, column=2, padx=10, pady=10)

def determineEmoji(dict):
    global emojiLabel
    emojis = [[":|", "˙◠˙"], ["(´◡`)", "(◕‿◕)"], ["⋋_⋌", "༽◺_◿༼"], ["( ⚆ _ ⚆ )", "ヽ(O_O )ﾉ"]]
    emoji = None

    del dict['Calmness']

    mostIntenseKey = None
    mostIntenseVal = 0
    for key, val in dict.items():
        if val > mostIntenseVal:
            mostIntenseKey, mostIntenseVal = key, val
    
    if mostIntenseVal < 30:
        if mostIntenseKey == 'Happiness':
            emoji = emojis[0][0]
        else:
            emoji = emojis[0][1]
    elif mostIntenseVal < 66:
        if mostIntenseKey == 'Happiness':
            emoji = emojis[1][0]
        elif mostIntenseKey == 'Anger':
            emoji = emojis[2][0]
        else:
            emoji = emojis[3][0]
    else:
        if mostIntenseKey == 'Happiness':
            emoji = emojis[1][1]
        elif mostIntenseKey == 'Anger':
            emoji = emojis[2][1]
        else:
            emoji = emojis[3][1]

    emojiLabel.config(text=emoji)

labelFrame = ttk.Frame(root, width="400", height="300")
labelFrame.pack_propagate(False)
camLabel = ttk.Label(labelFrame, text="yes") 
camLabel.pack(fill=tk.BOTH, expand=True)
labelFrame.grid(row=0, column=2, rowspan=lastI, padx=10, pady=10)

vid = cv2.VideoCapture(0) 
width, height = 400, 300
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

def update_frame():
    global frame
    _, frame = vid.read()
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    captured_image = Image.fromarray(opencv_image)
    bgImage = ImageTk.PhotoImage(image=captured_image)
    camLabel.photo_image = bgImage
    camLabel.configure(image=bgImage)
    camLabel.after(50, update_frame)  # Schedule the next update after 50 milliseconds

update_frame()

music.melodyInstrument = music.rollMelodyInstrument(drums.intensity)
music.harmonyInstrument = music.rollHarmonyInstrument(drums.intensity)
music.drumInstrument = 8
timeline1 = Timeline(music.melodyInstrument, [])
timeline2 = Timeline(music.harmonyInstrument, [])
timeline3 = Timeline(music.drumInstrument, [])

piece = Piece([(120, 0)], [timeline1, timeline2, timeline3])

def editMusic():
    global timeline1, timeline2, timeline3, piece, done

    #general vars
    currentBeat = 0
    currentBar = 0
    current4Bar = 0

    oldSyncopation = rhythm.syncopation
    oldSpeed = rhythm.speed
    oldDissonance = chords.dissonance
    oldCreativity = chords.creativity
    oldMajorness = chords.majorness
    oldIntensity = drums.intensity

    #melody rhythm vars
    melodyBuffer = 0.75 #seconds
    nextRhythmBarToGenerate = 0
    oldRhythmI = 0

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
    currentDrumPattern = drums.chooseDrumLoop()

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

        if oldDissonance != chords.dissonance or oldCreativity != chords.creativity or oldMajorness != chords.majorness:
            newprog = chords.generateProgression()
            progressions.append(newprog)
            chords.key = random.choices(["Major","Minor"],[chords.majorness,1-chords.majorness])[0]
        
        if oldIntensity != drums.intensity:
            currentDrumPattern = drums.chooseDrumLoop()
            music.stopCurrentNotes(timeline1,0)
            music.stopCurrentNotes(timeline2,1)
            melodyInstrument = music.rollMelodyInstrument(drums.intensity)
            timeline1.channel = melodyInstrument
            harmonyInstrument = music.rollHarmonyInstrument(drums.intensity)
            timeline2.channel = harmonyInstrument
        
        if oldSyncopation != rhythm.syncopation or oldSpeed != rhythm.speed:
            rhythm.resetRhythmScheme()

        oldSyncopation = rhythm.syncopation
        oldSpeed = rhythm.speed
        oldDissonance = chords.dissonance
        oldCreativity = chords.creativity
        oldMajorness = chords.majorness
        oldIntensity = drums.intensity

        oldRhythmI = rhythm.rhythmI

        #add melody rhythm
        if timeInto + melodyBuffer >= noteTimeToTime(nextRhythmBarToGenerate * 4, piece.bpms):
            nextRhythm = generateMelodyRhythm()
            for j in range(len(nextRhythm)):
                noteLen = (nextRhythm[j + 1] if j < len(nextRhythm) - 1 else 4) - nextRhythm[j]
                note = Note(60, nextRhythm[j] + currentBar * 4, 70, noteLen)
                timeline1.notes.append(note)
            chordNotes = getNotesFromChord(progressions[-1][nextChordBarToGenerate % 4])
            nextRhythmBarToGenerate += 1
        
        #add chords   
        if timeInto + chordBuffer >= noteTimeToTime(nextChordBarToGenerate * 4, piece.bpms):
            chordNotes = getNotesFromChord(progressions[-1][nextChordBarToGenerate % 4])
            noteTime = nextChordBarToGenerate * 4
            note = Note(rootNote + chordNotes[0], noteTime, 70, 4)
            timeline2.notes.append(note)
            note = Note(rootNote + chordNotes[1], noteTime, 70, 4)
            timeline2.notes.append(note)
            note = Note(rootNote + chordNotes[2], noteTime, 70, 4)
            timeline2.notes.append(note)
            nextChordBarToGenerate += 1

        #add melody
        if nextNoteToGenerateIndex <= len(timeline1.notes) - 1:
            thisNoteO = timeline1.notes[nextNoteToGenerateIndex]
            if (len(timeline1.notes) > 0 and timeInto + melodyBuffer >= noteTimeToTime(thisNoteO.time, piece.bpms)):
                lastNoteO = None
                try:
                    lastNoteO = timeline1.notes[nextNoteToGenerateIndex - 1]
                except:
                    pass

                lastNote = lastNoteO.note - 12 - rootNote if lastNoteO else 99
                chordNotes = chords.getNotesFromChord(progressions[-1][int(thisNoteO.time % 4)])
                if thisNoteO.time % 4 < 3:
                    nextChordNotes = chords.getNotesFromChord(progressions[-1][int(thisNoteO.time % 4)+1])
                else: 
                    nextChordNotes = chords.getNotesFromChord(progressions[-1][0])
                thisNote = generateNextNote(lastNote, thisNoteO.time, chordNotes, chords.key, nextChordNotes, rhythm.speed)
                if thisNoteO.time % 4 == 0:
                    thisNoteO.velocity += 8
                if thisNoteO.time % 2 == 0:
                    thisNoteO.velocity += 5
                thisNoteO.note = thisNote + 12 + rootNote
                nextNoteToGenerateIndex += 1

        #add drums
        if timeInto + drumBuffer >= noteTimeToTime(nextDrumBarToGenerate * 4, piece.bpms):
            
            drums.pasteDrumLoop(currentDrumPattern, timeline3, nextDrumBarToGenerate*4, drums.intensity)
            nextDrumBarToGenerate += 1
        

def play():
    global timeline1, piece
    init()
    playPiece(piece)

root.protocol("WM_DELETE_WINDOW", onClosing)

root.mainloop()