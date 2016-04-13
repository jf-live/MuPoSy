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

gen1 = algo.AlgoGen(notes = "low", 
                    tempo = vari.mainTempo* random.choice([2,4]), 
                    side = "mid",
                    mul = 0.05)
# gen2 = algo.AlgoGen(tempo = vari.mainTempo* random.choice([.2,.4]))
gen3 = algo.AlgoGen(notes = "loop",
                    tempo = vari.mainTempo* 0.125, 
                    side = "left",
                    mul = 0.05)
gen4 = algo.AlgoGen(notes = "loop",
                    tempo = vari.mainTempo* random.choice([0.125,0.25]), 
                    side = "right", 
                    mul = 0.05)


# b = effe.Distor(gen1,mul=1)
# c = effe.Harmon(b,mul=1)
# d = effe.Filter(c, mul=1)
# e = effe.Chorused(d)
# f = effe.Panning(gen1)
# g = effe.Delayer(g)
# h = effe.Phasered(g)
# i = Compress(h,-20,ratio = 20)
# i = Compress(f,-20,ratio = 20)
# i.out()
i = Compress(gen1,-20,ratio = 20)
i.out()
# i2 = Compress(gen2,-20,ratio = 20)
# i2.out()
i3 = Compress(gen3,-20,ratio = 20)
i3.out()
i4 = Compress(gen4,-20,ratio = 20)
i4.out()



# to play the sines "twinkles" while the voice is talking
sine = synt.SineGen()
sine.out()


### to play sound objects

samp1 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]
samp2 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]

# to change the notes for the pads
def chNotes():
    notes.newNotes()
    print 'NOTES'

noteUpdate = Pattern(chNotes, 10).play()





