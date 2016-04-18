# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.

### When adding new effects, update FxMixer's sections accordingly

import constants as cons
import variables as vari
# import Engine as engi
from pyo import *
import random




class Distor(Sig):
    def __init__(self, inp, intense=1,  mul = 1, add = 0):
        self.inp = inp
        coin = random.randint(0,1)
        if coin == 0:
            self.lfoFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,10*intense)
        self.driv = LFO(self.lfoFreq, type=random.randint(0,6), mul=0.4, add=0.4)
        self.sig1 = Disto(self.inp, self.driv*intense, random.random(), mul=0.75)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self



class Harmon(Sig):
    def __init__(self, inp, intense=1,  mix = 0.5, mul = 1, add = 0):
        self.inp = inp
        self.mix = mix
        tranList = [0,7,12,-5,-12,-24]
        randRange = cons.NUMOUTS+random.randint(3,6)
        coin1 = random.randint(0,1)
        if coin1 == 0:
            self.tran = [random.choice(tranList) for i in range(randRange)]
        else:
            self.tran = random.choice(tranList)
        coin2 = random.randint(0,1)
        if coin2 == 0:
            self.lfoFreq = [random.uniform(0.1,7*intense) for i in range(randRange)]
        else:
            self.lfoFreq = random.uniform(0.1,7*intense)
        vibInt = random.random()
        self.vibHarm = LFO(self.lfoFreq, type=random.randint(0,6), mul=1*vibInt)
        self.sigTran = Harmonizer(self.inp,self.tran+self.vibHarm, mul=0.9 * self.mix)
        self.intDry = rescale(self.mix,0,1,1,0)
        self.sig1 = [self.inp[i] * self.intDry for i in range(len(self.inp))] + self.sigTran * intense
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sigTran.setInput(self.inp2)
        return self


class Filter(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        coin1 = random.randint(0,100)
        if coin1 <=35:
            self.fType = 0
            self.lfoAddMin = 120
            self.lfoAddMax = 3000
            self.lfoAddN = 800
        elif coin1 >35 and coin1 <= 65:
            self.fType = 1
            self.lfoAddMin = 50
            self.lfoAddMax = 10000
            self.lfoAddN = 2500
        elif coin1 >65 and coin1 <= 85:
            self.fType = 2
            self.lfoAddMin = 50
            self.lfoAddMax = 4000
            self.lfoAddN = 2000
        else:
            self.fType = 3
            self.lfoAddMin = 50
            self.lfoAddMax = 4000
            self.lfoAddN = 2000
        coin2 = random.randint(0,1)
        if coin2 == 0:
            self.lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,5*intense)
        lfoAdd = random.triangular(self.lfoAddMin,self.lfoAddMax,self.lfoAddN)
        lfoMul = random.uniform(10,lfoAdd/1.5)
        self.freqFilt = LFO(self.lfoFreq, type=random.randint(0,6), mul=lfoMul,add=lfoAdd)
        q = random.triangular(0.5,4,2)
        self.sig1 = Biquad(self.inp, self.freqFilt, q, self.fType)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self


