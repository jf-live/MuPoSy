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
    rvb = 1 applies a reverb at the very end of the chain.
    """

    def __init__(self,inSig, mode=0, numOuts = cons.NUMOUTS, modu=1, numFXs=2, mult = 1, rvb = 0):
        self.sig = inSig
        self.mult = mult*0.6
        self.numFXs = numFXs
        self.amp = None
        self.rvb = rvb
        self.fxSig = []  # to add the fx signals for output
        self.peakVal = None
        self.clipMul = 1
        self.sigOut1 = None
        self.sigOut2 = None
        self.sigOut3 = None
        self.sigOut4 = None
        self.sigOut5 = None
        self.sigOut6 = None

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
        self.mainEnv = CosTable([(0,0), (10,0.01),(inRamp,1), (outRamp,1), (8191,0)])
        self.mainEnvDur = random.uniform(0.05,0.02)
        # print "DUR", self.mainEnvDur
        self.mainEnvGo = TableRead(table=self.mainEnv, freq=self.mainEnvDur).play()


        for i in range(numFXs):
            if i == 0:
                inputSig = self.sig
                outputSig = self.sigOut1
            elif i == 1:
                inputSig = self.sigOut1
                outputSig = self.sigOut2
            elif i == 2:
                inputSig = self.sigOut2
                outputSig = self.sigOut3
            elif i == 3:
                inputSig = self.sigOut3
                outputSig = self.sigOut4
            elif i == 4:
                inputSig = self.sigOut4
                outputSig = self.sigOut5
            elif i == 5:
                inputSig = self.sigOut5
                outputSig = self.sigOut6
            elif i == 6:
                inputSig = self.sigOut6
                outputSig = self.sigOut7

            if newFXs[i] == 0:
                print "disto on"
                print inputSig, outputSig
                self.fxSig.append(self.distor(inputSig, outputSig, modu))
            elif newFXs[i] == 1:
                print "harmon on"
                print inputSig, outputSig
                self.fxSig.append(self.harmon(inputSig, outputSig, modu))
            elif newFXs[i] == 2:
                print "filter on"
                print inputSig, outputSig
                self.fxSig.append(self.filter(inputSig, outputSig, modu))
            elif newFXs[i] == 3:
                print "chorus on"
                print inputSig, outputSig
                self.fxSig.append(self.chorus(inputSig, outputSig, modu))
            elif newFXs[i] == 4:
                print "panning on"
                print inputSig, outputSig
                self.fxSig.append(self.panning(inputSig, outputSig, modu))
            elif newFXs[i] == 5:
                print "delay on"
                print inputSig, outputSig
                self.fxSig.append(self.delay(inputSig, outputSig, modu))
            elif newFXs[i] == 6:
                print "phaser on"
                print inputSig, outputSig
                self.fxSig.append(self.phaser(inputSig, outputSig, modu))

        self.out()
        # self.pat = Pattern(self.getPeak,0.005)

    def distor(self, sig, outSig, intense=1, mult = 1):
        print outSig
        coin = random.randint(0,1)
        if coin == 0:
            lfoFreq = [random.uniform(0.1,8*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoFreq = random.uniform(0.1,8*intense)
        driv = LFO(lfoFreq, type=random.randint(0,6), mul=0.45, add=0.5)
        self.sigDis2 = Disto(sig, driv*intense*0.8, random.random(), mul=0.75*mult)
        # self.sig3 = Clip(self.sig2).mix(cons.NUMOUTS)
        self.sigDis3 = self.sigDis2.mix(cons.NUMOUTS)
        self.peak9 = PeakAmp(self.sigDis3)
        self.p9 = Print(self.peak9, message = "Disto")
        outSig = self.sigDis3
        print outSig
        # return self.sigDis3

    def harmon(self, sig, outSig, intense=1, mult = 1):
        tranList = [0,7,12,-5,-12,24,-24]
        randRange = cons.NUMOUTS+random.randint(0,6)
        # following if to avoid clipping if randRange == 1 (hopefully)
        if randRange == 1:
            amp = 0.93 ** randRange
        else:
            amp = 0.93 ** randRange + .1
        coin1 = random.randint(0,1)
        if coin1 == 0:
            tran = [random.choice(tranList) for i in range(randRange)]
        else:
            tran = random.choice(tranList)
        coin2 = random.randint(0,1)
        if coin2 == 0:
            lfoFreq = [random.uniform(0.1,8*intense)*amp for i in range(randRange)]
        else:
            lfoFreq = random.uniform(0.1,8*intense)*amp
        vibInt = random.uniform(0.1,10)
        vib = LFO(lfoFreq, type=random.randint(0,6), mul=1*vibInt)
        self.sigTran = Harmonizer(sig,tran+vib, mul=0.9*amp*mult)
        intenseDry = random.triangular(0,.9,0.5)
        self.sigHar2 = [self.sig[i] * intenseDry for i in range(len(self.sig))] + self.sigTran * intense
        # self.sigHar3 = Clip(self.sigHar2).mix(cons.NUMOUTS) * 0.1
        self.sigHar3 = self.sigHar2.mix(cons.NUMOUTS) * 0.1
        self.peak8 = PeakAmp(self.sigHar3)
        self.p8 = Print(self.peak8, message = "Harmon")
        outSig = self.sigHar3
        # return self.sigHar3

    def filter(self, sig, outSig, intense=1, mult = 1):
        print outSig
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
        q = random.triangular(0.5,2.5,2)
        self.sigFil2 = Biquad(sig, freq, q, fType, mul = mult)
        self.sigFil3 = self.sigFil2.mix(cons.NUMOUTS) * 0.7
        self.peak7 = PeakAmp(self.sigFil3)
        self.p7 = Print(self.peak7, message = "Filter")
        # self.sig3 = Clip(self.sig2).mix(cons.NUMOUTS) * 0.7
        outSig = self.sigFil3
        # return self.sigFil3

    def chorus(self, sig, outSig, intense=1, mult = 1):
        coin1 = random.randint(0,1)
        if len(self.sig) > 1 or coin1 == 0:
            lfoDepFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else: 
            lfoDepFreq = random.uniform(0.1,10*intense)
        dep = LFO(lfoDepFreq, type=random.randint(0,6)).range(0.01,4.99)
        dep2 = dep*random.random()
        feed = random.triangular(0,0.7,0.03)
        coin2 = random.randint(0,1)
        if len(self.sig) > 1 or coin2 == 0:
            lfoBalFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else: 
            lfoBalFreq = random.uniform(0.1,10*intense)
        bal = LFO(lfoDepFreq, type=random.randint(0,6)).range(0.01,.99)
        bal2 = bal*random.random()
        self.sigCho2 = Chorus(sig, dep2*intense, feed*intense, bal2, mul=mult)
        # self.sig3 = Clip(self.sig2)
        self.sigCho3 = self.sigCho2
        self.peak6 = PeakAmp(self.sigCho3)
        self.p6 = Print(self.peak6, message = "Chorus")
        outSig = self.sigCho3
        # return self.sigCho3

    def panning(self, sig, outSig, intense=1, mult = 1):
        coin = random.randint(0,1)
        freq = random.uniform(0.1,2*intense)
        if coin == 0 or len(self.sig) == 2:
            lfoMul = .5*random.random()
            pan = LFO(freq, type=random.randint(0,6), mul=lfoMul, add=.5) 
        elif coin == 1:
            pan = Phasor(freq)
        if len(self.sig) == 2:
            spread = 0
            self.sigPan2 = Pan(sig, cons.NUMOUTS, pan, spread) #, mul=amp)
        else:
            spread = random.uniform(0.,0.7)
            self.sigPan2 = Pan(self.sig, cons.NUMOUTS, pan, spread)
        self.sigPan3 = self.sigPan2.mix(cons.NUMOUTS) * 0.8
        self.peak5 = PeakAmp(self.sigPan3)
        self.p5 = Print(self.peak5, message = "Panning")
        # self.sig3 = Clip(self.sig2).mix(cons.NUMOUTS) * 0.8
        outSig = self.sigPan3
        # return self.sigPan3

    def delay(self, sig, outSig, intense=1, mult = 1):
        coin1 = random.randint(0,1)
        if coin1 == 0:
            coin2 = random.randint(0,1)
            if len(self.sig) > 1 or coin2 == 0:
                lfoDelFreq = [random.uniform(0.01,0.5*intense) for i in range(cons.NUMOUTS)]
            else: 
                lfoDelFreq = random.uniform(0.01,0.5*intense)
            lfoMul = 3.*random.random()
            lfoAdd = 3.*random.random()
            delLfo = LFO(lfoDelFreq, type=random.randint(0,6), mul=lfoMul, add=lfoAdd)
            delay = delLfo*random.triangular(0,0.5,0.01) 
        else:
            delay = random.uniform(0.005,0.5)
        feed = random.triangular(0.1,0.5,0.3)
        self.sigDel2 = Delay(sig, delay*intense, feed*intense, mul=0.7)
        self.sigDel3 = self.sigDel2.mix(cons.NUMOUTS)
        self.peak4 = PeakAmp(self.sigDel3)
        self.p4 = Print(self.peak4, message = "Delay")
        # self.sig3 = Clip(self.sig2).mix(cons.NUMOUTS)
        # self.sig = Compress(self.sig,-20,2)
        outSig = self.sigDel3
        # return self.sigDel3

    def phaser(self, sig, outSig, intense=1, mult = 1):

        coin2 = random.randint(0,1)
        if coin2 == 0:
            lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoFreq = random.uniform(0.1,5*intense)
        # lfoFreqAdd = random.triangular(50,3000,400)
        # lfoFreqMul = random.uniform(10,lfoFreqAdd/1.5)
        freq = LFO(lfoFreq, type=random.randint(0,6)).range(50,2000)
        # freq = LFO(lfoFreq, type=random.randint(0,6), mul=lfoFreqMul,add=lfoFreqAdd)
        lfoSpAdd = random.uniform(.8,1.4)
        lfoSpMul = random.uniform(.4,1.2)
        coin3 = random.randint(0,1)
        if coin3 == 0:
            lfoSpread = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            lfoSpread = random.uniform(0.1,5*intense)
        spread = LFO(lfoSpread, type=random.randint(0,6), mul=lfoSpMul,add=lfoSpAdd)
        q = random.uniform(1,20)
        feed = random.uniform(0.1,0.8)
        num = int(random.randint(1,20)*intense)+1

        self.sigPha2 = Phaser(sig, freq, spread, q, feed, num, mul=0.7*mult)
        self.sigPha3 = self.sigPha2.mix(cons.NUMOUTS)
        self.peak3 = PeakAmp(self.sigPha3)
        self.p3 = Print(self.peak3, message = "Phaser")
        # self.sig3 = Clip(self.sig2).mix(cons.NUMOUTS)
        outSig = self.sigPha3
        # return self.sigPha3

    def reverb(self, sig, outSig, intense=1, mult = 1):
        size = random.uniform(0.1,0.9)
        coin = random.randint(0,1)
        if coin == 0:
            size = [size+random.uniform(-0.05,0.05) for i in range(cons.NUMOUTS)]
        damp = random.random()
        bal = random.triangular(0.1,1,0.3)*intense
        self.sigRev2 = Freeverb(sig, size, damp, bal, mul = mult)
        self.sigRev3 = self.sigRev2.mix(cons.NUMOUTS)
        return self.sigRev3

    def out(self):
        print "Number of output channels: ", len(self.sig)

        numFxsOut = len(self.fxSig)

        if numFxsOut == 1:
            self.sigA = fxSig[0]
        elif numFxsOut == 2:
            self.sigOut1 = fxSig[0]
            self.sigA = fxSig[1]
        elif numFxsOut == 3:
            self.sigOut1 = fxSig[0]
            self.sigOut2 = fxSig[1]
            self.sigA = fxSig[2]
        elif numFxsOut == 4:
            self.sigOut1 = fxSig[0]
            self.sigOut2 = fxSig[1]
            self.sigOut2 = fxSig[2]
            self.sigA = fxSig[3]
        elif numFxsOut == 5:
            self.sigOut1 = fxSig[0]
            self.sigOut2 = fxSig[1]
            self.sigOut2 = fxSig[2]
            self.sigOut2 = fxSig[3]
            self.sigA = fxSig[4]

        # self.sigA = Mix(self.fxSig, cons.NUMOUTS)
        self.peak1 = PeakAmp(self.sigA)
        self.p1 = Print(self.peak1, message = "sigA")
        if self.rvb == 0:
            self.sigB = Freeverb(self.sigA,bal = 0)
        else:
            self.sigB = Freeverb(self.sigA, vari.fxRvbInit)
        self.sigC = Compress(self.sigB,-20,10,mul=1)#self.mainEnvGo) # Where the main amp env is applied
        self.peak2 = PeakAmp(self.sigC)
        self.p2 = Print(self.peak2, message = "sigC")
        # self.peak = PeakAmp(self.sigC)
        # self.p = Print(self.peak)
        # self.pat = Pattern(self.getPeak,0.005)
        # self.attDet = AttackDetector(self.sigC, 10000,-300)
        # self.trig = TrigFunc(self.attDet, trigP)
        # if self.peak > 0.:
        #     self.outLevel = 0
        # else:
        #     self.outLevel = 1.
        # self.p = Print(self.peak)
        self.sigD = Clip(self.sigC, mul = self.clipMul).out()

    def getDur(self, amp=1, tTime=1):
        return (1/self.mainEnvDur)

    def getPeak(self):
        self.peakVal = self.peak.get
        print 'self.peak.get', self.peak.get
        if self.peak.get > 1.1:
            print "1.1"
            self.clipMul = SigTo(0.,0.005)
        else:
            self.clipMul = SigTo(1,0.005)

def trigP():
    print "WOOOOOOOOOOOOT ATTAAACCKKKKK"


# a = Noise(mul=0.6)
# a = Sine(mul=0.4)
# modul = random.random()
# print "modul", modul
# a = [Sine(random.randint(300,3000),mul=0.2) for i in range(2)]
# b = [Sfxs(a,modu=modul, numFXs=2) for i in range(1)]


# s.gui(locals())


