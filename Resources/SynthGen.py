# encoding: utf-8

#Jean-Francois Primeau
#2016
#Digital Signal Generators


import constants as cons
import variables as vari
from pyo import *
import random

# s=Server().boot()


###Class where the audio signals are generated
class SynthGen:
    def __init__(self, freq=400, mod=1, mult=0.2, multMod=1, envDur = 3, wide=False):
        '''
        Wide is the parameter that controls if the gen is created for 1 channel,
            or for all channels.  False = 1 channel, True = all channels.

        '''
        self.freq = freq    #base frequency
        self.mod = mod      #modifier factor
        mult = mult*0.8
        self.multMod = multMod  
        self.envDur = envDur    #envelope duration
        self.wide = wide    #If gen is all channels or 1 channel
        self.randChooser = 2#int(random.triangular(0,13, random.randint(0,13)))
        # self.randChooser = 13
        print self.randChooser
        #0@5: LFO Saw Up, SawDown, Square, Triangle, Pulse, Bipolar Pulse
        #6: BLIT
        #7: RCOsc
        #8: SineLoop
        #9: CrossFM
        #10: FM
        #11@13: Osc tables


        # Temporary env to generate notes
        # Will need to be augmented to include no-zero envelopes, more 
        #   interesting shapes, etc.
        
        if vari.randEnvSynth >= 35:
            if self.envDur<3:
                self.attackT = random.random()/3
                self.decayT = random.uniform(0.01,0.5)/3
                self.releaseT = random.random()/3
            else:
                self.attackT = random.random()
                self.decayT = random.uniform(0.01,0.5)
                self.releaseT = random.random()
            self.dura = self.attackT + self.decayT + self.releaseT + self.envDur/4
            if self.dura > self.envDur:
                self.dura = self.envDur
            self.env = Adsr(self.attackT, self.decayT, 0.7, self.releaseT, self.dura).play()
        else:
            self.env = random.uniform(0.3,0.7)


        if self.randChooser <= 5:
            self.modifLFO = LFO(random.uniform(0.25,3)*(self.mod+0.001),
                                0.5,
                                random.randint(0,7),
                                1,0)
            self.modifLFOSig = SigTo(self.modifLFO,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,
                                 random.randint(0,7),
                                 .8,
                                 .2)
            if self.wide == True:
                self.sig = LFO([freq+random.random() for freq in range(cons.NUMOUTS)],
                               self.modifLFOSig,
                               self.randChooser,
                               mult*self.modifMult*self.env)
            else:
                self.sig = LFO(freq,
                           self.modifLFOSig,
                           self.randChooser,
                           mult*self.modifMult*self.env)

        elif self.randChooser == 6:
            self.modifBLIT = LFO(random.uniform(0.25,1.5)*(self.mod+0.001),
                                 0.5,random.randint(0,7),
                                 random.randint(5,20),
                                 random.randint(1,10)*(self.mod+0.001))
            self.modifBLITSig = SigTo(self.modifBLIT,0.25)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = Blit(freq,self.modifBLITSig,mult*self.modifMult*self.env)

        elif self.randChooser == 7:
            self.modifRC = LFO(random.uniform(0.25,3)*(self.mod+0.001),
                               0.5,random.randint(0,7),
                               1,
                               0)
            self.modifRCSig = SigTo(self.modifRC,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = RCOsc(freq, self.modifRCSig,mult*self.modifMult*self.env)

        elif self.randChooser == 8:
            self.modifSineLoop = LFO(random.uniform(0.25,3)*(self.mod+0.001),
                                     0.5,
                                     random.randint(0,7),
                                     random.uniform(0.01,.45),
                                     0)
            self.modifSineLoopSig = SigTo(self.modifSineLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = SineLoop(freq,self.modifSineLoopSig,mult*self.modifMult*self.env)

        elif self.randChooser == 9:
            self.modifCFMRatio = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                     0.5,
                                     random.randint(0,7),
                                     random.uniform(0.1,1),
                                     0)
            self.modifCFMRatioSig = SigTo(self.modifCFMRatio,0.2)
            self.modifCFMIndex1 = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                      0.5,
                                      random.randint(0,7),
                                      random.uniform(1,10),
                                      0)
            self.modifCFMIndex1Sig = SigTo(self.modifCFMIndex1,0.2)
            self.modifCFMIndex2 = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                      0.5,
                                      random.randint(0,7),
                                      random.uniform(1,10),
                                      0)
            self.modifCFMIndex2Sig = SigTo(self.modifCFMIndex2,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = CrossFM(freq, 
                               self.modifCFMRatioSig,
                               self.modifCFMIndex1Sig,
                               self.modifCFMIndex2Sig,
                               mult*self.modifMult*self.env)

        elif self.randChooser == 10:
            self.modifFMRatio = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                    0.5,random.randint(0,7),
                                    random.uniform(0.1,1),
                                    0)
            self.modifFMRatioSig = SigTo(self.modifFMRatio,0.2)
            self.modifFMIndex = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                    0.5,random.randint(0,7),
                                    random.uniform(1,10),
                                    0)
            self.modifFMIndexSig = SigTo(self.modifFMIndex,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = FM(freq, 
                          self.modifFMRatioSig,
                          self.modifFMIndexSig,
                          mult*self.modifMult*self.env)

        elif self.randChooser == 11:
            self.tableList = [(0.,0)]+ \
                             [(random.randint(1,8190), \
                             random.uniform(-1,1)) for i in \
                             range(int(random.triangular(5,100,10)))]+ \
                             [(8191,0)]
            self.tableList.sort()
            self.table = LogTable(self.tableList)
            self.modifOscLoop = LFO(random.uniform(0.25,3)*(self.mod+0.001),
                                    0.5,
                                    random.randint(0,7),
                                    random.uniform(0.01,.05),
                                    0)
            self.modifOscLoopSig = SigTo(self.modifOscLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,random.randint(0,7),
                                 .6,
                                 .2)
            self.sig = OscLoop(self.table, 
                               self.freq, 
                               self.modifOscLoopSig, 
                               mult*self.modifMult*self.env)

        elif self.randChooser == 12:
            self.tableList = [1.]+ \
                             [random.triangular(0.,.8) for \
                             i in range(random.randint(2,8))]
            self.table = HarmTable(self.tableList)
            self.modifOscLoop = LFO(random.uniform(0.25,3)*(self.mod+0.001),
                                    0.5,
                                    random.randint(0,7),
                                    random.uniform(0.01,.05),
                                    0)
            self.modifOscLoopSig = SigTo(self.modifOscLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,
                                 random.randint(0,7),
                                 .6,
                                 .2)
            self.sig = OscLoop(self.table, 
                               self.freq, 
                               self.modifOscLoopSig, 
                               mult*self.modifMult*self.env)

        elif self.randChooser == 13:
            self.tableList = [(0.,0)]+ \
                             [(random.randint(1,8190),random.uniform(-1,1)) for\
                             i in range(int(random.triangular(5,20,10)))]
            self.tableList = self.tableList+\
                             [(random.randint(1,8190),random.uniform(-.2,.2)) \
                             for i in range(int(random.triangular(5,random.randint(10,200),10)))]
            self.tableList = self.tableList+\
                             [(random.randint(1,8190),random.uniform(-1,1)) for\
                             i in range(int(random.triangular(5,20,10)))]+[(8191,0)]
            self.tableList.sort()
            self.table = LinTable(self.tableList)
            self.modifOscLoop = LFO(random.uniform(0.25,3)*(self.mod+0.001),
                                    0.5,
                                    random.randint(0,7),
                                    random.uniform(0.01,.05),
                                    0)
            self.modifOscLoopSig = SigTo(self.modifOscLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,3)*(self.multMod+0.001),
                                 0.5,
                                 random.randint(0,7),
                                 .6,
                                 .2)
            self.sig = OscLoop(self.table, 
                               self.freq, 
                               self.modifOscLoopSig, 
                               mult*self.modifMult*self.env)

    def repeat(self):
        '''
        Retrigs the envelope.
        '''
        print 'Env for SynthGen triggered'
        self.env.play()

    def repeatJit(self, walk = 1):
        '''
        Generates a new envelope from a walk from the previous one and trigs it.

        '''
        if self.envDur<3:
            self.attackT += random.random()/3*walk-0.5
            if self.attackT <= 0.:
                self.attackT = 0.1
            self.decayT += random.uniform(-0.2*walk,0.2*walk)/3
            if self.decayT <= 0.:
                self.decayT = 0.1
            self.releaseT += random.random()/3*walk-0.5
            if self.releaseT <= 0.:
                self.releaseT = 0.1        
        else:
            self.attackT += random.random()*walk-0.5
            if self.attackT <= 0.:
                self.attackT = 0.1
            self.decayT += random.uniform(-0.2*walk,0.2*walk)
            if self.decayT <= 0.:
                self.decayT = 0.1
            self.releaseT += random.random()*walk-0.5
            if self.releaseT <= 0.:
                self.releaseT = 0.1        
        self.dura = self.attackT + self.decayT + self.releaseT + self.envDur/4
        if self.dura > self.envDur:
            self.dura = self.envDur
        self.env.setAttack(self.attackT)
        self.env.setDecay(self.decayT)
        self.env.setRelease(self.releaseT)
        self.env.setDur(self.dura)
        self.env.play()

    def getOut(self):
        return self.sig.mix(cons.NUMOUTS)

    def out(self, outs=1, whatOut=0):
        self.sigOut = self.sig.mix(outs).out(whatOut)

    def getFreq(self):
        print self.freq

    def testing(self):
        print "testing"


    def getRandChooser(self):
        #prints the list of gen choices
        print self.randChooser

    def setNewNote(self):
        print 'new note'
        #Chooses a new note to play right from vari.scaleInUse
        freq = random.choice(vari.scaleInUse)
        if self.randChooser > 8 and self.randChooser <= 10:
            self.sig.setCarrier(freq)
        else:
            self.sig.setFreq(freq)
        print "test done"

    def setNewFreq(self,newFreq):
        freq = newFreq
        if self.randChooser > 8 and self.randChooser <= 10:
            self.sig.setCarrier(freq)
        else:
            self.sig.setFreq(freq)


    def setRandom(self, mini=200, maxi=3000):
        if self.randChooser > 8 and self.randChooser <= 10:
            self.sig.setCarrier(random.randint(mini,maxi))
        else:
            self.sig.setFreq(random.randint(mini,maxi))

    def stop(self):
        self.sig.stop()

