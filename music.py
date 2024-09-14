import mido
import pygame
import pygame.midi

mido.set_backend("mido.backends.portmidi")

names = mido.get_output_names()
print(names) 


out = mido.open_output(names[2])
out.send(mido.Message('note_on', note=60, velocity=64))

#msg.copy(channel=1)
#mido.Message('note_on', channel=1, note=60, velocity=64, time=0)
#time.sleep(50)