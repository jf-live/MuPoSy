# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.

### When adding new effects, update FxMixer's sections accordingly

### Attribute values should be managed more efficiently so as to avoid duplicate lines...
### Some lines from setNewValues methods are in comments as they were adding up
###     extra streams.

import constants as cons
import variables as vari
# import Engine as engi
from pyo import *
import random




class Distor(Sig):
    def __init__(self, inp, intense=1,  mul = 1, add = 0):
        self.inp = inp
        self.intense = intense
        coin = random.randint(0,1)
        if coin == 0:
            self.lfoFreq = [random.uniform(0.1,10*intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,10*intense)
        self.driv = LFO(self.lfoFreq, type=random.randint(0,6), mul=0.4, add=0.4)
        self.sig1 = Disto(self.inp, self.driv*self.intense, random.random(), mul=0.75)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self
    def setNewValues(self):
        coin = random.randint(0,1)
        if coin == 0:
            self.lfoFreq = [random.uniform(0.1,10*self.intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,10*self.intense)
        self.driv = LFO(self.lfoFreq, type=random.randint(0,6), mul=0.4, add=0.4)
        self.sig1.setDrive(self.driv*self.intense)
        self.sig1.setSlope(random.random())
        return self


class Harmon(Sig):
    def __init__(self, inp, intense=1,  mix = 0.5, mul = 1, add = 0):
        self.inp = inp
        self.mix = mix
        self.intense = intense
        self.tranList = [0,7,12,-5,-12,-24]
        self.randRange = cons.NUMOUTS+random.randint(3,6)
        coin1 = random.randint(0,1)
        if coin1 == 0:
            self.tran = [random.choice(self.tranList) for i in range(self.randRange)]
        else:
            self.tran = random.choice(self.tranList)
        coin2 = random.randint(0,1)
        if coin2 == 0:
            self.lfoFreq = [random.uniform(0.1,7*intense) for i in range(self.randRange)]
        else:
            self.lfoFreq = random.uniform(0.1,7*intense)
        vibInt = random.random()
        self.vibHarm = LFO(self.lfoFreq, type=random.randint(0,6), mul=vibInt)
        self.sigTran = Harmonizer(self.inp,self.tran+self.vibHarm, mul=0.9 * self.mix)
        self.intDry = rescale(self.mix,0,1,1,0)
        self.sig1 = [self.inp[i] * self.intDry for i in range(len(self.inp))] + self.sigTran * intense
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sigTran.setInput(self.inp2)
        return self
    def setNewValues(self):
        coin1 = random.randint(0,1)
        if coin1 == 0:
            self.tran = [random.choice(self.tranList) for i in range(self.randRange)]
        else:
            self.tran = random.choice(self.tranList)
        # coin2 = random.randint(0,1)
        # if coin2 == 0:
        #     self.lfoFreq = [random.uniform(0.1,7*self.intense) for i in range(self.randRange)]
        # else:
        #     self.lfoFreq = random.uniform(0.1,7*self.intense)
        vibInt = random.random()
        # self.vibHarm.setFreq(self.lfoFreq)
        self.vibHarm.setType(random.randint(0,6))
        self.vibHarm.setMul(vibInt)
        self.sigTran.setTranspo(self.tran)
        return self


class Filter(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        self.intense = intense
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
    def setNewValues(self):
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
            self.lfoFreq = [random.uniform(0.1,5*self.intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,5*self.intense)
        lfoAdd = random.triangular(self.lfoAddMin,self.lfoAddMax,self.lfoAddN)
        lfoMul = random.uniform(10,lfoAdd/1.5)
        self.freqFilt.setFreq(self.lfoFreq)
        self.freqFilt.setType(random.randint(0,6))
        self.freqFilt.setMul(lfoMul)
        self.freqFilt.setAdd(lfoAdd)
        self.sig1.setFreq(self.freqFilt)
        q = random.triangular(0.5,4,2)
        self.sig1.setQ(q)
        self.sig1.setType(self.fType)
        return self


class Chorused(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        self.intense = intense
        coin1 = random.randint(0,1)
        if len(self.inp) > 1 or coin1 == 0:
            self.lfoDepFreq = [random.uniform(0.1,7*self.intense) for i in range(cons.NUMOUTS)]
        else: 
            self.lfoDepFreq = random.uniform(0.1,7*self.intense)
        self.depChor = LFO(self.lfoDepFreq, type=random.randint(0,6), mul=2.4, add=2.5)
        dep2 = self.depChor*random.random()
        feed = random.triangular(0,0.7,0.03)
        coin2 = random.randint(0,1)
        if len(self.inp) > 1 or coin2 == 0:
            self.lfoBalFreq = [random.uniform(0.1,10*self.intense) for i in range(cons.NUMOUTS)]
        else: 
            self.lfoBalFreq = random.uniform(0.1,10*self.intense)
        self.balChor = LFO(self.lfoBalFreq, type=random.randint(0,6), mul=.5, add=.5)
        bal = self.balChor*random.random()
        self.sig1 = Chorus(self.inp, dep2*self.intense, feed*self.intense, bal)
        Sig.__init__(self, self.sig1,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self
    def setNewValues(self):
        coin1 = random.randint(0,1)
        if len(self.inp) > 1 or coin1 == 0:
            self.lfoDepFreq = [random.uniform(0.1,7*self.intense) for i in range(cons.NUMOUTS)]
        else: 
            self.lfoDepFreq = random.uniform(0.1,7*self.intense)
        self.depChor.setFreq(self.lfoDepFreq)
        self.depChor.setType(random.randint(0,6))
        feed = random.triangular(0,0.7,0.03)
        coin2 = random.randint(0,1)
        if len(self.inp) > 1 or coin2 == 0:
            self.lfoBalFreq = [random.uniform(0.1,10*self.intense) for i in range(cons.NUMOUTS)]
        else: 
            self.lfoBalFreq = random.uniform(0.1,10*self.intense)
        self.balChor.setFreq(self.lfoBalFreq)
        self.balChor.setType(random.randint(0,6))
        # self.sig1.setDepth(self.depChor*random.random()*self.intense)
        self.sig1.setFeedback(feed*self.intense)
        # self.sig1.setBal(self.balChor*random.random())
        return self


class Panning(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        self.intense = intense
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
    def setNewValues(self):
        if len(self.inp) == 2:
            spread = 0
        else:
            spread = random.uniform(0.,0.7)
        self.sig1.setSpread(spread)
        freq = random.uniform(0.1,2*self.intense)
        self.panPan1.setFreq(freq)
        return self

class Delayer(Sig):
    def __init__(self, inp, intense=1., mul = 1, add = 0):
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
    def setNewValues(self):
        self.setTimeFb()
        return self


class Phasered(Sig):
    def __init__(self, inp, intense=1, mul = 1, add = 0):
        self.inp = inp
        self.intense = intense
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
        self.spread = LFO(self.lfoSpread, type=random.randint(0,6), mul=lfoSpMul,add=lfoSpAdd)
        q = random.uniform(1,20)
        feed = random.uniform(0.1,0.8)
        num = int(random.randint(1,20)*intense)+1
        self.sig1 = Phaser(self.inp, self.freqPhas, self.spread, q, feed, num, mul=0.7)
        self.sig2 = self.sig1.mix(cons.NUMOUTS)
        Sig.__init__(self, self.sig2,mul,add)
    def setInput(self,inp2):
        self.inp2 = inp2
        self.sig1.setInput(self.inp2)
        return self
    def setNewValues(self):
        coin2 = random.randint(0,1)
        if coin2 == 0:
            self.lfoFreq = [random.uniform(0.1,5*self.intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoFreq = random.uniform(0.1,5*self.intense)
        lfoFreqAdd = random.triangular(50,3000,400)
        lfoFreqMul = random.uniform(10,lfoFreqAdd/1.5)
        self.freqPhas.setFreq(self.lfoFreq)
        self.freqPhas.setType(random.randint(0,6))
        self.freqPhas.setMul(lfoFreqMul)
        self.freqPhas.setAdd(lfoFreqAdd)
        lfoSpAdd = random.uniform(.8,1.4)
        lfoSpMul = random.uniform(.4,1.2)
        coin3 = random.randint(0,1)
        if coin3 == 0:
            self.lfoSpread = [random.uniform(0.1,5*self.intense) for i in range(cons.NUMOUTS)]
        else:
            self.lfoSpread = random.uniform(0.1,5*self.intense)
        self.spread.setFreq(self.lfoSpread)
        self.spread.setType(random.randint(0,6))
        self.spread.setMul(lfoSpMul)
        self.spread.setAdd(lfoSpAdd)
        q = random.uniform(1,20)
        feed = random.uniform(0.1,0.8)
        self.sig1.setQ(q)
        self.sig1.setFeedback(feed)
        return self


class FxMixer(Sig):
    def __init__(self, inPut, numFXs=2, modu=1, mul=1, add=0):

        self.inPut = inPut
        self.modu = modu
        self.numFXs = numFXs

        self.updateCounter = 0 # used to iterate through the FXs to update their values

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
        self.mixer1 = Mixer(8, 2, vari.fxChangeTime/1.1)

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

        self.patChange = Pattern(self.changeValues,vari.fxChangeTime/8).play(delay=vari.fxChangeTime/2)

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

    def changeFXs(self):
        # assigns new effects
        self.routing(target = 0.)
        self.fxSel()
        self.routing(target = 1.)
        return self

    def changeValues(self):
        # change the fx values when not in use (mixer amp of the channel == 0)
        fx1Val = self.fx1.get()
        fx2Val = self.fx2.get()
        fx3Val = self.fx3.get()
        fx4Val = self.fx4.get()
        fx5Val = self.fx5.get()
        fx6Val = self.fx6.get()
        fx7Val = self.fx7.get()

        # updates iterate to avoid CPU peaks
        if self.updateCounter == 0:
            if fx1Val == 0.0:
                # print "changin 1"
                self.fx1.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 1:
            if fx2Val == 0.0:
                # print "changin 2"
                self.fx2.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 2:
            if fx3Val == 0.0:
                # print "changin 3"
                self.fx3.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 3:
            if fx4Val == 0.0:
                # print "changin 4"
                self.fx4.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 4:
            if fx5Val == 0.0:
                # print "changin 5"
                self.fx5.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 5:
            if fx6Val == 0.0:
                # print "changin 6"
                self.fx6.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 6:
            if fx7Val == 0.0:
                # print "changin 7"
                self.fx7.setNewValues()
            self.updateCounter += 1
        elif self.updateCounter == 7:
            self.updateCounter = 0



