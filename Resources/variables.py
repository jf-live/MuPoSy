# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.


import random

mainTempo = 1  # en seconde

currentCC0Val = 0  # pour transmettre les valeurs CC

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






fx = {  "filter": {
                    "freq": random.random(), 
                    "q": random.random()
        },
        "disto": {
                    "lfoFreq": random.uniform(0.1,10),
                    "amount": random.random()

        },
                "wow": 2, 
                "patate": 3, 
                "gens": 
                    {"gen1": '1a' , "gen2": '2a'}
     }


# to determine if synthGens are played with closed envelopes, or continuously
randEnvSynth = 10#random.randint(0,100)





