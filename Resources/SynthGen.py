# encoding: utf-8

#Jean-Francois Primeau
#2016
#Digital Signal Generators


import constants as cons
import variables as vari
from pyo import *
import random


###Class where the audio signals are generated
class SynthGen(Sig):
    def __init__(self, freq=400, mod=1, multMod=1, wide=True, side = "mid", mul=1,add=0):
        '''
        Wide is the parameter that controls if the gen is created for 1 channel,
            or for all channels.  False = 1 channel, True = all channels.

        '''
        self.freq = freq    #base frequency
        self.freq0 = self.freq  # for SigTo(freq...)
        self.mod = mod      #modifier factor
        self.multMod = multMod  
        self.mulInter = vari.synthGenMul
        self.wide = wide    #If gen is all channels or 1 channel
        self.randChooser = int(random.triangular(0,13, random.randint(0,13)))

        #0@5: LFO Saw Up, SawDown, Square, Triangle, Pulse, Bipolar Pulse
        #6: BLIT
        #7: RCOsc
        #8: SineLoop
        #9: CrossFM
        #10: FM
        #11@13: Osc tables

        # assign randomly a snd gen
        if self.randChooser <= 5:
            self.modifLFO = LFO(random.uniform(0.25,1.5)*(self.mod+0.001),
                                random.uniform(0.2,0.8),
                                random.randint(0,7),
                                1,0)
            self.modifLFOSig = SigTo(self.modifLFO,0.2)
            self.modifMult = LFO(random.uniform(0.25,1)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .8,
                                 .2)
            if self.wide == True:
                self.sig = LFO([freq*random.uniform(0.98,1.02) for i in range(cons.NUMOUTS)],
                               self.modifLFOSig,
                               self.randChooser, self.modifMult*self.mulInter)
            else:
                self.sig = LFO(freq,
                           self.modifLFOSig,
                           self.randChooser, self.modifMult*self.mulInter)

        elif self.randChooser == 6:
            self.modifBLIT = LFO(random.uniform(0.25,1.5)*(self.mod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 random.randint(5,10),
                                 random.randint(1,8)*(self.mod+0.001))
            self.modifBLITSig = SigTo(self.modifBLIT,0.25)
            self.modifMult = LFO(random.uniform(0.25,1)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = Blit(freq,self.modifBLITSig, self.modifMult*self.mulInter)

        elif self.randChooser == 7:
            self.modifRC = LFO(random.uniform(0.25,1.5)*(self.mod+0.001),
                               random.uniform(0.2,0.8),
                               random.randint(0,7),
                               1,
                               0)
            self.modifRCSig = SigTo(self.modifRC,0.2)
            self.modifMult = LFO(random.uniform(0.25,1)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = RCOsc(freq, self.modifRCSig, self.modifMult*self.mulInter)

        elif self.randChooser == 8:
            self.modifSineLoop = LFO(random.uniform(0.25,1)*(self.mod+0.001),
                                     random.uniform(0.2,0.8),
                                     random.randint(0,7),
                                     random.uniform(0.01,.45),
                                     0)
            self.modifSineLoopSig = SigTo(self.modifSineLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,1.5)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = SineLoop(freq,self.modifSineLoopSig, self.modifMult*self.mulInter)

        elif self.randChooser == 9:
            self.modifCFMRatio = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                     random.uniform(0.2,0.8),
                                     random.randint(0,7),
                                     random.uniform(0.1,1),
                                     0)
            self.modifCFMRatioSig = SigTo(self.modifCFMRatio,0.2)
            self.modifCFMIndex1 = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                      random.uniform(0.2,0.8),
                                      random.randint(0,7),
                                      random.uniform(1,10),
                                      0)
            self.modifCFMIndex1Sig = SigTo(self.modifCFMIndex1,0.2)
            self.modifCFMIndex2 = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                      random.uniform(0.2,0.8),
                                      random.randint(0,7),
                                      random.uniform(1,10),
                                      0)
            self.modifCFMIndex2Sig = SigTo(self.modifCFMIndex2,0.2)
            self.modifMult = LFO(random.uniform(0.25,1.5)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = CrossFM(freq, 
                               self.modifCFMRatioSig,
                               self.modifCFMIndex1Sig,
                               self.modifCFMIndex2Sig, self.modifMult*self.mulInter)

        elif self.randChooser == 10:
            self.modifFMRatio = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                    random.uniform(0.2,0.8),
                                    random.randint(0,7),
                                    random.uniform(0.1,1),
                                    0)
            self.modifFMRatioSig = SigTo(self.modifFMRatio,0.2)
            self.modifFMIndex = LFO(random.uniform(0.01,0.2)*(self.mod+0.001),
                                    random.uniform(0.2,0.8),
                                    random.randint(0,7),
                                    random.uniform(1,10),
                                    0)
            self.modifFMIndexSig = SigTo(self.modifFMIndex,0.2)
            self.modifMult = LFO(random.uniform(0.25,1.5)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .8,
                                 .2)
            self.sig = FM(freq, 
                          self.modifFMRatioSig,
                          self.modifFMIndexSig, self.modifMult*self.mulInter)

        elif self.randChooser == 11:
            self.tableList = [(0.,0)]+ \
                             [(random.randint(1,8190), \
                             random.uniform(-1,1)) for i in \
                             range(int(random.triangular(5,100,10)))]+ \
                             [(8191,0)]
            self.tableList.sort()
            self.table = LogTable(self.tableList)
            self.modifOscLoop = LFO(random.uniform(0.25,1)*(self.mod+0.001),
                                    random.uniform(0.2,0.8),
                                    random.randint(0,7),
                                    random.uniform(0.01,.05),
                                    0)
            self.modifOscLoopSig = SigTo(self.modifOscLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,1)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .6,
                                 .2)
            self.sig = OscLoop(self.table, 
                               self.freq, 
                               self.modifOscLoopSig, self.modifMult*self.mulInter)

        elif self.randChooser == 12:
            self.tableList = [1.]+ \
                             [random.triangular(0.,.8) for \
                             i in range(random.randint(2,8))]
            self.table = HarmTable(self.tableList)
            self.modifOscLoop = LFO(random.uniform(0.25,1)*(self.mod+0.001),
                                    random.uniform(0.2,0.8),
                                    random.randint(0,7),
                                    random.uniform(0.01,.05),
                                    0)
            self.modifOscLoopSig = SigTo(self.modifOscLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,1.5)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .6,
                                 .2)
            self.sig = OscLoop(self.table, 
                               self.freq, 
                               self.modifOscLoopSig, self.modifMult*self.mulInter)

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
            self.modifOscLoop = LFO(random.uniform(0.25,1)*(self.mod+0.001),
                                    random.uniform(0.2,0.8),
                                    random.randint(0,7),
                                    random.uniform(0.01,.05),
                                    0)
            self.modifOscLoopSig = SigTo(self.modifOscLoop,0.2)
            self.modifMult = LFO(random.uniform(0.25,1.5)*(self.multMod+0.001),
                                 random.uniform(0.2,0.8),
                                 random.randint(0,7),
                                 .6,
                                 .2)
            self.sig = OscLoop(self.table, 
                               self.freq, 
                               self.modifOscLoopSig, self.modifMult*self.mulInter)

        self.sigForPan = Clip(self.sig)
        self.forPan = Sine(random.uniform(0.1,1), phase = random.random())
        if side == "left":
            self.forPan.mul = 0.4
            self.forPan.add = 0
        elif side == "mid":
            self.forPan.mul = 0.5
            self.forPan.add = 0.5
        elif side == "right":
            self.forPan.mul = 0.4
            self.forPan.add = 0.6            
        self.sigPanned = Pan(self.sigForPan,outs=cons.NUMOUTS, pan=self.forPan)
        self.sigForOut = self.sigPanned.mix(cons.NUMOUTS)

        Sig.__init__(self, self.sigForOut, mul=mul, add=add)

    def repeatJit(self, walk = 1):
        '''
        Generates a new envelope from a walk from the previous one and trigs it.

        '''
        if vari.randEnvSynth < 50:
            pass
        else:
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

    def setNewFreq(self,newFreq):
        freq = newFreq
        if self.randChooser > 8 and self.randChooser <= 10:
            self.sig.setCarrier(SigTo(freq,random.uniform(0.01,0.05),self.freq0))
        else:
            self.sig.setFreq(SigTo(freq,random.uniform(0.01,0.05),self.freq0))
        self.freq0 = freq



# to be played when the text is spoken
class SineGen(Sig):
    def __init__(self, mul=1,add=0):
        self.a = Sine(4000, mul=0.05)
        self.b = Pan(self.a, pan = 0.5, mul=0)
        self.c1 = Delay(self.b, random.uniform(0.1,0.3), random.uniform(0.2,0.6))
        self.c2 = sum([self.b + self.c1])
        self.d = WGVerb(self.c2,0.8,20000,bal=0.7)
        # self.d = Freeverb(self.c2, 0.8, bal=0.7)
        self.patFreq = Pattern(self.newFreq, vari.sineTempo).play()
        self.patMul = Pattern(self.settings,0.05).play()
        Sig.__init__(self, self.d, mul=mul, add=add)
    def newFreq(self):
        self.a.freq = random.randint(3000,16000)
        self.b.pan = random.random()

    def settings(self):
        self.b.mul = vari.sineGenMul
        self.patFreq.time = vari.sineTempo
        self.d.feedback = vari.sineRevMul

# s.gui(locals())