class Chorused(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        coin1 = random.randint(0,1)
        if len(self.inp) > 1 or coin1 == 0:
            self.lfoDepFreq = [random.uniform(0.1,7*intense) for i in range(cons.NUMOUTS)]
        else: 
            self.lfoDepFreq = random.uniform(0.1,7*intense)
        self.depChor = LFO(self.lfoDepFreq, type=random.randint(0,6), mul=2.4, add=2.5)
        dep2 = self.depChor*random.random()
        feed = random.triangular(0,0.7,0.03)
        coin2 = random.randint(0,1)
        if len(self.inp) > 1 or coin2 == 0:
            self.lfoBalFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else: 
            self.lfoBalFreq = random.uniform(0.1,10*intense)
        self.balChor = LFO(self.lfoDepFreq, type=random.randint(0,6), mul=.5, add=.5)
        bal = self.balChor*random.random()
        self.sig1 = Chorus(self.inp, dep2*intense, feed*intense, bal)
        Sig.__init__(self, self.sig1,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self


class Panning(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        coin = random.randint(0,1)
        freq = random.uniform(0.1,2*intense)
        if coin == 0 or len(self.inp) == 2:
            self.lfoMul = .5*random.random()
            self.panPan1 = LFO(freq, type=random.randint(0,6), mul=self.lfoMul, add=.5) 
            self.panPan2 = SigTo(self.panPan1,0.1)
        elif coin == 1:
            self.panPan1 = Phasor(freq)
            self.panPan2 = SigTo(self.panPan1,0.1)
        if len(self.inp) == 2:
            spread = 0
            self.sig1 = Pan(self.inp, cons.NUMOUTS, self.panPan2, spread)
        else:
            spread = random.uniform(0.,0.7)
            self.sig1 = Pan(self.inp, cons.NUMOUTS, self.panPan2, spread)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)   
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self

class Delayer(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        self.intense = intense
        coin1 = random.randint(0,1)
        if coin1 == 0:
            coin2 = random.randint(0,1)
            if len(self.inp) > 1 or coin2 == 0:
                self.lfoDelFreq = [random.uniform(0.01,0.5*intense) for i in range(cons.NUMOUTS)]
            else: 
                self.lfoDelFreq = random.uniform(0.01,0.5*intense)
            delLfo = LFO(self.lfoDelFreq, type=random.randint(0,6)).range(0.01,0.2)
            self.delay = delLfo*random.triangular(0,0.5,0.01) 
        else:
            self.delay = random.uniform(0.005,0.5)
        self.feed = random.triangular(0.1,0.6,0.3)
        self.sig1 = Delay(self.inp, self.delay*intense, self.feed*intense, mul=0.7)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        self.sig3 = self.sig2 + self.inp
        Sig.__init__(self, self.sig3,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self
    def setTimeFb(self):
        coin = random.randint(0,1)
        if coin == 0:
            coin2 = random.randint(0,1)
            if len(self.inp) > 1 or coin2 == 0:
                self.lfoDelFreq = [random.uniform(0.01,0.5*self.intense) for i in range(cons.NUMOUTS)]
            else: 
                self.lfoDelFreq = random.uniform(0.01,0.5*self.intense)
            delLfo = LFO(self.lfoDelFreq, type=random.randint(0,6)).range(0.01,0.2)
            self.sig1.delay = delLfo*random.triangular(0,0.5,0.01) 
        else:
            self.sig1.delay = random.uniform(0.005,0.5)
        self.sig1.feedback = random.triangular(0.1,0.6,0.3)
        return self


class Phasered(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        coin2 = random.randint(0,1)
        if coin2 == 0:
            self.lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,5*intense)
        lfoFreqAdd = random.triangular(50,3000,400)
        lfoFreqMul = random.uniform(10,lfoFreqAdd/1.5)
        self.freqPhas = LFO(self.lfoFreq, type=random.randint(0,6), mul=lfoFreqMul,add=lfoFreqAdd)
        lfoSpAdd = random.uniform(.8,1.4)
        lfoSpMul = random.uniform(.4,1.2)
        coin3 = random.randint(0,1)
        if coin3 == 0:
            self.lfoSpread = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoSpread = random.uniform(0.1,5*intense)
        spread = LFO(self.lfoSpread, type=random.randint(0,6), mul=lfoSpMul,add=lfoSpAdd)
        q = random.uniform(1,20)
        feed = random.uniform(0.1,0.8)
        num = int(random.randint(1,20)*intense)+1
        self.sig1 = Phaser(self.inp, self.freqPhas, spread, q, feed, num, mul=0.7)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self


class FxMixer(Sig):
    def __init__(self, inPut, numFXs=3, modu=1, mul=1, add=0):

        self.inPut = inPut
        self.modu = modu
        self.numFXs = numFXs

        ##To prevent out of range assignation
        if self.modu > 1:
            print 'WARNING: Max modu amount is 1.  modu set to 1.'
            self.modu = 1
        elif self.modu <= 0:
            print 'WARNING: Min modu amount is 0.  modu set to 0.'
            self.modu = 0
        if self.numFXs > 7:
            print 'WARNING: Max numFXs amount is 7.  numFXs set to 7.'
            self.numFXs = 7
        elif self.numFXs <= 0:
            print 'WARNING: Min numFXs amount is 1.  numFXs set to 1.'
            self.numFXs = 1

        # select which FXs are applied
        self.fxSel()

        # instantiate Mixer
        self.mixer1 = Mixer(8, 2)

        # instantiate the Fxs
        self.fx1 = Distor(self.mixer1[0], self.modu)
        self.fx2 = Harmon(self.mixer1[1], self.modu)
        self.fx3 = Filter(self.mixer1[2], self.modu)
        self.fx4 = Chorused(self.mixer1[3], self.modu)
        self.fx5 = Panning(self.mixer1[4], self.modu)
        self.fx6 = Delayer(self.mixer1[5], self.modu)
        self.fx7 = Phasered(self.mixer1[6], self.modu)

        # assign the Fxs to Mixer inputs
        self.mixer1.addInput(0,self.inPut)
        self.mixer1.addInput(1,self.fx1)
        self.mixer1.addInput(2,self.fx2)
        self.mixer1.addInput(3,self.fx3)
        self.mixer1.addInput(4,self.fx4)
        self.mixer1.addInput(5,self.fx5)
        self.mixer1.addInput(6,self.fx6)
        self.mixer1.addInput(7,self.fx7)

        # applies proper internal mixer routing
        self.routing()

        # last output is picked up here to send sig out of this object
        Sig.__init__(self, self.mixer1[len(self.mixer1.getKeys())-1],mul,add)

    def fxSel(self):
        # FX selection - TO BE MODIFIED IF MORE FXs ARE ADDED

        origFXs = []
        origFXs = random.sample([0,1,2,3,4,5,6],self.numFXs)

        # FX order sorting
        # Disto always 1st, then harmon, filter or phaser, 
        #     then chorus or panning, then delay.
        tempFXs = []
        TEMPLATE = [[0],[1,2,6],[3,4],[5]]
        for i in range(len(TEMPLATE)):
            sub = []
            sub = [val for val in origFXs if val in TEMPLATE[i]]
            tempFXs.append(sub)

        for sub in tempFXs:
            random.shuffle(sub)

        # list to store the selected effects, in correct order
        self.newFXs = []
        for sub in tempFXs:
            self.newFXs += sub
        return self

    def routing(self, target = 1):
        # assigns Mixer internal routing depending on the Fxs selected
        for i in range(self.numFXs):
            if i == 0:
                self.mixer1.setAmp(0,self.newFXs[i]-1,target)
            elif i == len(self.newFXs)-1:
                # assign the last effect to exit
                self.mixer1.setAmp(self.newFXs[i-1],len(self.mixer1.getKeys())-1,target)
            else:
                self.mixer1.setAmp(self.newFXs[i-1],self.newFXs[i]-1,target)
        return self

    def chMix(self):
        # assigns new effects
        self.routing(target = 0.)
        self.fxSel()
        self.routing(target = 1.)
        return self
        



###################################################### PROB DEPRECATED  -  START
# class Sfxs:
#     """
#     This is where the audio signal from the gens is picked up and processed for output.
#     If mode = 0, the effects are randomly applied.
#     If mode = 1, the effects can be chosen manually. (TODO)
#     modu is the amount of effect applied.  Min is 0, max is 1.
#     numFXs is the number of effects applied.  Min is 1, max is 7.
#     rvb = 1 applies a reverb at the very end of the chain.
#     """

#     def __init__(self,inSig, mode=0, numOuts = cons.NUMOUTS, modu=1, numFXs=2, mult = 1, rvb = 0):
#         self.sig = inSig
#         self.mult = mult*0.6
#         self.numFXs = numFXs
#         self.amp = None
#         self.rvb = rvb
#         self.fxSig = []  # to add the fx signals for output
#         self.outFilt = None

#         # to store settings, for realtime modifications
#         self.fxDict = {'disto':{},
#                        'harmon':{},
#                        'filter':{},
#                        'chorus':{},
#                        'panning':{},
#                        'phaser':{}}

#         ###To prevent out of range assignation
#         if modu > 1:
#             print 'WARNING: Max modu amount is 1.  modu set to 1.'
#             modu = 1
#         elif modu <= 0:
#             print 'WARNING: Min modu amount is 0.  modu set to 0.'
#             modu = 0
#         if numFXs > 7:
#             print 'WARNING: Max numFXs amount is 7.  numFXs set to 7.'
#             numFXs = 7
#         elif numFXs <= 0:
#             print 'WARNING: Min numFXs amount is 1.  numFXs set to 1.'
#             numFXs = 1

#         ###FX selection
#         origFXs = []
#         origFXs = [0,1,2,3,4,5,6]#random.sample([0,1,2,3,4,5,6],numFXs)    #### TESTING 

#         ###FX order sorting
#         ### Disto always 1st, then harmon, filter or phaser, 
#         ###     then chorus or panning, then delay.
#         tempFXs = []
#         TEMPLATE = [[0],[1,2,6],[3,4],[5]]
#         for i in range(len(TEMPLATE)):
#             sub = []
#             sub = [val for val in origFXs if val in TEMPLATE[i]]
#             tempFXs.append(sub)

#         for sub in tempFXs:
#             random.shuffle(sub)

#         # list to store the selected effects, in correct order
#         self.newFXs = []
#         for sub in tempFXs:
#             self.newFXs += sub
#         print self.newFXs

#         # envelope for main volume profile
#         inRamp = random.randint(1000,3000)
#         outRamp = 8191 - random.randint(1000,3000)
#         self.mainEnv = CosTable([(0,0), (inRamp,1), (outRamp,1), (8191,0)])
#         self.mainEnvDur = random.uniform(0.05,0.02)
#         self.mainEnvGo = TableRead(table=self.mainEnv, freq=self.mainEnvDur).play()


#         for i in range(numFXs):
#             if self.newFXs[i] == 0:
#                 print "disto on"
#                 self.fxSig.append(self.distor(modu))
#             if self.newFXs[i] == 1:
#                 print "harmon on"
#                 self.fxSig.append(self.harmon(modu))
#             if self.newFXs[i] == 2:
#                 print "filter on"
#                 self.fxSig.append(self.filter(modu))
#             if self.newFXs[i] == 3:
#                 print "chorus on"
#                 self.fxSig.append(self.chorus(modu))
#             if self.newFXs[i] == 4:
#                 print "panning on"
#                 self.fxSig.append(self.panning(modu))
#             if self.newFXs[i] == 5:
#                 print "delay on"
#                 self.fxSig.append(self.delay(modu))
#             if self.newFXs[i] == 6:
#                 print "phaser on"
#                 self.fxSig.append(self.phaser(modu))
#         print "dict",self.fxDict
#         self.out()

#         # to update the values according to the input (MIDI CC for now)
#         self.patSettings = Pattern(self.settings,0.05).play()


#     def distor(self, intense=1, mult = 1):
#         coin = random.randint(0,1)
#         if coin == 0:
#             lfoFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
#         else:
#             lfoFreq = random.uniform(0.1,10*intense)
#         self.fxDict['disto']['lfoFreq'] = lfoFreq
#         self.driv = LFO(lfoFreq, type=random.randint(0,6), mul=0.4, add=0.4)
#         self.sig2 = Disto(self.sig, self.driv*intense, random.random(), mul=0.75*mult)
#         self.sig = self.sig2.mix(cons.NUMOUTS)
#         return self.sig


#     def harmon(self, intense=1, mult = 1):
#         tranList = [0,7,12,-5,-12,-24]
#         randRange = cons.NUMOUTS+random.randint(0,6)
#         coin1 = random.randint(0,1)
#         if coin1 == 0:
#             tran = [random.choice(tranList) for i in range(randRange)]
#         else:
#             tran = random.choice(tranList)
#         coin2 = random.randint(0,1)
#         if coin2 == 0:
#             lfoFreq = [random.uniform(0.1,7*intense) for i in range(randRange)]
#         else:
#             lfoFreq = random.uniform(0.1,7*intense)
#         self.fxDict['harmon']['lfoFreq'] = lfoFreq
#         vibInt = random.random()
#         self.vibHarm = LFO(lfoFreq, type=random.randint(0,6), mul=1*vibInt)
#         self.sigTran = Harmonizer(self.sig,tran+self.vibHarm, mul=0.9*mult)
#         intenseDry = random.triangular(0,.9,0.5)
#         self.sig2 = [self.sig[i] * intenseDry for i in range(len(self.sig))] + self.sigTran * intense
#         self.sig = self.sig2.mix(cons.NUMOUTS)
#         return self.sig

#     def filter(self, intense=1, mult = 1):
#         coin1 = random.randint(0,100)
#         if coin1 <=35:
#             fType = 0
#             lfoAddMin = 120
#             lfoAddMax = 3000
#             lfoAddN = 800
#         elif coin1 >35 and coin1 <= 65:
#             fType = 1
#             lfoAddMin = 50
#             lfoAddMax = 10000
#             lfoAddN = 2500
#         elif coin1 >65 and coin1 <= 85:
#             fType = 2
#             lfoAddMin = 50
#             lfoAddMax = 4000
#             lfoAddN = 2000
#         else:
#             fType = 3
#             lfoAddMin = 50
#             lfoAddMax = 4000
#             lfoAddN = 2000
#         coin2 = random.randint(0,1)
#         if coin2 == 0:
#             lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
#         else:
#             lfoFreq = random.uniform(0.1,5*intense)
#         self.fxDict['filter']['lfoFreq'] = lfoFreq
#         lfoAdd = random.triangular(lfoAddMin,lfoAddMax,lfoAddN)
#         lfoMul = random.uniform(10,lfoAdd/1.5)
#         self.freqFilt = LFO(lfoFreq, type=random.randint(0,6), mul=lfoMul,add=lfoAdd)
#         q = random.triangular(0.5,4,2)
#         self.sig2 = Biquad(self.sig, self.freqFilt, q, fType, mul = mult)
#         self.sig = self.sig2.mix(cons.NUMOUTS)
#         return self.sig

#     def chorus(self, intense=1, mult = 1):
#         coin1 = random.randint(0,1)
#         if len(self.sig) > 1 or coin1 == 0:
#             lfoDepFreq = [random.uniform(0.1,7*intense) for i in range(cons.NUMOUTS)]
#         else: 
#             lfoDepFreq = random.uniform(0.1,7*intense)
#         self.fxDict['chorus']['lfoDepFreq'] = lfoDepFreq
#         self.depChor = LFO(lfoDepFreq, type=random.randint(0,6), mul=2.4, add=2.5)
#         dep2 = self.depChor*random.random()
#         feed = random.triangular(0,0.7,0.03)
#         coin2 = random.randint(0,1)
#         if len(self.sig) > 1 or coin2 == 0:
#             lfoBalFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
#         else: 
#             lfoBalFreq = random.uniform(0.1,10*intense)
#         self.fxDict['chorus']['lfoBalFreq'] = lfoBalFreq
#         self.balChor = LFO(lfoDepFreq, type=random.randint(0,6), mul=.5, add=.5)
#         bal = self.balChor*random.random()
#         self.sig = Chorus(self.sig, dep2*intense, feed*intense, bal, mul=mult)
#         return self.sig

#     def panning(self, intense=1, mult = 1):
#         coin = random.randint(0,1)
#         freq = random.uniform(0.1,2*intense)
#         self.fxDict['panning']['lfoFreq'] = freq

#         if coin == 0 or len(self.sig) == 2:
#             lfoMul = .5*random.random()
#             self.panPan = LFO(freq, type=random.randint(0,6), mul=lfoMul, add=.5) 
#         elif coin == 1:
#             self.panPan = Phasor(freq)
#         if len(self.sig) == 2:
#             spread = 0
#             self.sig2 = Pan(self.sig, cons.NUMOUTS, self.panPan, spread) #, mul=amp)
#         else:
#             spread = random.uniform(0.,0.7)
#             self.sig2 = Pan(self.sig, cons.NUMOUTS, self.panPan, spread)
#         self.sig = self.sig2.mix(cons.NUMOUTS)   
#         return self.sig

#     def delay(self, intense=1, mult = 1):
#         coin1 = random.randint(0,1)
#         if coin1 == 0:
#             coin2 = random.randint(0,1)
#             if len(self.sig) > 1 or coin2 == 0:
#                 lfoDelFreq = [random.uniform(0.01,0.5*intense) for i in range(cons.NUMOUTS)]
#             else: 
#                 lfoDelFreq = random.uniform(0.01,0.5*intense)
#             delLfo = LFO(lfoDelFreq, type=random.randint(0,6)).range(0.01,0.2)
#             delay = delLfo*random.triangular(0,0.5,0.01) 
#         else:
#             delay = random.uniform(0.005,0.5)
#         feed = random.triangular(0.1,0.6,0.3)
#         self.sig2 = Delay(self.sig, delay*intense, feed*intense, mul=0.7)
#         self.sig = self.sig2.mix(cons.NUMOUTS)
#         return self.sig

#     def phaser(self, intense=1, mult = 1):

#         coin2 = random.randint(0,1)
#         if coin2 == 0:
#             lfoFreq = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
#         else:
#             lfoFreq = random.uniform(0.1,5*intense)
#         self.fxDict['phaser']['lfoFreq'] = lfoFreq
#         lfoFreqAdd = random.triangular(50,3000,400)
#         lfoFreqMul = random.uniform(10,lfoFreqAdd/1.5)
#         self.freqPhas = LFO(lfoFreq, type=random.randint(0,6), mul=lfoFreqMul,add=lfoFreqAdd)
#         lfoSpAdd = random.uniform(.8,1.4)
#         lfoSpMul = random.uniform(.4,1.2)
#         coin3 = random.randint(0,1)
#         if coin3 == 0:
#             lfoSpread = [random.uniform(0.1,5*intense) for i in range(cons.NUMOUTS)]
#         else:
#             lfoSpread = random.uniform(0.1,5*intense)
#         spread = LFO(lfoSpread, type=random.randint(0,6), mul=lfoSpMul,add=lfoSpAdd)
#         q = random.uniform(1,20)
#         feed = random.uniform(0.1,0.8)
#         num = int(random.randint(1,20)*intense)+1
#         self.sig2 = Phaser(self.sig, self.freqPhas, spread, q, feed, num, mul=0.7*mult)
#         self.sig = self.sig2.mix(cons.NUMOUTS)
#         return self.sig


#     def out(self):
#         print "Number of output channels: ", len(self.sig)
#         print "Number of output channels FX: ", len(self.fxSig)
#         if len(self.fxSig)>2:
#             self.sigA = Mix(self.fxSig, cons.NUMOUTS)
#         else:
#             self.sigA = self.sig
#         self.outFilt = Biquad(self.sigA, type = 1, freq=0, q=6)
#         if self.rvb == 0:
#             self.sigB = Freeverb(self.outFilt,bal = 0)
#         else:
#             self.sigB = Freeverb(self.outFilt, random.choice([.02,.1,.3,.5,.8]))
#         self.sigC = Compress(self.sigB,-20,10,mul=self.mainEnvGo).out() # Where the main amp env is applied

#     def getDur(self, amp=1, tTime=1):
#         return (1/self.mainEnvDur)

#     def settings(self):
#         speedMod = 1/vari.mainTempo
#         # Filter applied depending on the fader value
#         self.outFilt.freq = SigTo(vari.outFiltFreq,0.5)
#         self.outFilt.freq = vari.outFiltFreq
#         if 0 in self.newFXs:
#             if isinstance(self.fxDict['disto']['lfoFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['disto']['lfoFreq']]
#                 self.driv.freq = l
#             else:
#                 self.driv.freq = self.fxDict['disto']['lfoFreq'] * speedMod 
#         if 1 in self.newFXs:
#             if isinstance(self.fxDict['harmon']['lfoFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['harmon']['lfoFreq']]
#                 self.vibHarm.freq = l
#             else:
#                 self.vibHarm.freq = self.fxDict['harmon']['lfoFreq'] * speedMod

#         if 2 in self.newFXs:
#             if isinstance(self.fxDict['filter']['lfoFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['filter']['lfoFreq']]
#                 self.freqFilt.freq = l
#             else:
#                 self.freqFilt.freq = self.fxDict['filter']['lfoFreq'] * speedMod
#         if 3 in self.newFXs:
#             if isinstance(self.fxDict['chorus']['lfoDepFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['chorus']['lfoDepFreq']]
#                 self.depChor.freq = l
#             else: 
#                 self.depChor.freq = self.fxDict['chorus']['lfoDepFreq'] * speedMod
#             if isinstance(self.fxDict['chorus']['lfoBalFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['chorus']['lfoBalFreq']]
#                 self.balChor.freq = l
#             else:
#                 self.balChor.freq = self.fxDict['chorus']['lfoBalFreq'] * speedMod
#         if 4 in self.newFXs:
#             if isinstance(self.fxDict['panning']['lfoFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['panning']['lfoFreq']]
#                 self.panPan.freq = l
#             else:
#                 self.panPan.freq = self.fxDict['panning']['lfoFreq'] * speedMod
#         if 6 in self.newFXs:
#             if isinstance(self.fxDict['phaser']['lfoFreq'],list):
#                 l = [x * speedMod for x in self.fxDict['phaser']['lfoFreq']]
#                 self.freqPhas.freq = l
#             else:
#                 self.freqPhas.freq = self.fxDict['phaser']['lfoFreq'] * speedMod
######################################################## PROB DEPRECATED  - END