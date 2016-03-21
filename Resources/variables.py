# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.

from pyo import *
import random

mainTempo = 1  # en seconde
sineTempo = 1  #

currentCCVoix = 0  # pour transmettre les valeurs CC pour Voix
currentCCSnd = 0  # pour transmettre les valeurs CC pour Sons


outFiltFreq = 0 # used to change the master filter, set by CC
outFiltFreqSig = SigTo(outFiltFreq,0.05)

sineGenMul = 0 # to change the volume of the SineGen, set by CC

synthGenMul = 1 # to change the volume of the SynthGens, set by CC


reuse = True # determines if a sequence keeps going, or new parameters should be applied

# For notes
rootColl = [] # mise en mémoire des clés sélectionnées
scaleColl = [] # mise en mémoire des gammes sélectionnées
octColl = [] # mise en mémoire des octaves sélectionnées
# Will set the number of chosen keys for a section
# Can be changed later by calling vari.collLenDef
collLen = 0

scaleInUse = []   # Current scale being played


# For samples
sampColl = [] # mise en mémoire des samples utilisés
# Max number of samples to be used at one time
sampCollLen = 0

class LenDef:

    def notesCollLen(self, minL=1,maxL=5):
        global collLen
        collLen = random.randint(minL,maxL)

    def sampCollLen(self, minL=1,maxL=5):
        global sampCollLen
        sampCollLen = random.randint(minL,maxL)


# To set at init of piece
LenDef().notesCollLen(1,5)
LenDef().sampCollLen(1,10)

# To store the path to the Tts poem
poemPath = None

# For darwinian evolution of gens

genStore = {"osc": [],
            "value": [],
            "LFOFreq":[],
            "LFOType":[],
            "MultFreq":[],
            "MultType":[], 
            }

genStMain = []


# Initiates the reverb space for samples
fxRvbInit = random.choice([.02,.1,.3,.5,.8])


fx = {  "filter": {

        },
        "disto": {

        },

     }


# to determine if synthGens are played with closed envelopes, or continuously


print "randEnvSynth"
randEnvSynth = random.randint(0,100)
print randEnvSynth