#--------------------------------------------------------------------START-OLD

#####Tout ce qui concerne la spacialisation devrait être dans le module "effets"

# ###Class that calls the audio generators from SynthGen() and outputs them
# class SynthOut:
#   """This class calls a given number of signal generators. 
# The attributes are: 

#   numGens: number of signal generators to be created.  By defaul they all share the same root freq.
#   freq: the root frequency.
#   envMode: 0 for infinitely held notes, 1 for cycling amp enveloppe
#   modder: the amount of modulation to be applied, from 0 to 4 (can go higher, but might be a bit too wild)
#   multi: amplitude multiplier.  Better to keep it low.
#   multiMod: amplitude multiplier modulator.
#   maxOuts: number of output channels available
#   outMode: 0 for signal to all channels, 1 for signal to random channels, 2 for signal moving in circle around channels, 3 for random movements
#           4 for random movements to specific channels (no splitting the signal between channels)

#   """
#   def __init__(self, numGens=1, freq = 500, envMode = 0, modder = 0.3, multi = 0.5, 
#                      multiMod = 0.2, maxOuts = MAXCHANNELS):
#       self.numberGens = numGens
#       if envMode == 0:
#           ###Continuous
#           self.a = [SynthGen(freq*random.randint(1,3), 
#                               mod = modder, 
#                               mult = (multi+(multi*random.uniform(-0.5,0.5)))/numGens, 
#                               multMod = multiMod) for i in range(numGens)]
            
