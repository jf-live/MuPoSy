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

### Synths section:

# generates the synth sounds
gen1 = algo.AlgoGen(notes = "low", 
                    tempo = vari.mainTempoInit* random.choice([2,4]), 
                    side = "mid",
                    mul = 0.8)
# gen2 = algo.AlgoGen(tempo = vari.mainTempoInit* random.choice([.2,.4]))
gen3 = algo.AlgoGen(notes = "loop",
                    tempo = vari.mainTempoInit* 0.125, 
                    side = "mid",
                    mul = 0.6)
# gen4 = algo.AlgoGen(notes = "loop",
#                     tempo = vari.mainTempoInit* random.choice([0.125,0.25]), 
#                     side = "right", 
#                     mul = 0.6)

# applies effects
genFX1 = effe.FxMixer(gen1)
# genFX2 = effe.FxMixer(gen2)
genFX3 = effe.FxMixer(gen3)
# genFX4 = effe.FxMixer(gen4)

def chFXs():
    print "changing FXs"
    genFX1.changeFXs()
    # genFX2.changeFXs()
    genFX3.changeFXs()
    # genFX4.changeFXs()

patChFXs = Pattern(chFXs,vari.fxChangeTime).play()


# compression and output
# heavy compression is applied to prevent annoying peaks sometimes created by 
# some settings
genOut1 = Compress(genFX1,-40,ratio = 20)
# genOut2 = Compress(genFX2,-40,ratio = 20, mul=4.5)
genOut3 = Compress(genFX3,-40,ratio = 20)
# genOut4 = Compress(genFX4,-40,ratio = 20)

# filtering from Interactivity and output
gensTot = genOut1 + genOut3
gensOutput = ButHP(gensTot,vari.outFiltFreqSig).out()


# to play the sines "twinkles" while the voice is talking
sine = synt.SineGen()
sine.out()


### to play sound objects

samp1 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]
# samp2 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]

# to change the notes for the pads
def chNotes():
    notes.newNotes()
    print 'NOTES'

noteUpdate = Pattern(chNotes, 10).play()





