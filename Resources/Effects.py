# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.

import constants as cons
import variables as vari
import Engine as engi
from pyo import *
import random

# s = Server().boot()


class Sfxs:
    """
    This is where the audio signal from the gens is picked up and processed for output.
    If mode = 0, the effects are randomly applied.
    If mode = 1, the effects can be chosen manually. (TODO)
    modu is the amount of effect applied.  Min is 0, max is 1.
    numFXs is the number of effects applied.  Min is 1, max is 7.
    """

    def __init__(self,inSig, mode=0, numOuts = cons.NUMOUTS, modu=1, numFXs=2, mult = 1):
        self.sig = inSig
        self.mult = mult*0.6
        self.numFXs = numFXs
        self.amp = None

        ###To prevent out of range assignation
        if modu > 1:
            print 'WARNING: Max modu amount is 1.  modu set to 1.'
            modu = 1
        elif modu <= 0:
            print 'WARNING: Min modu amount is 0.  modu set to 0.'
            modu = 0
        if numFXs > 7:
            print 'WARNING: Max numFXs amount is 7.  numFXs set to 7.'
            numFXs = 7
        elif numFXs <= 0:
            print 'WARNING: Min numFXs amount is 1.  numFXs set to 1.'
            numFXs = 1

        ###FX selection
        origFXs = []
        origFXs = random.sample([0,1,2,3,4,5,6],numFXs)
        #----------------------------------------------------------START-OLD
        # for i in range(numFXs):
            # newChoice = random.choice([0,1,2,3,4,5,6])
            # while newChoice in origFXs:
            #   newChoice = random.choice([0,1,2,3,4,5,6])
            # origFXs.append(newChoice)
        #------------------------------------------------------------END-OLD

        ###FX order sorting
        ### Disto always 1st, then harmon, filter or phaser, 
        ###     then chorus or panning, then delay.
        tempFXs = []
        TEMPLATE = [[0],[1,2,6],[3,4],[5]]
        for i in range(len(TEMPLATE)):
            sub = []
            sub = [val for val in origFXs if val in TEMPLATE[i]]
            tempFXs.append(sub)

        for sub in tempFXs:
            random.shuffle(sub)

        newFXs = []
        for sub in tempFXs:
            newFXs += sub
        print newFXs

        #----------------------------------------------------------START-OLD
        # for i in range(numFXs):
        #   current = origFXs[i]
        #   if current == 0:
        #       newFXs.insert(0, current)
        #   elif current == 1 or current == 2 or current == 6:
        #       if len(newFXs) >= 1:
        #           if newFXs[0] is not 0:
        #               newFXs.insert(0, current)
        #           else:
        #               newFXs.insert(1, current)
        #       elif len(newFXs) == 0:
        #           newFXs.insert(0,current)
        #       else:
        #           newFXs.append(current)
        #   elif current == 3 or current == 4:
        #       if len(newFXs) >= 1:
        #           if newFXs[-1] is not 5:
        #               newFXs.insert(len(newFXs), current)
        #           else:
        #               newFXs.insert(len(newFXs)-1, current)
        #       elif len(newFXs) == 1:
        #           if newFXs[0] is 5:
        #               newFXs.append(current)
        #       else:
        #           newFXs.insert(len(newFXs)-2, current)
        #   elif current == 5:
        #       newFXs.append(current)
        #------------------------------------------------------------END-OLD

        # envelope for main volume profile
        inRamp = random.randint(1000,3000)
        outRamp = 8191 - random.randint(1000,3000)
        self.mainEnv = CosTable([(0,0), (inRamp,1), (outRamp,1), (8191,0)])
        self.mainEnvDur = random.uniform(0.05,0.02)
        self.mainEnvGo = TableRead(table=self.mainEnv, freq=self.mainEnvDur).play()


        for i in range(numFXs):
            if newFXs[i] == 0:
                print "disto on"
                self.distor(modu)
            if newFXs[i] == 1:
                print "harmon on"
                self.harmon(modu)
            if newFXs[i] == 2:
                print "filter on"
                self.filter(modu)
            if newFXs[i] == 3:
                print "chorus on"
                self.chorus(modu)
            if newFXs[i] == 4:
                print "panning on"
                self.panning(modu)
            if newFXs[i] == 5:
                print "delay on"
                self.delay(modu)
            if newFXs[i] == 6:
                print "phaser on"
                self.phaser(modu)
            ###Reverb maybe should not be used here 
            ###    as tail will be cut prob most of the time.
            # if newFXs[i] == 7:
            #   print "reverb on"
            #   self.reverb(modu)

        self.out()


    def distor(self, intense=1, mult = 1):
        coin = random.randint(0,1)
        if coin == 0:
            lfoFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoFreq = random.uniform(0.1,10*intense)
        driv = LFO(lfoFreq, type=random.randint(0,6), mul=0.5, add=0.5)
        self.sig = Disto(self.sig, driv*intense, random.random(), mul=0.75*mult)
        self.sig = self.sig.mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-12,5)
        return self.sig

    def harmon(self, intense=1, mult = 1):
        tranList = [0,7,12,-5,-12,24,-24]
        randRange = cons.NUMOUTS+random.randint(0,6)
        amp = 0.93 ** randRange + .1
        coin1 = random.randint(0,1)
        if coin1 == 0:
            tran = [random.choice(tranList) for i in range(randRange)]
        else:
            tran = random.choice(tranList)
        coin2 = random.randint(0,1)
        if coin2 == 0:
            lfoFreq = [random.uniform(0.1,10*intense)*amp for i in range(randRange)]
        else:
            lfoFreq = random.uniform(0.1,10*intense)*amp
        vibInt = random.random()
        vib = LFO(lfoFreq, type=random.randint(0,6), mul=1*vibInt)
        self.sigTran = Harmonizer(self.sig,tran+vib, mul=0.9*amp*mult)
        intenseDry = random.triangular(0,1,0.5)
        self.sig = [self.sig[i] * intenseDry for i in range(len(self.sig))] + self.sigTran * intense
        self.sig = self.sig.mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-12,5)
        return self.sig

    def filter(self, intense=1, mult = 1):
        coin1 = random.randint(0,100)
        if coin1 <=35:
            fType = 0
            lfoAddMin = 120
            lfoAddMax = 3000
            lfoAddN = 800
        elif coin1 >35 and coin1 <= 65:
            fType = 1
            lfoAddMin = 50
            lfoAddMax = 10000
            lfoAddN = 2500
        elif coin1 >65 and coin1 <= 85:
            fType = 2
            lfoAddMin = 50
            lfoAddMax = 4000
            lfoAddN = 2000
        else:
            fType = 3
            lfoAddMin = 50
            lfoAddMax = 4000
            lfoAddN = 2000
        coin2 = random.randint(0,1)
        if coin2 == 0:
            lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoFreq = random.uniform(0.1,5*intense)
        lfoAdd = random.triangular(lfoAddMin,lfoAddMax,lfoAddN)
        lfoMul = random.uniform(10,lfoAdd/1.5)
        freq = LFO(lfoFreq, type=random.randint(0,6), mul=lfoMul,add=lfoAdd)
        q = random.triangular(0.5,20,2)
        self.sig = Biquad(self.sig, freq, q, fType, mul = mult)
        self.sig = self.sig.mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-12,5)
        return self.sig

    def chorus(self, intense=1, mult = 1):
        coin1 = random.randint(0,1)
        if len(self.sig) > 1 or coin1 == 0:
            lfoDepFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else: 
            lfoDepFreq = random.uniform(0.1,10*intense)
        dep = LFO(lfoDepFreq, type=random.randint(0,6), mul=2.5, add=2.5)
        dep = dep*random.random()
        feed = random.triangular(0,1,0.03)
        coin2 = random.randint(0,1)
        if len(self.sig) > 1 or coin2 == 0:
            lfoBalFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else: 
            lfoBalFreq = random.uniform(0.1,10*intense)
        bal = LFO(lfoDepFreq, type=random.randint(0,6), mul=.5, add=.5)
        bal = bal*random.random()
        self.sig = Chorus(self.sig, dep*intense, feed*intense, bal, mul=mult)
        return self.sig

    def panning(self, intense=1, mult = 1):
        coin = random.randint(0,1)
        freq = random.uniform(0.1,2*intense)
        if coin == 0 or len(self.sig) == 2:
            lfoMul = .5*random.random()
            pan = LFO(freq, type=random.randint(0,6), mul=lfoMul, add=.5) 
        elif coin == 1:
            pan = Phasor(freq)
        # ampTable = ExpTable([(0,0.),(50,1.),(8141,1.),(8191,0.)], inverse=False)
        # amp = Osc(table=ampTable, freq=freq, mul=.8)
        if len(self.sig) == 2:
            spread = 0
            self.sig = Pan(self.sig, cons.NUMOUTS, pan, spread) #, mul=amp)
        else:
            spread = random.uniform(0.,0.7)
            self.sig = Pan(self.sig, cons.NUMOUTS, pan, spread)
        self.sig = self.sig.mix(cons.NUMOUTS)   
        return self.sig

    def delay(self, intense=1, mult = 1):
        coin1 = random.randint(0,1)
        if coin1 == 0:
            coin2 = random.randint(0,1)
            if len(self.sig) > 1 or coin2 == 0:
                lfoDelFreq = [random.uniform(0.01,0.5*intense) for i in range(cons.NUMOUTS)]
            else: 
                lfoDelFreq = random.uniform(0.01,0.5*intense)
            lfoMul = 10.*random.random()
            lfoAdd = 10.*random.random()
            delLfo = LFO(lfoDelFreq, type=random.randint(0,6), mul=lfoMul, add=lfoAdd)
            delay = delLfo*random.triangular(0,0.5,0.01) 
        else:
            delay = random.uniform(0.005,0.5)
        feed = random.triangular(0.1,0.6,0.3)
        self.sig = Delay(self.sig, delay*intense, feed*intense, mul=0.7)
        self.sig = self.sig.mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-20,2)
        return self.sig

    def phaser(self, intense=1, mult = 1):

        coin2 = random.randint(0,1)
        if coin2 == 0:
            lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoFreq = random.uniform(0.1,5*intense)
        lfoFreqAdd = random.triangular(50,3000,400)
        lfoFreqMul = random.uniform(10,lfoFreqAdd/1.5)
        freq = LFO(lfoFreq, type=random.randint(0,6), mul=lfoFreqMul,add=lfoFreqAdd)
        lfoSpAdd = random.uniform(.8,1.4)
        lfoSpMul = random.uniform(.4,1.2)
        coin3 = random.randint(0,1)
        if coin3 == 0:
            lfoSpread = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoSpread = random.uniform(0.1,5*intense)
        spread = LFO(lfoSpread, type=random.randint(0,6), mul=lfoSpMul,add=lfoSpAdd)
        q = random.uniform(1,40)
        feed = random.uniform(0.1,0.85)
        num = int(random.randint(1,30)*intense)+1

        self.sig = Phaser(self.sig, freq, spread, q, feed, num, mul=0.7*mult)
        self.sig = self.sig.mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-15,40)
        return self.sig

    def reverb(self, intense=1, mult = 1):
        size = random.uniform(0.1,0.9)
        coin = random.randint(0,1)
        if coin == 0:
            size = [size+random.uniform(-0.05,0.05) for i in range(cons.NUMOUTS)]
        damp = random.random()
        bal = random.triangular(0.1,1,0.3)*intense
        self.sig = Freeverb(self.sig, size, damp, bal, mul = mult)
        self.sig = self.sig.mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-20,2)
        return self.sig

    def out(self):
        print "Number of output channels: ", len(self.sig)
        self.sig = Mix(self.sig, cons.NUMOUTS)
        self.sigC = Compress(self.sig,-20,10,mul=self.mainEnvGo) # Where the main amp env is applied
        # self.sig = self.sigC*self.amp
        self.sigC.out()

    def getDur(self, amp=1, tTime=1):
        return (1/self.mainEnvDur)

# a = Noise(mul=0.6)
# a = Sine(mul=0.4)
# modul = random.random()
# print "modul", modul
# a = [Sine(random.randint(300,3000),mul=0.2) for i in range(2)]
# b = [Sfxs(a,modu=modul, numFXs=2) for i in range(1)]


# s.gui(locals())


