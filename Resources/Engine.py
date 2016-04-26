# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
# 
# This is where the calling is done
# Depending on the performance of the computer, more or less generators can be 
#   activated.



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

notes = algo.Notes()
vari.notesList = notes.getListNotes()

### Synths section:

# Available synth depending on how many are requested in the constants at init.
# Heavy compression is applied to prevent annoying peaks sometimes created by 
#   some settings.
# HP filtering from Interactivity is applied before outputing.

def gen1():
    gen01 = algo.AlgoGen(notes = "loop",
                         tempo = 0.125, 
                         side = "mid",
                         mul = 0.6)
    genFX01 = effe.FxMixer(gen01)
    return genFX01

def gen2():
    gen02 = algo.AlgoGen(notes = "low", 
                         tempo = random.choice([2,4]), 
                         side = "mid",
                         mul = 0.8)
    genFX02 = effe.FxMixer(gen02)
    return genFX02

def gen3():
    gen03 = algo.AlgoGen(tempo = random.choice([.2,.4]))
    genFX03 = effe.FxMixer(gen03)
    return genFX03

def gen4():
    gen04 = algo.AlgoGen(notes = "loop",
                        tempo = random.choice([0.125,0.25]), 
                        side = "right", 
                        mul = 0.6)
    genFX04 = effe.FxMixer(gen04)
    genOut04 = Compress(genFX04,-40,ratio = 20)
    return genOut04

if cons.NUMGENS == 1:
    outA = gen1()
    gensTot = Compress(outA,-40,ratio = 20)
elif cons.NUMGENS == 2:
    outA = gen1()
    outB = gen2()
    genOut01 = Compress(outA,-40,ratio = 20)
    genOut02 = Compress(outB,-40,ratio = 20)
    gensTot = genOut01 + genOut02
elif cons.NUMGENS == 3:
    outA = gen1()
    outB = gen2()
    outC = gen3()
    genOut01 = Compress(outA,-40,ratio = 20)
    genOut02 = Compress(outB,-40,ratio = 20)
    genOut03 = Compress(outC,-40,ratio = 20)
    gensTot = genOut01 + genOut02 + genOut03
elif cons.NUMGENS == 4:
    outA = gen1()
    outB = gen2()
    outC = gen3()
    outC = gen4()
    genOut01 = Compress(outA,-40,ratio = 20)
    genOut02 = Compress(outB,-40,ratio = 20)
    genOut03 = Compress(outC,-40,ratio = 20)
    genOut04 = Compress(outD,-40,ratio = 20)
    gensTot = genOut01 + genOut02 + genOut03 + genOut04

if cons.PLAYMODE == "Demo":
    mainSynthEnv = Fader(4,4,cons.DEMOTIME)
    def playMainSynthEnv():
        mainSynthEnv.play()
    patMainSynthEnv = Pattern(playMainSynthEnv,cons.DEMOTIME).play()

elif cons.PLAYMODE == "Forever":
    mainSynthEnv = 1.

gensOutput = ButHP(gensTot,vari.outFiltFreqSig, mul = mainSynthEnv).out()


# to update the effects as the piece goes by, thus slowly changing the timbre of 
#   the sound gens
def chFXs(num = cons.NUMGENS):
    print "changing FXs"
    if num == 1:
        outA.changeFXs()
    elif num == 2:
        outA.changeFXs()
        outB.changeFXs()
    elif num == 3:
        outA.changeFXs()
        outB.changeFXs()
        outC.changeFXs()
    elif num == 4:
        outA.changeFXs()
        outB.changeFXs()
        outC.changeFXs()
        outD.changeFXs()

patChFXs = Pattern(chFXs,vari.fxChangeTime).play()



# to play the sines "twinkles" while the voice is talking
sine = synt.SineGen()
sine.out()


### to play sound objects
if cons.NUMSAMPS == 1:
    samp1 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]
elif cons.NUMSAMPS == 2:
    samp1 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]
    samp2 = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]


# to change the notes for the pads
def chNotes():
    notes.newNotes()
    print 'NOTES'


noteUpdate = Pattern(chNotes, 20).play()





