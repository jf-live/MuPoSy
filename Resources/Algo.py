#!/usr/bin/env python
# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
#
# Algorithmic engine


from pyo import *
import utilities as util
import constants as cons
import variables as vari
import Voix as voix
import SynthGen as synt
import SamplePlay as samp
import Effects as effe
import Interactivity as inte
import random, threading, time


# generates short melodies to be looped
class MelMaker:
    def __init__(self):
        self.mel = []  # to store the melodies

    def genMel(self,freqs,numMel):
        self.freqs = freqs
        self.numMel = numMel # how many melodies will be generated
        # 2 à 4 mélodies de 3 à 6 notes sont générées puis stockées dans une list
        coin = random.random()
        for i in range(self.numMel):
            if coin >= 0.5:
                self.mel.append([])
                for j in range(random.randint(3,4)):
                    if j == 0:
                        self.mel[i].append(random.choice(self.freqs[:-3]))
                    elif j == 1:
                        tempFreq = self.freqs.index(self.mel[i][0])
                        self.mel[i].append(random.choice(self.freqs[tempFreq:tempFreq+3]))
                    elif j == 2:
                        tempFreq = self.freqs.index(self.mel[i][1])
                        self.mel[i].append(random.choice(self.freqs[tempFreq:tempFreq+3]))
                    else:
                        self.mel[i].append(random.choice(self.freqs[5:]))
            elif coin < 0.5 and coin >= 0.25:
                self.mel.append([])
                for j in range(random.randint(3,4)):
                    if j ==0:
                        self.mel[i].append(random.choice(self.freqs))
                    elif j == 1 or j == 2:
                        coin2 = random.random()
                        if coin2 > 0.5:
                            self.mel[i].append(random.choice(self.freqs))
                        else:
                            self.mel[i].append(random.choice(self.freqs[-4:]))
                    else:
                        self.mel[i].append(self.mel[i][0]*2)
            else:
                self.mel.append([])
                for j in range(random.randint(3,4)):
                    if j == 0:
                        self.mel[i].append(self.freqs[0]*2)
                    elif j == 1 or j == 2:
                        coin2 = random.random()
                        if coin2 > 0.5:
                            self.mel[i].append(self.freqs[0]*2)
                        else:
                            self.mel[i].append(self.freqs[0]*4)
                    else:
                        self.mel[i].append(self.freqs[0]*8)
        return self

    def getMel(self):
        return self.mel


class AlgoGen(Sig):
    def __init__(self, notes="normal", tempo = 0.25, side= "mid", mul=1, add=0): 
        '''
        This module generates a stream of notes, with a specified root note.
        Duration of this stream is specified in seconds.
        '''

        self.notes = notes

        # to set tempo of this synth relative to mainTempo
        self.tempo = tempo

        # for periodic tempo variations
        self.tempoMod = 1

        # selection of weights for differents beats done in self.newLoops
        self.beat = Beat(self.tempo,8).play()

        # generates envelope
        self.env = CosTable([(0,.0),(3000,1.),(5191,1.),(8191,0.)])

        # to keep track of which step of the melody is being played
        self.melStep = 0

        # how many melodies will be generated
        self.numMel = random.randint(2,4)

        # to store the generated looped melody
        self.mel = []


        # generates a looped melody
        self.newLoops()

        randInitMel = random.randint(0,len(self.mel)-1)
        self.currentMel = self.mel[randInitMel]
        self.melRepCount = 0
        # change melody every 16 notes played (or about, depending on "notes" setting)
        self.patChangeMel = Pattern(self.changeMel,self.tempo*16.0).play()

        # if this instance is a "normal" note stream or a bass ("low") note stream
        if notes == "normal":
            self.whatFunc = self.changeNote
            self.inst = "normal"
        elif notes == "low":
            self.whatFunc = self.changeNoteLow
            self.inst = "low"
        elif notes == "loop":
            self.whatFunc = self.loopMel
            self.inst = "normal"
            self.patTempoMod = Pattern(self.tempoModifier,vari.mainTempo*self.tempo).play()

        self.tfunc = TrigFunc(self.beat, self.whatFunc)
        self.trigEnv = TrigEnv(self.beat, self.env, self.beat['dur'])

        # to change the tempo according to Interactivity
        self.patUpdateTempo = Pattern(self.keepTime,0.01).play()

        self.synthNum = random.randint(1,5)  # how many synthGen instances will compose a note
        # self.a = [synt.SynthGen(inst=self.inst,side=side,mul=self.trigEnv*vari.synthGenMul) for i in range(1)]#self.synthNum)]
        self.a = [synt.SynthGen(inst=self.inst,side=side,mul=self.trigEnv*vari.synthGenMul) for i in range(self.synthNum)]

        self.forOut = sum(self.a)
        Sig.__init__(self,self.forOut,[mul,mul],add)

    def changeNote(self):
        # plays random notes in key, used by "normal" only
        coin = random.random()
        if coin > 0.9:
            self.newNote = random.choice(vari.scaleInUse[-4:])
            [self.a[i].setNewFreq(self.newNote) for i in range(self.synthNum)]
        return self

    def changeNoteLow(self):
        # plays random bass notes in key, used by "low" only
        self.newNote = random.choice(vari.scaleInUse[0:3])
        if self.newNote >= 400:
            self.newNote /= random.choice([4,8,16])
        [self.a[i].setNewFreq(self.newNote) for i in range(self.synthNum)]
        return self

    # def changeGen(self):      ########### NOT IN USE, PROB TO BE DELETED
    #     # generates a new synthGen
    #     self.a = [synt.SynthGen() for i in range(self.synthNum)]
    #     return self

    def tempoModifier(self):
        # bursts of tempo change, used by "loop" only
        coin = random.random()
        if coin > 0.50:
            self.tempoMod = 1
        elif coin <= 0.50 and coin > 0.30:
            self.tempoMod = 2
        elif coin <=0.30 and coin > 0.10:
            self.tempoMod = 4
        elif coin <= 0.10:
            self.tempoMod = 8
        return self

    def changeMel(self):
        # changed the looped melody being played, used by "loop" only
        prevMel = self.currentMel
        pick = random.randint(0,len(self.mel)-1)
        self.currentMel = self.mel[pick]
        if self.currentMel == prevMel:
            self.melRepCount +=1
        if self.currentMel != prevMel:
            self.melRepCount = 0
        if self.melRepCount == 4:
            while self.currentMel == prevMel:
                pick = random.randint(0,len(self.mel)-1)
                self.currentMel = self.mel[pick]
            self.melRepCount = 0
        return self

    def loopMel(self, coin2 = 0):
        # plays the looped melody, used by "loop" only
        if self.melStep < len(self.currentMel):
            # 5% of the time, a note is pitchshifted
            coin = random.random()
            if coin >0.95:
                coin2 = random.random()
                if coin2 < 0.3:
                    mult = 2.
                elif coin2 >= 0.3 and coin2 < 0.5:
                    mult = 3.
                elif coin2 >=0.5 and coin2 < 0.7:
                    mult = 1.5
                else:
                    mult = 0.5
                [self.a[i].setNewFreq(self.currentMel[self.melStep]*mult) for i in range(self.synthNum)]
            else:
                [self.a[i].setNewFreq(self.currentMel[self.melStep]) for i in range(self.synthNum)]
            [self.a[i].setNewFreq(self.currentMel[self.melStep]) for i in range(self.synthNum)]
            self.melStep +=1
        # wraps around at the end of the melody
        else:
            [self.a[i].setNewFreq(self.currentMel[0]) for i in range(self.synthNum)]
            self.melStep = 0
        return self

    def keepTime(self):
        # modifies tempo according to MIDI CC
        self.beat.setTime(vari.mainTempo*self.tempo*self.tempoMod)
        self.patChangeMel.setTime(vari.mainTempo*self.tempo*16.)
        if self.notes == "loop":
            self.patTempoMod.setTime(vari.mainTempo*self.tempo)

    def newLoops(self):
        # generates a looped melody
        print "New loops"
        f = MelMaker().genMel(vari.scaleInUse, self.numMel)
        self.mel = f.getMel()
        self.beat.setW1(random.randint(80,100))
        self.beat.setW2(random.randint(10,60))
        self.beat.setW3(random.randint(30,60))
        return self



