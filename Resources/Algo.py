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
    def __init__(self, freqs, numMel):
        self.freqs = freqs
        self.numMel = numMel # how many melodies will be generated
        self.mel = []  # to store the melodies
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

    def getMel(self):
        return self.mel


class AlgoGen(Sig):
    def __init__(self, notes="normal", tempo = 0.25, side= "mid", mul=1, add=0): 
        '''
        This module generates a stream of notes, with a specified root note.
        Duration of this stream is specified in seconds.
        '''
        self.tempo = tempo
        primaryBeat = random.randint(80,100)
        secondaryBeat = random.randint(10,60)
        thirdBeat = random.randint(30,60)
        self.beat = Beat(self.tempo,8, 100,10,10).play()
        self.env = CosTable([(0,.0),(3000,1.),(5191,1.),(8191,0.)])
        # to keep track of which step of the melody is being played
        self.melStep = 0
        # how many melodies will be generated
        self.numMel = random.randint(2,4)
        # to store the generated looped melody
        self.mel = []

        # generates a looped melody
        f = MelMaker(vari.scaleInUse, self.numMel)
        self.mel = f.getMel()

        randInit = random.randint(0,len(self.mel)-1)
        self.currentMel = self.mel[randInit]
        self.melRepCount = 0
        # change melody every 16 notes played
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

        self.tfunc = TrigFunc(self.beat, self.whatFunc)
        self.trigEnv = TrigEnv(self.beat, self.env, self.beat['dur'])

        self.patUpdateTempo = Pattern(self.keepTime,0.05).play()

        self.synthNum = random.randint(1,5)  # how many synthGen instances will compose a note
        self.a = [synt.SynthGen(inst=self.inst,side=side,mul=self.trigEnv*vari.synthGenMul) for i in range(self.synthNum)]
        self.forOut = sum(self.a)
        Sig.__init__(self,self.forOut,[mul,mul],add)

    def keepTime(self):
        # modifies tempo according to MIDI CC
        self.beat.setTime(vari.mainTempo)
        self.patChangeMel.setTime(vari.mainTempo*16.)

    def changeNote(self):
        # plays random notes in key
        coin = random.random()
        if coin > 0.9:
            self.newNote = random.choice(vari.scaleInUse[-4:])
            [self.a[i].setNewFreq(self.newNote) for i in range(self.synthNum)]
        return self

    def changeNoteLow(self):
        # plays random bass notes in key
        self.newNote = random.choice(vari.scaleInUse[0:3])
        if self.newNote >= 400:
            self.newNote /= random.choice([8,16])
        [self.a[i].setNewFreq(self.newNote) for i in range(self.synthNum)]
        return self

    def changeGen(self):
        # generates a new synthGen
        self.a = [synt.SynthGen() for i in range(self.synthNum)]
        return self

    def changeMel(self):
        # changed the looped melody being played
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
        # plays the looped melody
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



class AlgoSamp:
    def __init__(self, notes=[60], mainDur=15): 
        '''
        This module manages the samples being played.
        THIS IS NOW ALL DONE INSIDE samp.GranuleSf()
        '''
        self.grSamp = samp.GranuleSf(mainDur = mainDur)
        self.grSamp.out()



class Notes:
    def __init__(self, key='Rand', scale='Rand'):
        '''
        This class creates a list of notes in Hz to choose from for melodies.
        '''
        self.key = key
        self.scale = scale

        if self.key == 'Rand':
            self.root = random.choice([60,48,36])
            self.root = 60+random.choice(cons.KEYS.values())          #finding the root from the requested key
        else:
            self.root = 60+cons.KEYS[self.key]        #finding the root from the requested key

        # add the root note to a list to retrieve later.
        vari.rootColl.append(self.root) 

        if self.scale == 'Rand':
            self.notes = random.choice(cons.SCALES.values())          #getting the basic note list
        else:
            self.notes = cons.SCALES[self.scale]          #getting the basic note list

        # add the scale to a list to retrieve later.
        vari.scaleColl.append(self.notes)   

        self.notes = [x + self.root for x in self.notes]      #adding the root to the notes list
        octaves = [12,-12,-24,-36]
        self.selOctaves = random.sample(octaves, random.randint(2,4))
        self.selOctaves.append(0)
        vari.octColl.append(self.selOctaves)
        self.notesFull = []
        for i in self.selOctaves:
            for x in self.notes:
                self.notesFull.append(x+i)
        self.notesFull.sort()
        print "scale: ", self.notesFull
        vari.scaleInUse = [midiToHz(x) for x in self.notesFull]

    def getListNotes(self):
        return self.notesFull

    def getListHz(self):
        self.hzFull = []
        self.hzFull = [midiToHz(x) for x in self.notesFull]  #notes converted to Hz
        return self.hzFull

    def newNotes(self, key='Rand', scale='Rand'):
        self.key = key
        self.scale = scale

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
            # Pick new
            if self.key == 'Rand':
                self.root = random.choice([60,48,36])
                self.root = 60+random.choice(cons.KEYS.values())          #finding the root from the requested key
            else:
                self.root = 60+cons.KEYS[self.key]        #finding the root from the requested key

            # add the root note to a list to retrieve later.
            vari.rootColl.append(self.root) 

            if self.scale == 'Rand':
                self.notes = random.choice(cons.SCALES.values())          #getting the basic note list
            else:
                self.notes = cons.SCALES[self.scale]          #getting the basic note list

            # add the scale to a list to retrieve later.
            vari.scaleColl.append(self.notes)   


            self.notes = [x + self.root for x in self.notes]      #adding the root to the notes list
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


