# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
# 
# This is where the calling is done



import utilities as util
import constants as cons
import variables as vari
import Interactivity as inte
import Voix as voix
import SynthGen as synt
import SamplePlay as samp
import Effects as effe
import Algo as algo

import random
from pyo import *


####  !!!   Poem audio is completely done in Voix.py   !!!   ####

notes = algo.Notes(key='D')
vari.notesList = notes.getListNotes()

# to play synths

gen1 = algo.AlgoGen(notes = "low", tempo = vari.mainTempo)
gen2 = algo.AlgoGen(tempo = vari.mainTempo* random.choice([2,0.5,0.25,4]))
gen3 = algo.AlgoGen(tempo = vari.mainTempo* random.choice([0.05,0.1]), mul = 0.4)


# b = effe.Distor(gen1,mul=1)
# c = effe.Harmon(b,mul=1)
# d = effe.Filter(c, mul=1)
# e = effe.Chorused(d)
f = effe.Panning(gen1)
# g = effe.Delayer(f)
# h = effe.Phasered(g)
# i = Compress(h,-20,ratio = 20)
i = Compress(f,-20,ratio = 20)
i.out()
i2 = Compress(gen2,-20,ratio = 20)
i2.out()
i3 = Compress(gen3,-20,ratio = 20)
i3.out()



### to play sound objects

# to keep alive the samples being played
samp1 = None
samp2 = None
# to keep track of the samples playtime
timeSamp1 = 15
timeSamp2 = 15

def callSamp1():
    global patSamp1
    global samp1
    global timeSamp1
    samp1 = [algo.AlgoSamp(dur = timeSamp1) for i in range(cons.NUMSAMPS)]
    # change the time for the next calls here
    timeSamp1 = random.randint(5,30)
    patSamp1.time = timeSamp1

def callSamp2():
    global patSamp2
    global samp2
    global timeSamp2
    samp2 = [algo.AlgoSamp(dur = timeSamp2) for i in range(cons.NUMSAMPS)]
    # change the time for the next calls here
    timeSamp2 = random.randint(5,30)
    patSamp2.time = timeSamp2


# to play the sines "twinkles" while the voice is talking
sine = synt.SineGen()
sine.out()



# to change the notes for the pads
def chNotes():
    notes.newNotes()
    print 'NOTES'


### Actual calling is done here

# Change notes being played
# patNotes = Pattern(chNotes, timeSynth).play()  # TRYING OUT TIMESYNTH HERE<-----------

# Plays Samples
patSamp1 = Pattern(callSamp1, timeSamp1).play()
patSamp2 = Pattern(callSamp2, timeSamp2).play()