class AlgoSamp:
    def __init__(self, notes=[60], mainDur=15): 
        '''
        This module manages the samples being played.
        THIS IS NOW ALL DONE INSIDE samp.GranuleSf(), so this is quite empty
        '''
        self.grSamp = samp.GranuleSf(mainDur = mainDur)
        self.grSamp.out()



class Notes:
    def __init__(self, key='Rand', scale='Rand'):
        '''
        This class creates a list of notes in Hz to choose from for synths.
        '''
        self.pickNewNotes(key = key, scale = scale)

    def getListNotes(self):
        return self.notesFull

    def newNotes(self, key='Rand', scale='Rand'):
        ###

        # Determines if a new root/scale should be piked, or a previous one 
        # should be reused.
        if len(vari.rootColl) > vari.collLen:
            # Reuse
            coin = random.random()
            if coin > .5:
                # previous data is reused, independently from each other
                self.root = random.choice(vari.rootColl)
                self.notes = random.choice(vari.scaleColl)  
                self.selOctaves = random.choice(vari.octColl)

            else:
                # previous data is reused, same root/notes combo
                pick = random.randint(1, vari.collLen)
                self.root = vari.rootColl[pick]
                self.notes = vari.scaleColl[pick]
                self.selOctaves = vari.octColl[pick]

            self.notes = [x + self.root for x in self.notes]
            for i in self.selOctaves:
                for x in self.notes:
                    self.notesFull.append(x+i)
            self.notesFull.sort()
            vari.scaleInUse = [midiToHz(x) for x in self.notesFull]

        else:
            # Pick completely new notes
            self.pickNewNotes(key = key, scale = scale)

    def pickNewNotes(self, key='Rand', scale='Rand'):
            # Pick new
            if key == 'Rand':
                self.root = random.choice([60,48,36])
                # finding the root from the requested key
                self.root = 60+random.choice(cons.KEYS.values())
            else:
                # finding the root from the requested key
                self.root = 60+cons.KEYS[self.key]

            # add the root note to a list to retrieve later.
            vari.rootColl.append(self.root) 

            if scale == 'Rand':
                # getting the basic note list
                self.notes = random.choice(cons.SCALES.values())
            else:
                # getting the basic note list
                self.notes = cons.SCALES[self.scale]

            # add the scale to a list to retrieve later.
            vari.scaleColl.append(self.notes)   

            # adding the root to the notes list
            self.notes = [x + self.root for x in self.notes] 
            octaves = [12,24,36,-12,-24,-36]
            self.selOctaves = random.sample(octaves, random.randint(1,4))
            self.selOctaves.append(0)
            vari.octColl.append(self.selOctaves)
            self.notesFull = []
            for i in self.selOctaves:
                for x in self.notes:
                    self.notesFull.append(x+i)
            self.notesFull.sort()
            vari.scaleInUse = [midiToHz(x) for x in self.notesFull]


