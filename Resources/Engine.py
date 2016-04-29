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

# picks notes and scale at init
notes = algo.Notes()
vari.notesList = notes.getListNotes()

### Synths section:

# Available synth depending on how many are requested in the constants at init.
# Heavy compression is applied to prevent annoying peaks sometimes created by 
#   some settings.
# HP filtering from Interactivity is applied before outputing.

class Gens(Sig):
    def __init__(self, which = 1, mul = 1, add = 0):
        if which == 1:
            self.gen = algo.AlgoGen(notes = "loop",
                                    tempo = 0.125, 
                                    side = "mid",
                                    mul = 0.6)
        elif which == 2:
            self.gen = algo.AlgoGen(notes = "low", 
                                    tempo = random.choice([1,3]), 
                                    side = "mid",
                                    mul = 0.8)
        elif which == 3:
            self.gen = algo.AlgoGen(tempo = random.choice([.2,.4]))
        elif which == 4:
            self.gen = algo.AlgoGen(notes = "loop",
                                    tempo = random.choice([0.125,0.25]), 
                                    side = "right", 
                                    mul = 0.6)

        self.genFX = effe.FxMixer(self.gen)
        Sig.__init__(self,self.genFX,mul,add)

    def changeFXs(self):
        self.genFX.changeFXs()

    def newNotesMels(self):
        self.gen.newLoops()

if cons.NUMGENS > 0:

    if cons.NUMGENS == 1:
        outA = Gens(1)
        gensTot = Compress(outA,-30,ratio = 20)
    elif cons.NUMGENS == 2:
        outA = Gens(1)
        outB = Gens(2)
        genOut01 = Compress(outA,-30,ratio = 20)
        genOut02 = Compress(outB,-30,ratio = 20)
        gensTot = genOut01 + genOut02
    elif cons.NUMGENS == 3:
        outA = Gens(1)
        outB = Gens(2)
        outC = Gens(3)
        genOut01 = Compress(outA,-30,ratio = 20)
        genOut02 = Compress(outB,-30,ratio = 20)
        genOut03 = Compress(outC,-30,ratio = 20)
        gensTot = genOut01 + genOut02 + genOut03
    elif cons.NUMGENS == 4:
        outA = Gens(1)
        outB = Gens(2)
        outC = Gens(3)
        outC = Gens(4)
        genOut01 = Compress(outA,-30,ratio = 20)
        genOut02 = Compress(outB,-30,ratio = 20)
        genOut03 = Compress(outC,-30,ratio = 20)
        genOut04 = Compress(outD,-30,ratio = 20)
        gensTot = genOut01 + genOut02 + genOut03 + genOut04



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



    # to change the melodies being played in Demo mode
    def chLoopsDemo(num = cons.NUMGENS):
        print "changing Loops Demo"
        # first change available notes
        notes.newNotes()
        vari.notesList = notes.getListNotes()
        # then generate new melodies
        if num == 1:
            outA.newNotesMels()
        elif num == 2:
            outA.newNotesMels()
            outB.newNotesMels()
        elif num == 3:
            outA.newNotesMels()
            outB.newNotesMels()
            outC.newNotesMels()
        elif num == 4:
            outA.newNotesMels()
            outB.newNotesMels()
            outC.newNotesMels()
            outD.newNotesMels()
        vari.mainTempoInit = random.uniform(0.2,0.5)

    # to change notes and melody in manual mode

    def chLoopsManual(num = cons.NUMGENS):
        if vari.currentCCSnd > 110 and vari.isVoicePlaying2 == 0:
            print "changing Loops Manual"

            # first change available notes
            notes.newNotes()
            vari.notesList = notes.getListNotes()
            # then generate new melodies
            if num == 1:
                outA.newNotesMels()
            elif num == 2:
                outA.newNotesMels()
                outB.newNotesMels()
            elif num == 3:
                outA.newNotesMels()
                outB.newNotesMels()
                outC.newNotesMels()
            elif num == 4:
                outA.newNotesMels()
                outB.newNotesMels()
                outC.newNotesMels()
                outD.newNotesMels()
            # then change global tempo
            vari.mainTempoInit = random.uniform(0.2,0.5)
            vari.isVoicePlaying2 = 1
            
        elif vari.currentCCSnd <= 110 and vari.isVoicePlaying2 == 1:
            vari.isVoicePlaying2 = 0

    # applies the patterns depending on the playmode
    if cons.PLAYMODE == "Demo":
        mainSynthEnv = Fader(cons.DEMOSLOPE,cons.DEMOSLOPE,cons.DEMOTIME)
        def playMainSynthEnv():
            mainSynthEnv.play()
        patMainSynthEnv = Pattern(playMainSynthEnv,cons.DEMOTIME).play()
        patChLoops = Pattern(chLoopsDemo, cons.DEMOTIME).play()

    elif cons.PLAYMODE == "Manual":
        mainSynthEnv = 1.
        patChLoops = Pattern(chLoopsManual, 1).play()



    # outputs the synths
    gensOutput = ButHP(gensTot,vari.outFiltFreqSig, mul = mainSynthEnv).out()



### to play the sines "twinkles" while the voice is talking
sine = synt.SineGen()
sine.out()



### to play sound objects

samp = [[algo.AlgoSamp() for i in range(cons.NUMSAMPS)] for i in range(cons.NUMSAMPS)]




