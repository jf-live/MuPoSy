# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
#
# Sample players

import constants as cons
import variables as vari
import utilities as util
import os, random, fnmatch
from pyo import *


# first load all samples in tables
allSnds = []
allSndsTables = []

def loadObjSono(path=cons.SFFOLDER_PATH):
    global allSnds
    global allSndsTables
    # loads all samples from path
    allSnds = util.RandListDir_noHidden().deepAll(path)
    for i in allSnds:
        a = SndTable(i)
        allSndsTables.append(a)


loadObjSono()

print "# of loaded samples:", len(allSndsTables)



###class where SfPlayer is used, for minimally modified sounds
class SoundRead:
    """
    This class is to read a soundfile using SfPlayer.
    Mode 0 is random sound.
    Mode 1 is a specific sound, needs to be specified with fileSel.
    If speed init argument is set to 400, the reading speed will be random.
    Modu is the amount of randomness for reading speed.  Default (1) is between
        -2 and 2.
    """
    def __init__(self, mode = 0, path=cons.SFFOLDER_PATH, fileSel=cons.SONTEST, speed=1, modu=1):
        print "testingSndRead"
        print fileSel
        self.sf = None
        if speed == 400:
            speed = random.uniform(-2*modu,2*modu)
            while speed > -0.1 and speed < 0.1:
                speed = random.uniform(-2*modu,2*modu)
        self.path = path
        self.fileSel = fileSel
        self.speed = speed
        if mode == 0:
            rSound = util.RandListDir_noHidden().doItDeep(self.path)
            # sFile = os.path.join(path,rSound)
            # self.sf = SfPlayer(sFile, speed)
            self.sf = SfPlayer(rSound, speed)
        elif mode == 1:
            self.sf = SfPlayer(self.fileSel, self.speed)

    def stop(self):
        self.sf.stop()
        return self

    def getOut(self):
        self.sf.play()
        return self.sf

    def out(self):
        self.sf.out()

    def chooseNew(self, speed = None):
        if speed == None:
            speed = self.speed
        else:
            self.speed = speed
        rSound = RandListDir_noHidden().doItDeep(self.path)
        # sFile = os.path.join(self.path,rSound)
        self.sf = SfPlayer(rSound, speed)


