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
class SoundRead(Sig):
    """
    This class is to read a soundfile using SfPlayer.
    Mode 0 is random sound.
    Mode 1 is a specific sound, needs to be specified with fileSel.
    If speed init argument is set to 400, the reading speed will be random.
    Modu is the amount of randomness for reading speed.  Default (1) is between
        -2 and 2.
    """
    def __init__(self, mode = 0, path=cons.SFFOLDER_PATH, fileSel=cons.SONTEST, speed=1, modu=1, mul=1, add=0):
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
            self.sf = SfPlayer(rSound, speed)
        elif mode == 1:
            self.sf = SfPlayer(self.fileSel, self.speed)
        Sig.__init__(self, self.sf, mul, add)

    def stop(self):
        self.sf.stop()
        return self


###class where granulation is used on soundfiles
class GranuleSf(Sig):
    """
    This class is to granulate a sound.
    Mode 0 is random sound.
    Mode 1 is a specific sound, needs to be specified with fileSel.  NOT IN USE!
    """
    def __init__(self, path=cons.SFFOLDER_PATH, modu=1, dur=1, mainDur = 15, mul=1,add=0):
        print "sample"
        global allSndsTables
        global allSnds
        self.path = path
        randSel = random.random() # Chooses if Granule or Granulator is used
        self.snd = None
        selSndIndex = random.randint(0,len(allSndsTables)-1)
        self.snd = allSndsTables[selSndIndex]   # Selects to table to be played
        vari.sampColl.append(allSnds[selSndIndex])  # To keep track of played samples

        # Grain envelope
        grEnv = CosTable([(0,.0),(1000,1.),(7191,1.),(8191,0.)])

        # global envelope
        globEnvRaise = random.randint(2000,4000)
        globEnvFall = random.randint(4100,6000)
        self.globEnv = CosTable([(0,.0),(globEnvRaise,1.),(globEnvFall,1.),(8191,0.)])
        
        ### Pour obtenir le sampling rate
        sr = grEnv.getServer().getSamplingRate()

        end = self.snd.getSize()

        # sets initial envelope and creates an Adsr with the values
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
        self.mulTableFreq = 1./mainDur
        self.mulTable = TableRead(self.globEnv,self.mulTableFreq).play()

        # main amp env is applied here
        self.gr2 = Compress(self.gr, -30,6,0.05, mul = self.mulTable*0.8)

        # panning stuff
        lfoFreq = random.uniform(0.1,1)
        self.lfoPan = LFO(freq=lfoFreq,type=random.randint(0,7),mul=.5, add=.5)
        self.toPan = SigTo(self.lfoPan, random.uniform(0.01,1))
        self.pan = SPan(self.gr2, cons.NUMOUTS, self.toPan)

        # reverb and out
        revFeed = random.uniform(0.6,0.9)
        self.grVerb = WGVerb(self.pan, [revFeed, revFeed*(random.uniform(0.98,1.02))])
        Sig.__init__(self, self.grVerb, mul, add)

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

    def chooseNew(self):
        revFeed = random.uniform(0.6,0.9)
        self.grVerb.feedback = [revFeed, revFeed*(random.uniform(0.98,1.02))]
        selSndIndex = random.randint(0,len(allSndsTables)-1)
        self.snd = allSndsTables[selSndIndex]   # Selects a table to be played
        vari.sampColl.append(allSnds[selSndIndex])  # To keep track of played samples
        self.noteEnv.play()




