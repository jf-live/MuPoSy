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
import Effects as effe
import os, random, fnmatch, time
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

    def returnTrig(self):
        return self.sf['trig']


###class where granulation is used on soundfiles
class GranuleSf(Sig):
    """
    This class is to granulate a sound.
    """
    def __init__(self, path=cons.SFFOLDER_PATH, dur=1, mainDur = 15, mul=1,add=0):
        print "sample"
        global allSndsTables
        global allSnds
        self.path = path
        selSndIndex = random.randint(0,len(allSndsTables)-1)
        self.snd = allSndsTables[selSndIndex]   # Selects to table to be played at init
        vari.sampColl.append(selSndIndex)  # To keep track of played samples
        self.mulInter = vari.synthGenMul  # fades according to interaction input

        # Grain envelope
        grEnv = CosTable([(0,.0),(1000,1.),(7191,1.),(8191,0.)])

        # sets initial envelope and creates an Adsr with the values
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
        self.noteEnv = Adsr(self.att, self.dec, self.sus, self.rel, dur = self.dur)

        randSel = random.random() # Chooses if Granule or Granulator is used
        if randSel >= 0.5:
            end = self.snd.getSize()
            self.pos = Xnoise(freq=10, mul=end)
            dns = Randi(min=20, max=30, freq=3)
            pit = Randi(min=0.59, max=2.01, freq=Randi(0.5,4,3))
            self.gr = Granule(self.snd, grEnv, dens=dns, pitch=pit, pos=self.pos, mul=self.noteEnv*0.7)

        else:
            self.pos = Phasor(self.snd.getRate()*random.uniform(0.01,0.5), 0, self.snd.getSize())
            dns = random.randint(10, 30)
            pit = Randi(min=0.59, max=2.01, freq=Randi(0.5,4,3))
            self.gr = Granulator(self.snd, grEnv, grains=dns, pitch=pit, pos=self.pos, mul=self.noteEnv*0.7)

        self.grClip = Clip(self.gr)
        self.gr2 = Compress(self.grClip, -30,6,0.05, mul = 0.5*self.mulInter)
        self.gr3 = effe.Harmon(self.gr2,mix = 0.5)
        self.gr4 = effe.Delayer(self.gr3)
        # self.gr5 = ButHP(self.gr4, 30)
        self.gr5 = ButHP(self.gr4, vari.outFiltFreqSig)
        self.gr6 = DCBlock(self.gr5) # DC problems introduced by vari.outFiltFreqSig, DCBlock will do for now...

        # panning stuff
        lfoFreq = random.uniform(0.1,1)
        self.lfoPan = LFO(freq=lfoFreq,type=random.randint(0,7),mul=.5, add=.5)
        self.toPan = SigTo(self.lfoPan, random.uniform(0.01,1))
        self.pan = SPan(self.gr6, cons.NUMOUTS, self.toPan)

        # reverb and out
        revFeed = random.uniform(0.5,0.9)
        lfoFreqBal = random.uniform(0.1,1)
        self.revBal = LFO(freq=lfoFreqBal,type=6).range(0.5,1)
        self.grVerb = WGVerb(self.pan, [revFeed, revFeed*random.uniform(0.98,1.02)], self.revBal)
        Sig.__init__(self, self.grVerb, mul, add)

        self.patChooseNew = Pattern(self.chooseNew,self.dur + random.uniform(0.2,4)).play(delay = random.uniform(1,3))

    def setEnv(self):  
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
        self.dur = (self.att+self.dec+self.rel)+random.uniform(0.1, 6)

    def chooseNew(self):
        print "chooseNEW"
        self.gr.stop()
        self.gr3.mix = random.random()

        # changes the reverb fb once in a while
        coinRev = random.random()
        if coinRev > 0.8: 
            revFeed = random.uniform(0.5,0.9)
            self.grVerb.feedback = [revFeed, revFeed*(random.uniform(0.98,1.02))]

        # 60% of the time, a new sample is selected until the list runs out, at
        #                  which point the list is cleared and starts anew.
        # 20% of the time, a previous sample is repeated,
        # 20% of the time, the sample just played is repeated
        coinSamp = random.random()
        if coinSamp > 0.4:
            # makes sure all the samples are played once before repeating
            if len(vari.sampColl) != len(allSnds):
                selSndIndex = random.randint(0,len(allSndsTables)-1)
                while allSnds[selSndIndex] in vari.sampColl:
                    selSndIndex = random.randint(0,len(allSndsTables)-1)
            else:
                vari.sampColl = []
                selSndIndex = random.randint(0,len(allSndsTables)-1)
            self.gr.setTable(allSndsTables[selSndIndex])   ### CREATES THE BIG NOISE OF INFINITE DEATH (sometimes) !!!!! NOT ANYMORE :D
            vari.sampColl.append(selSndIndex)  # To keep track of played samples
        elif coinSamp > 0.2 and coinSamp <= 0.4:
            print len(vari.sampColl)
            print vari.sampColl
            if len(vari.sampColl) == 1:
                selSndIndex = random.randint(0,len(allSndsTables)-1)
                vari.sampColl.append(selSndIndex)
            else:
                selSndIndex = random.choice(vari.sampColl)

            self.gr.setTable(allSndsTables[selSndIndex])
        elif coinSamp <= 0.2:
            selSndIndex = random.randint(0,len(allSndsTables)-1)

        # changes the position pointer type
        coinPos = random.random()
        if coinPos > 0.2:
            self.gr.pos = Xnoise(freq=10, mul=allSndsTables[selSndIndex][0].getSize())
        else:
            self.gr.pos = Phasor(allSndsTables[selSndIndex][0].getRate()*random.uniform(0.01,0.5), 
                                 0, 
                                 allSndsTables[selSndIndex][0].getSize())
        self.gr4.setTimeFb()
        self.patChooseNew.time = self.dur + random.uniform(2,4)
        self.setEnv()
        self.gr.play()
        self.noteEnv.play(delay=0.1)  # delay applied to prevent the BIG NOISE OF INFINITE DEATH



