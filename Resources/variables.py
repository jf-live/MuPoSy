# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.

from pyo import *
import random

### Tempo
mainTempoInit = random.uniform(0.2,2) # mainTempoInit keeps the slowest possible time for a note
mainTempo = mainTempoInit #mainTempo is the current tempo, affected by MIDI CC in Engine.py
sineTempo = 1 #sineTempo is also affected by MIDI CC; is used by sines with Voice
fxChangeTime = 15 # time for pattern to change the FXs

### MIDI CC
currentCCVoix = 0  # pour transmettre les valeurs CC pour Voix
currentCCSnd = 0  # pour transmettre les valeurs CC pour Sons

outFiltFreqSig = SigTo(0,0.05) # used to change the master filter, set by CC

sineGenMul = 0 # to change the volume of the SineGen, set by CC
sineRevMul = 0.8 # to change the amount of reverb feedback of SineGen, set by CC

synthGenMul = SigTo(1, 0.05) # to change the volume of the SynthGens, set by CC


### NOT IN USE - START
reuse = True # determines if a sequence keeps going, or new parameters should be applied
### NOT IN USE - END


### For notes
rootColl = [] # mise en mémoire des clés sélectionnées
scaleColl = [] # mise en mémoire des gammes sélectionnées
octColl = [] # mise en mémoire des octaves sélectionnées
# Will set the number of chosen keys for a section
# Can be changed later by calling collLenDef in variables
scaleInUse = []   # Current scale being played
collLen = 12

class LenDef:
    def notesCollLen(self, minL=4,maxL=20):
        global collLen
        collLen = random.randint(minL,maxL)

# To set at init of piece
LenDef().notesCollLen(4,20)


### For samples
sampColl = [] # storing the played samples



### To store the path to the Tts poem
poemPath = None

### For darwinian evolution of gens

genStore = {"osc": [],
            "value": [],
            "LFOFreq":[],
            "LFOType":[],
            "MultFreq":[],
            "MultType":[], 
            }




