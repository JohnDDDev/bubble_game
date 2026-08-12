from playsound3 import playsound
import threading
from time import sleep

def sound_handler(sound,length,delay):
    first_bubble = True
    for i in range(length):
        if not first_bubble:
            playsound(sound, block=False)
            continue
        sleep(delay)
        playsound(sound, block=False)

def Play(sound,length):
    play = threading.Thread(target=sound_handler,args=(sound,length,0.2)).start()