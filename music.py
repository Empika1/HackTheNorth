import mido
import time
import pygame.midi

mido.set_backend("mido.backends.portmidi")

names = mido.get_output_names()
print(names)

out = mido.open_output(names[2])
out.send(mido.Message('note_on', note=60, velocity=64, time=1))
time.sleep(1)
out.send(mido.Message('note_on', note=60, velocity=64, time=1))