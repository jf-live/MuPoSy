# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
from pyo import *
# s=Server().boot()
import random, os, thread
# import Effects as effe
import constants as cons


# s.start()
# snd = SndTable(SNDS_PATH + "/transparent.aif")
# env = HannTable()
# pos = Phasor(snd.getRate()*.25, 0, snd.getSize())
# dur = Noise(.001, .1)
# g = Granulator(snd, env, [1, 1.001], pos, dur, 24, mul=.1).out()

numFXs = 2
origFXs = []
origFXs = random.sample([0,1,2,3,4,5,6],numFXs)

###FX order sorting
### Disto always 1st, then harmon, filter or phaser, 
###     then chorus or panning, then delay.
s = Server().boot()
s.start()
lfo = Sine(freq=4, mul=.02, add=1)
lf2 = Sine(freq=.25, mul=20, add=30)
a = Blit(freq=[100, 99.7]*lfo, harms=lf2, mul=.3).out()
s.gui(locals())



# class DistoJF(Sig):
#     def __init__(self, inp, mul=1,add=0):
#         self.inp = inp
#         self.a = Disto(inp, 0.9)
#         Sig.__init__(self, self.a,mul,add)
#     def setInput(self,inp2):
#         self.inp2 = inp2
#         self.a.setInput(self.inp2)
#         return self

# class DelayJF(Sig):
#     def __init__(self, inp, mul=0.6,add=0):
#         self.inp = inp
#         self.a = Delay(self.inp, feedback = [0.6,0.61])
#         Sig.__init__(self, self.a,mul,add)
#     def setInput(self,inp2):
#         self.inp2 = inp2
#         self.a.setInput(self.inp2)
#         return self






# freqMod = Sine(1).range(300,1000)
# a1 = Sine(freqMod,mul=0.2)
# a2 = Sine(mul = 0.2)

# b = effe.Distor(a1,mul=0.4)

# c = effe.Harmon(b,mul=0.4)

# d = effe.Filter(c, mul=0.5)

# e = effe.Chorused(d)

# f = effe.Panning(e)

# g = effe.Delayer(f)

# h = effe.Phasered(g)

# i = Compress(h,-40,ratio = 20)
# i.out()


# # print "streams:",s.getNumberOfStreams()




# def whatIsOn():
#     global a1, a2, b,c,d,e,f,g,h
#     slots = [a1,b,c,d,e,f,g,h]
#     onOff = [b.isPlaying(),c.isPlaying(),d.isPlaying(),e.isPlaying(),f.isPlaying(),g.isPlaying(),h.isPlaying()]

#     try:
#         t = [i for i, x in enumerate(onOff) if x == False]
#     except:
#         pass

#     if t != test:
#         test = t


#         for i in t:
#             if len(t) == 1:
#                 slots[t[0]+2].setInput(slots[t[0]])

#         # if t[-1]-t[-2]











# pat = Pattern(whatIsOn, 0.5).play()


# s.gui(locals())