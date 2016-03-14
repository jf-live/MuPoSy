# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
#
# Sample players

import constants as cons
import variables as vari
import os, random, fnmatch
import Trigs
from pyo import *


# s = Server().boot()
# s.start()


#chooses 1 random file in a given folder, excludes hidden files and folders
class RandListDir:
    def doIt(self,pathTo):
        toChoose = [f for f in os.listdir(pathTo) if f.endswith(".aif") or 
                                                     f.endswith(".wav") or 
                                                     f.endswith(".aiff")]
        toReturn = random.choice(toChoose)
        print "Sound loaded", toReturn
        return toReturn

    def doItDeep(self,pathTo):
        """
        Retourne des fichiers son pour un dossier et sa suite
        """
        self.toChoose = []

        for root, dirnames,filenames in os.walk(pathTo):
            for filename in fnmatch.filter(filenames, ("*.aif" or "*.wav" or "*.aiff")):
                self.toChoose.append(os.path.join(root,filename))
        toReturn = random.choice(self.toChoose)
        print "Sound loaded", toReturn
        return toReturn




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
            # rSound = RandListDir().doIt(path)
            rSound = RandListDir().doItDeep(path)
            sFile = os.path.join(path,rSound)
            self.sf = SfPlayer(sFile, speed)
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
        rSound = RandListDir().doIt(self.path)
        rSound = RandListDir().doItDeep(self.path)
        sFile = os.path.join(self.path,rSound)
        self.sf = SfPlayer(sFile, speed)


###class where granulation is used on soundfiles
class GranuleSf:
    """
    This class is to granulate a sound.
    Mode 0 is random sound.
    Mode 1 is a specific sound, needs to be specified with fileSel.
    """
    def __init__(self, mode = 0, path=cons.SFFOLDER_PATH, fileSel=cons.SONTEST, modu=1, dur=1):
        print "sample"
        self.t = SndTable()
        self.path = path
        self.fileSel = fileSel
        self.mode = mode
        randSel = random.randint(0,1) # Chooses if Granule or Granulator is used

        if self.mode == 0:
            # rSound = RandListDir().doIt(path)
            rSound = RandListDir().doItDeep(self.path)
            sFile = os.path.join(self.path,rSound)
            vari.sampColl.append(sFile)
            self.t.setSound(sFile)
        elif self.mode == 1:
            sFile = os.path.join(self.path,self.fileSel)
            vari.sampColl.append(sFile)
            self.t.setSound(sFile)
        grEnv = HannTable()
        
        ### Pour obtenir le sampling rate
        sr = grEnv.getServer().getSamplingRate()

        # end = self.t.getSize() - s.getSamplingRate() * 0.2
        end = self.t.getSize() - 48000 * 0.2  #version simplifiée (voir ligne précédente), à revoir...

        self.setEnv()

        self.noteEnv = Adsr(self.att, self.dec, self.sus, self.rel, dur = self.dur)

        if randSel == 0:
            self.pos = Xnoise(freq=10, mul=end)
            dns = Randi(min=20, max=30, freq=3)
            pit = Randi(min=0.59, max=2.01, freq=100)#+RandInt(20,1)
            self.gr = Granule(self.t, grEnv, dens=dns, pitch=pit, pos=self.pos, mul=self.noteEnv*0.8)

        else:
            self.pos = Phasor(self.t.getRate()*random.uniform(0.01,0.5), 0, self.t.getSize())
            dns = random.randint(10, 30)
            pit = Randi(min=0.59, max=2.01, freq=3)#+RandInt(20,1)
            self.gr = Granulator(self.t, grEnv, grains=dns, pitch=pit, pos=self.pos, mul=self.noteEnv*0.8)

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
            # new sampe
            coin = random.random()
            if coin > 0.5:
                if self.mode == 0:
                    # rSound = RandListDir().doIt(path)
                    rSound = RandListDir().doItDeep(self.path)
                    sFile = os.path.join(self.path,rSound)
                    vari.sampColl.append(sFile)
                    self.t.setSound(sFile)
                elif self.mode == 1:
                    sFile = os.path.join(self.path,self.fileSel)
                    vari.sampColl.append(sFile)
                    self.t.setSound(sFile)
            else:
                sFile = random.choice(vari.sampColl)
                self.t.setSound(sFile)
        else:
            # Reuse
            sFile = random.choice(vari.sampColl)
            self.t.setSound(sFile)


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
            outSig = SPan(self.gr, random.randint(0,cons.NUMOUTS)/cons.NUMOUTS)
        elif stereo == 1:
            #lfo between speakers
            a = LFO(freq=freq,type=3,mul=.5, add=.5)
            # b = SigTo(a, random.uniform(0.01,1))
            outSig = SPan(self.gr, cons.NUMOUTS, a)
        self.noteEnv.play()
        return outSig

    # To be used when first loading the sounds so they don't get all triggered 
    # all at once like with getOut()
    def getOutInit(self, stereo=1, freq=1):
        outSig = None
        if stereo == 0:
            #goes to 1 speaker
            outSig = SPan(self.gr, random.randint(0,cons.NUMOUTS)/cons.NUMOUTS)
        elif stereo == 1:
            #lfo between speakers
            a = LFO(freq=freq,type=3,mul=.5, add=.5)
            # b = SigTo(a, random.uniform(0.01,1))
            outSig = SPan(self.gr, cons.NUMOUTS, a)
        return outSig


    def out(self, stereo=1, freq=1):
        if stereo == 0:
            #goes to 1 speaker
            self.gr.out(random.randint(0,cons.NUMOUTS)/cons.NUMOUTS)
            self.noteEnv.play()
        elif stereo == 1:
            #lfo between speakers
            a = LFO(freq=freq,type=6,mul=.5, add=.5)
            b = SigTo(a, random.uniform(0.01,1))
            outSig = SPan(self.gr, cons.NUMOUTS, b).out()
            self.noteEnv.play()

        
    def outRand(self): #outputs sound with a new env different than initial
        self.resetEnv()
        self.gr.out()

    def getOutRand(self, lfoFreq = 1): #outputs sound with a new env different than initial
        self.resetEnv()
        a = self.getOut(lfoFreq)
        return a

    def chooseNew(self):
        # rSound = RandListDir().doIt(self.path)
        rSound = RandListDir().doItDeep(self.path)
        sFile = os.path.join(self.path,rSound)
        vari.sampColl.append(sFile)
        self.t.setSound(sFile)

# a = GranuleSf()

# def rep():
#     a.resetEnv()
# #   a.out()
#     a.getOut()

    
# c = LFO(freq=1,type=6,mul=.5, add=.5)
# d = SigTo(c, random.uniform(0.01,1))

# pat = Pattern(rep, time=2).play()

# # a = SoundRead(0, speed=2)
# # b = Freeverb(a.getOut(),.9).out()
# b = Pan(a.getOut(), 2, pan=d).out()



# s.gui(locals())