###class where granulation is used on soundfiles
class GranuleSf:
    """
    This class is to granulate a sound.
    Mode 0 is random sound.
    Mode 1 is a specific sound, needs to be specified with fileSel.  NOT IN USE!
    """
    def __init__(self, mode = 0, path=cons.SFFOLDER_PATH, fileSel=cons.SONTEST, modu=1, dur=1, mainDur = 15):
        print "sample"
        global allSndsTables
        global allSnds
        # self.t = SndTable()
        self.path = path
        self.fileSel = fileSel
        self.mode = mode
        randSel = random.random() # Chooses if Granule or Granulator is used
        self.snd = None
        if self.mode == 0:
            selSndIndex = random.randint(0,len(allSndsTables)-1)
            # self.snd = random.choice(allSndsTables)
            self.snd = allSndsTables[selSndIndex]   # Selects to table to be played
            vari.sampColl.append(allSnds[selSndIndex])  # To keep track of played samples
        # NOT IN USE:
        elif self.mode == 1:   # THIS DOES NOT WORK ANY MORE, CAUSED PROBLEMS WITH LATE LOADING OF SAMPLES
            sFile = os.path.join(self.path,self.fileSel)
            vari.sampColl.append(sFile)
            self.t.setSound(sFile)   # THIS DOES NOT WORK ANY MORE, CAUSED PROBLEMS WITH LATE LOADING OF SAMPLES
        
        grEnv = HannTable()

        # global envelope
        self.globEnv = CosTable([(0,.0),(100,1.),(8091,1.),(8191,0.)])
        
        ### Pour obtenir le sampling rate
        sr = grEnv.getServer().getSamplingRate()

        end = self.snd.getSize()

        self.setEnv()

        self.noteEnv = Adsr(self.att, self.dec, self.sus, self.rel, dur = self.dur)

        if randSel >= 0.5:
            self.pos = Xnoise(freq=10, mul=end)
            dns = Randi(min=20, max=30, freq=3)
            pit = Randi(min=0.59, max=2.01, freq=100)#+RandInt(20,1)
            self.gr = Granule(self.snd, grEnv, dens=dns, pitch=pit, pos=self.pos, mul=self.noteEnv*0.7)

        else:
            self.pos = Phasor(self.snd.getRate()*random.uniform(0.01,0.5), 0, self.snd.getSize())
            dns = random.randint(10, 30)
            pit = Randi(min=0.59, max=2.01, freq=3)#+RandInt(20,1)
            self.gr = Granulator(self.snd, grEnv, grains=dns, pitch=pit, pos=self.pos, mul=self.noteEnv*0.7)

        # applies main amplitude envelope
        self.mulTableFreq = 1./dur
        self.mulTable = TableRead(self.globEnv,self.mulTableFreq).play()


        self.gr2 = Compress(self.gr, -30,300,10, mul = 0.6* self.mulTable)

    def setEnv(self):  #sets initial attributes for Adsr env
        self.att = random.uniform(0.01,1)
        if self.att > 0.5:
            self.dec = random.uniform(0.01,0.5)
        else:
            self.dec = random.uniform(0.01,1)
        self.sus = random.uniform(0.5,0.95)
        if self.att + self.dec > 0.5:
            self.rel = random.uniform(0.01,0.5)
        else:
            self.rel = random.uniform(0.01,1)
        self.dur = (self.att+self.dec+self.rel)+random.uniform(0.01, 0.5)
        print self.att, self.dec, self.rel, self.dur

    def changeSamp(self, mode = 0, path=cons.SFFOLDER_PATH, fileSel=cons.SONTEST): # changes sample being played
        self.mode = mode
        self.fileSel = fileSel
        self.path = path
        if len(vari.sampColl) < vari.sampCollLen:
            coin = random.random()
            # New sound being played:
            if coin >= 0.5:
                if self.mode == 0:
                    selSndIndex = random.randint(0,len(allSndsTables)-1)
                    # self.snd = random.choice(allSndsTables)
                    self.snd = allSndsTables[selSndIndex]   # Selects to table to be played
                    vari.sampColl.append(allSnds[selSndIndex])  # To keep track of played samples
                    # self.snd = random.choice(allSndsTables)
                    # vari.sampColl.append(sFile)
                ### DOES NOT WORK, PROBLEMS WHEN CHANGING SAMPLE:
                elif self.mode == 1:
                    sFile = os.path.join(self.path,self.fileSel)
                    vari.sampColl.append(sFile)
                    self.t.setSound(sFile)
            # Prevously played sound:
            else:
                selSndIndex = random.choice(vari.sampColl)
                index = allSnds.index(selSndIndex)
                self.snd = allSndsTables[index]   # Selects to table to be played
        else:
            # Reuse
            selSndIndex = random.choice(vari.sampColl)
            index = allSnds.index(selSndIndex)
            self.snd = allSndsTables[index]   # Selects to table to be played


    def resetEnv(self):  #sets new attributes for Adsr env
        self.att = random.uniform(0.01,1)
        if self.att > 0.5:
            self.dec = random.uniform(0.01,0.5)
        else:
            self.dec = random.uniform(0.01,1)
        self.sus = random.uniform(0.5,0.95)
        if self.att + self.dec > 0.5:
            self.rel = random.uniform(0.01,0.5)
        else:
            self.rel = random.uniform(0.01,1)
        self.dur = (self.att+self.dec+self.rel)+random.uniform(0.01, 0.5)
        print self.att, self.dec, self.rel, self.dur
        self.noteEnv.attack = self.att
        self.noteEnv.decay = self.dec
        self.noteEnv.sustain = self.sus
        self.noteEnv.release = self.rel

    # When using this one to load a sound, it is immediately played.
    def getOut(self, stereo=1, freq=1):
        outSig = None
        if stereo == 0:
            #goes to 1 speaker
            outSig = SPan(self.gr2, random.randint(0,cons.NUMOUTS)/cons.NUMOUTS)
        elif stereo == 1:
            #lfo between speakers
            a = LFO(freq=freq,type=3,mul=.5, add=.5)
            # b = SigTo(a, random.uniform(0.01,1))
            outSig = SPan(self.gr2, cons.NUMOUTS, a)
        self.noteEnv.play()
        return outSig

    # To be used when first loading the sounds so they don't get all triggered 
    # all at once like with getOut()
    def getOutInit(self, stereo=1, freq=1):
        outSig = None
        if stereo == 0:
            #goes to 1 speaker
            outSig = SPan(self.gr2, random.randint(0,cons.NUMOUTS)/cons.NUMOUTS)
        elif stereo == 1:
            #lfo between speakers
            a = LFO(freq=freq,type=3,mul=.5, add=.5)
            # b = SigTo(a, random.uniform(0.01,1))
            outSig = SPan(self.gr2, cons.NUMOUTS, a)
        return outSig


    def out(self, stereo=1, freq=1):
        if stereo == 0:
            #goes to 1 speaker
            self.gr2.out(random.randint(0,cons.NUMOUTS)/cons.NUMOUTS)
            self.noteEnv.play()
        elif stereo == 1:
            #lfo between speakers
            a = LFO(freq=freq,type=6,mul=.5, add=.5)
            b = SigTo(a, random.uniform(0.01,1))
            outSig = SPan(self.gr, cons.NUMOUTS, b).out()
            self.noteEnv.play()

        
    def outRand(self): #outputs sound with a new env different than initial
        self.resetEnv()
        self.gr2.out()

    def getOutRand(self, lfoFreq = 1): #outputs sound with a new env different than initial
        self.resetEnv()
        self.a = self.getOut(lfoFreq)
        return self.a

    def chooseNew(self):
        self.gr2.mul = SigTo(0,0.005)
        selSndIndex = random.randint(0,len(allSndsTables)-1)
        self.snd = allSndsTables[selSndIndex]   # Selects to table to be played
        vari.sampColl.append(allSnds[selSndIndex])  # To keep track of played samples
        self.gr2.mul = self.noteEnv*0.8

