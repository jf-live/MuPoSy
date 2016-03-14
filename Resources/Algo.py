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
import random, threading, time



class AlgoGen:
    def __init__(self, notes = [60],dur=30, noteDur=5): 
        '''
        This module generates a stream of notes, with a specified root note.
        Duration of this stream is specified in seconds.

        '''
        self.notes = notes
        self.dur = dur
        self.noteDur = noteDur
        self.timeUp = 0  # Time to have the amp of the effects chain go to 1
        self.timeDown = 0  # Time to have the amp of the effects chain go to 0

        # First, generate a sound

        self.synthNum = random.randint(1,5)  # how many synthGen instances will compose a note
        print 'algo 1', self.synthNum
        self.a = [synt.SynthGen(envDur = self.noteDur) for i in range(self.synthNum)]
        print "self.a",self.a
        print "self.a",self.a[0]
        self.a1 = [self.a[i].getOut() for i in range(self.synthNum)]

        #Then applies effects on the list of synths
        #modul changes the intensity or amount of the effects (between 0 and 1)

        sfxNum = random.randint(1,5)
        modulA = random.random()
        print "modulation a: ", modulA
        self.a2 = effe.Sfxs(self.a1,modu=modulA, numFXs=sfxNum, mult=0.8)
        print self.a2.getDur()
        self.tDown = threading.Thread(target=self.volDown).start()


    def volDown(self):
        time.sleep(self.a2.getDur()+2)
        self.ending()

    def ending(self):
        print 'Ending AlgoGen'
        del self.a,self.a1,self.a2,self.trigA1,self.trigA2,self.trigA3,self.tDown

    def doinIt(self,time=10):
        '''
        arg time defines the life duration of the synth line.  Set notes chosen.
        '''
        self.time = time
        ## Evolves the parameters of the gens
        # self.trigA0 = TrigFunc(util.genMet, [self.a[i].setEvo(i) for i in range(self.synthNum)])
        #For a minimum of variation, selects new random pitch every few seconds.
        # self.trigA1 = TrigFunc(util.genMet, [self.a[i].setNewNote() for i in range(self.synthNum)])   #### MOVED DOWN A FEW LINES
        #and triggers the notes also every 3 seconds, 65% this script is run.
        # 35% of the time it is a continuous stream of sound
        if vari.randEnvSynth >= 35:
            self.trigA1 = TrigFunc(util.genMet, [self.a[i].setNewNote() for i in range(self.synthNum)])
            self.trigA2 = TrigFunc(util.genMet, self.retriggin)
        else:
            #For a minimum of variation, selects new random pitch every few seconds.
            print "self.a",self.a
            print "self.a",self.a[0]
            self.trigA0 = TrigFunc(util.genMet, self.a[0].testing)
            self.trigA1 = TrigFunc(util.genMet, self.a[0].setNewNote)
            # self.trigA1 = TrigFunc(util.genMet, [self.a[i].setNewNote() for i in range(self.synthNum)])

        #To trigger set notes, via patA2
    def retriggin(self):
        [self.a[i].repeatJit() for i in range(self.synthNum)]


    def doinItRand(self,time=10):
        '''
        arg time defines the life duration of the synth line.  Random freq chosen.
        '''
        self.time = time

        #For a minimum of variation, selects new random pitch every 3 seconds.
        self.patA1 = Pattern([self.a[i].setRandom for i in range(self.synthNum)], time=self.noteDur).play()
        #and triggers the notes also every 3 seconds, 65% this script is run.
        # 35% of the time it is a continuous stream of sound
        if vari.randEnvSynth >= 35:
            self.patA2 = Pattern(self.retrigginRand, self.noteDur).play()

        self.end = CallAfter(self.ending,self.time).play()

        #To trigger random notes
    def retrigginRand(self):
        print 'algo going'
        [self.a[i].repeat() for i in range(self.synthNum)]




class AlgoSamp:
    def __init__(self, notes = [60],dur=30, noteDur=5): 
        '''
        This module manages the samples being played.
        '''

        # Generates sound from a granulated audio file
        self.b = [samp.GranuleSf() for i in range(4)]
        self.b1 = [self.b[i].getOutInit() for i in range(4)]

        modulB = random.random()/10
        print "modulation b: ", modulB
        self.b2 = effe.Sfxs(self.b1[i],modu=modulB, numFXs=random.randint(1,4))
        # Get the duration of the main env
        self.bTime = self.b2.getDur()
        self.patTime = random.randint(1,4)
        # Change the samples in the order they were called to prevent calling before
        # playback is done.
        self.chSamp = 0
        self.tDown = threading.Thread(target=self.volDown).start()

        self.tFreq = Randi(0.5,3,10)
        # trig = Cloud(tFreq).play()
        self.trig = Beat(1).play()
        self.patB1 = TrigFunc(self.trig,self.repChoice)
        self.patB2 = Pattern(self.beatFill, time=self.patTime).play()

    def volDown(self):
        time.sleep(self.bTime+2)
        self.ending()

    def ending(self):
        print 'Ending AlgoSamp'
        del self.b,self.b1,self.b2,self.tDown, self.tFreq, self.trig, self.patB1, self.patB2

    def repChoice(self):
        self.b[self.chSamp].mul = SigTo(0,0.05)
        self.b[self.chSamp].chooseNew()
        self.b1[self.chSamp] = self.b[self.chSamp].getOutRand(random.uniform(0.001,2))
        # patB1.time = random.triangular(0.01,10,1)
        self.chSamp += 1
        if self.chSamp == 4:
            self.chSamp = 0

    def beatFill(self):
        self.trig
        self.trig.fill()






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
        print "scale", vari.scaleInUse

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


