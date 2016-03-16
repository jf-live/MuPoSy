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


# to play synth "pads"
gen = None

def callGen():
	global patGens1
	global patGens2
	global gen
	gen = [algo.AlgoGen(noteDur=vari.mainTempo) for i in range(cons.NUMGENS)]
	genCall = [gen[i].doinIt() for i in range(cons.NUMGENS)]
	# a2 = [algo.AlgoGen(noteDur=vari.mainTempo/2) for i in range(cons.NUMGENS)]
	# a3 = [a2[i].doinIt() for i in range(cons.NUMGENS)]
	# change the time for the next calls here
	patGens1.time = random.randint(20,50)
	# patGens2.time = random.randint(20,50)


# to play sound objects
samp=None

def callSamp():
	global patSamp1
	global patSamp2
	global samp
	samp = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]
	# sampCall = [samp[i].doinIt() for i in range(cons.NUMSAMPS)]
	# a2 = [algo.AlgoGen(noteDur=vari.mainTempo/2) for i in range(cons.NUMGENS)]
	# a3 = [a2[i].doinIt() for i in range(cons.NUMGENS)]

	# change the time for the next calls here
	patSamp1.time = random.randint(5,15)
	# patSamp2.time = random.randint(10,20)


# to play the sines while the voice is talking
sine = synt.SineGen()



# to change the notes for the pads
def chNotes():
	notes.newNotes()
	print 'NOTES'



# Actual calling is done here
patNotes = Pattern(chNotes, 10).play()
patGens1 = Pattern(callGen, 20).play()
# patGens2 = Pattern(callGen, 20).play()
patSamp1 = Pattern(callSamp, 10).play()
# patSamp2 = Pattern(callSamp, 10).play()




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
	vari.mainTempo = util.translate(mTempo, 0, 80, 1,4)


pat0 = Pattern(distance,0.1).play(delay=2)

    





