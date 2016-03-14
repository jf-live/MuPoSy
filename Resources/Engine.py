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

met = util.genMet.setTime(2)

# patTime = 2

notes = algo.Notes(key='D')



def callGen():
	global patGens1
	global patGens2
	gen = [algo.AlgoGen(noteDur=vari.mainTempo) for i in range(cons.NUMGENS)]
	genCall = [gen[i].doinIt() for i in range(cons.NUMGENS)]
	# a2 = [algo.AlgoGen(noteDur=vari.mainTempo/2) for i in range(cons.NUMGENS)]
	# a3 = [a2[i].doinIt() for i in range(cons.NUMGENS)]

	# change the time for the next calls here
	patGens1.time = random.randint(20,50)
	# patGens2.time = random.randint(20,50)



def callSamp():
	global patSamp1
	global patSamp2
	samp = [algo.AlgoSamp() for i in range(cons.NUMSAMPS)]
	# sampCall = [samp[i].doinIt() for i in range(cons.NUMSAMPS)]
	# a2 = [algo.AlgoGen(noteDur=vari.mainTempo/2) for i in range(cons.NUMGENS)]
	# a3 = [a2[i].doinIt() for i in range(cons.NUMGENS)]

	# change the time for the next calls here
	patSamp1.time = random.randint(10,20)
	patSamp2.time = random.randint(10,20)


def chNotes():
	notes.newNotes()
	print 'NOTES'



# Actual calling is done here
patNotes = Pattern(chNotes, 10).play()
patGens1 = Pattern(callGen, 20).play()
# patGens2 = Pattern(callGen, 20).play()
# patSamp1 = Pattern(callSamp, 10).play()
# patSamp2 = Pattern(callSamp, 10).play()










