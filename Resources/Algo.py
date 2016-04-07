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



class AlgoGen(Sig):
    def __init__(self, notes="normal", tempo = 0.25, mul=1, add=0): 
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
        if notes == "normal":
            self.whatFunc = self.changeNote
        elif notes == "low":
            self.whatFunc = self.changeNoteLow
        self.tfunc = TrigFunc(self.beat, self.whatFunc)
        self.trig = TrigEnv(self.beat, self.env, self.beat['dur'])
        # First, generate a sound
        self.synthNum = random.randint(1,5)  # how many synthGen instances will compose a note
        self.a = [synt.SynthGen(mul = self.trig*vari.synthGenMul) for i in range(self.synthNum)]

        self.patMul = Pattern(self.settingMul,0.05).play()

        self.b = [self.a[i] for i in range(self.synthNum)]


        Sig.__init__(self,self.b,mul,add)

    def changeNote(self):
        self.newNote = random.choice(vari.scaleInUse)
        [self.a[i].setNewFreq(self.newNote) for i in range(self.synthNum)]
        return self
    def changeNoteLow(self):
        self.newNote = random.choice(vari.scaleInUse[0:3])
        if self.newNote >= 400:
            self.newNote /= random.choice([8,16])
        print self.newNote
        [self.a[i].setNewFreq(self.newNote) for i in range(self.synthNum)]
        return self

    def changeGen(self):
        self.a = [synt.SynthGen() for i in range(self.synthNum)]

    def settingMul(self):
        print "mul"
        [self.a[i].setMul(vari.synthGenMul) for i in range(self.synthNum)]
        return self




class AlgoSamp:
    def __init__(self, notes = [60],dur=30, noteDur=5): 
        '''
        This module manages the samples being played.
        '''
        # Generates sound from a granulated audio file
        self.b = samp.GranuleSf(mainDur = dur)
        self.b.out()
        modulB = random.random()/10
        print "modulation b: ", modulB

        # Change the samples in the order they were called to prevent calling before
        # playback is done.

        coin = random.random()
        randFreq = random.randint(3,20)
        if coin >0.5:
            self.tFreq = Randi(0.1,2,randFreq)
            self.trig = Cloud(self.tFreq).play()
        else:
            self.tFreq = Randh(1,3,randFreq)
            self.trig = Beat(self.tFreq).play()

        self.patB1 = TrigFunc(self.trig,self.repChoice)

    def repChoice(self):
        self.b.chooseNew()
        return self





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
        self.selOctaves = random.sample(octaves, random.randint(1,4))
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


