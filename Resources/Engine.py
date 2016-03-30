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


# to play synths
gen1 = None
gen2 = None
timeSynth = 20

def callGen1():
    global patGens1
    global timeSynth
    global gen1

    # change the time for the next calls here
    timeSynthNew = random.randint(20,50)
    gen1 = [algo.AlgoGen(noteDur=vari.mainTempo, dur=timeSynthNew) for i in range(cons.NUMGENS)]
    genCall = [gen1[i].doinIt() for i in range(cons.NUMGENS)]
    patGens1.time = timeSynthNew
    timeSynth = timeSynthNew

def callGen2():
    global patGens2
    global timeSynth
    global gen2

    # change the time for the next calls here
    timeSynthNew = random.randint(20,50)
    gen2 = [algo.AlgoGen(noteDur=vari.mainTempo/2., dur=timeSynthNew) for i in range(cons.NUMGENS)]
    genCall = [gen2[i].doinIt() for i in range(cons.NUMGENS)]
    patGens2.time = timeSynthNew
    timeSynth = timeSynthNew


    


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
patNotes = Pattern(chNotes, timeSynth).play()  # TRYING OUT TIMESYNTH HERE<-----------
# Plays SynthGens
patGens1 = Pattern(callGen1, timeSynth).play()
patGens2 = Pattern(callGen2, timeSynth).play(delay = timeSynth/2.)
# Plays Samples
patSamp1 = Pattern(callSamp1, timeSamp1).play()
patSamp2 = Pattern(callSamp2, timeSamp2).play()



# To retrieve MIDI CC and affect the sound accordingly
midiMet = util.eventMetSnd
signalIn = inte.MidiCCInSnd()
tr = TrigFunc(midiMet, signalIn.retVal)

def distance():
    # must be a better way for the variables...
    filtFreq = vari.currentCCSnd
    sineMul = vari.currentCCSnd
    synthMul = vari.currentCCSnd
    tempo = vari.currentCCSnd
    mTempo = vari.currentCCSnd
    # adjusting hipass 
    if filtFreq < 40:
        vari.outFiltFreq = util.translate(filtFreq, 0,40, 0, 2000)
    elif filtFreq >= 40:
        if filtFreq > 100:
            filtFreq = 100
        vari.outFiltFreq = util.translate(filtFreq, 40,100, 2000, 8000)
    if sineMul < 10:
        sineMul = 10
    if sineMul > 85:
        sineMul = 85
    vari.sineGenMul = util.translate(sineMul, 10, 85, 0,1)
    if synthMul < 50:
        synthMul = 50
    if synthMul > 100:
        synthMul = 100
    vari.synthGenMul = util.translate(synthMul, 50, 100, 1,0.2)
    vari.sineTempo = util.translate(tempo, 0, 127, 0.7,0.3)
    if mTempo > 80:
        mTempo = 80
    vari.mainTempo = util.translate(mTempo, 0, 80, vari.mainTempoInit,8)


patMIDI = Pattern(distance,0.1).play(delay=2)

    


