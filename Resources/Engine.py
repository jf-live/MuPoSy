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

notes = algo.Notes(key='D')
vari.notesList = notes.getListNotes()

### Synths section:

# available synth depending on how many are requested in the constants at init

# heavy compression is applied to prevent annoying peaks sometimes created by 
# some settings

# HP filtering from Interactivity is applied before outputing

def gen1():
    gen01 = algo.AlgoGen(notes = "loop",
                         tempo = vari.mainTempoInit* 0.125, 
                         side = "mid",
                         mul = 0.6)
    genFX01 = effe.FxMixer(gen01)
    
    return genFX01

def gen2():
    gen02 = algo.AlgoGen(notes = "low", 
                         tempo = vari.mainTempoInit* random.choice([2,4]), 
                         side = "mid",
                         mul = 0.8)
    genFX02 = effe.FxMixer(gen02)
    return genFX02

def gen3():
    gen03 = algo.AlgoGen(tempo = vari.mainTempoInit* random.choice([.2,.4]))
    genFX03 = effe.FxMixer(gen03)
    genOut03 = Compress(genFX03,-40,ratio = 20)
    return genOut03

def gen4():
    gen04 = algo.AlgoGen(notes = "loop",
                        tempo = vari.mainTempoInit* random.choice([0.125,0.25]), 
                        side = "right", 
                        mul = 0.6)
    genFX04 = effe.FxMixer(gen04)
    genOut04 = Compress(genFX04,-40,ratio = 20)
    return genOut04

if cons.NUMGENS == 1:
    outA = gen1()
    genOut01 = Compress(outA,-40,ratio = 20)
    gensOutput = ButHP(genOut01,vari.outFiltFreqSig).out()
elif cons.NUMGENS == 2:
    outA = gen1()
    outB = gen2()
    genOut01 = Compress(outA,-40,ratio = 20)
    genOut02 = Compress(outB,-40,ratio = 20)
    gensTot = genOut01 + genOut02
    gensOutput = ButHP(gensTot,vari.outFiltFreqSig).out()





def chFXs(num = cons.NUMGENS):
    print "changing FXs"
    if num == 1:
        outA.changeFXs()
    elif num == 2:
        outA.changeFXs()
        outB.changeFXs()
    elif num == 3:
        genFX1.changeFXs()
        genFX2.changeFXs()
        genFX3.changeFXs()
    elif num == 4:
        genFX1.changeFXs()
        genFX2.changeFXs()
        genFX3.changeFXs()
        genFX4.changeFXs()

patChFXs = Pattern(chFXs,vari.fxChangeTime).play()



# filtering from Interactivity and output
# gensTot = genOut1 + genOut3
# gensOutput = ButHP(gensTot,vari.outFiltFreqSig).out()


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

noteUpdate = Pattern(chNotes, 10).play()