#       elif envMode == 1:
#           ###Cycling envelope
#           self.t = LinTable([(0,0), (100,1), (1000,.25), (8191,0)])
#           self.tRead = Osc(self.t, random.uniform(0.5,2), mul=.25)
#           self.a = [SynthGen(freq*random.randint(1,3), 
#                               mod = modder, 
#                               mult = (multi+(multi*random.uniform(-0.5,0.5)))*self.t, 
#                               multMod = multiMod) for i in range(numGens)]

#   def getOut(self):
#       return [self.a[i].getOut() for i in range(self.numberGens)]

#####Tout ce qui concerne la spacialisation devrait être dans le module "effets"
        # if outMode == 0:
        #   ###Every signal to all channels
        #   self.aOut = [self.a[i].out(maxOuts) for i in range(numGens)]

        # elif outMode == 1:
        #   ###Signal to random channels
        #   a = random.randint(0,maxOuts-1)
        #   self.aOut = [self.a[i].out(1,a) for i in range(numGens)]

        # elif outMode == 2:
        #   ###Signal moving in a circle aroung the channels (currently buggy: click when passing from 1 to 0)
        #   self.panPhase = [Phasor(random.uniform(0.01, 2), random.random()) for i in range(numGens)]
        #   self.aOut = [Pan(self.a[i].getOut(), 
        #                       maxOuts, 
        #                       self.panPhase[i], 
        #                       random.uniform(0,.5)).out() for i in range(numGens)]

        # elif outMode == 3:
        #   ###Signal moving randomly
        #   self.panSNH = [LFO(random.uniform(0.01, 2), 0.1, 6, .5, .5) for i in range(numGens)]
        #   self.aOut = [Pan(self.a[i].getOut(), 
        #                       maxOuts, self.panSNH[i], 
        #                       random.uniform(0,.5)).out() for i in range(numGens)]

        # elif outMode == 4:
        #   ###Signal moving randomly
        #   self.m = Metro(1).play()
        #   self.trigm = [TrigRandInt(self.m,maxOuts-1) for i in range(numGens)]
        #   self.testing = TrigFunc(self.m,self.printing)
        #   self.aOut = [Pan(self.a[i].getOut(), 
        #                       maxOuts, self.trigm[i], 0).out() for i in range(numGens)]


#----------------------------------------------------------------------END-OLD

### 'a' is a list of signal generator instances.  
###     To retrieve a stream for manipulation, use a[0], a[1], ...
# a = [SynthGen() for i in range(3)]
# a1 = [a[i].getOut() for i in range(3)]
# r = Sine(1,mul=0.5,add=0.5)
# a2 = Pan(a1, 2, r)
# b = Freeverb(a2).mix(2).out()
# b = SynthOut()
# c = SynthOut()

# s.gui(locals())










