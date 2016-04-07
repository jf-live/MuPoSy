#!/usr/bin/env python
# encoding: utf-8


# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
#
# For the time being: MIDI CC input to control installation
#
# Some issues with the integration of the Kinect have led me to use a Korg
# nanoKontrol2 to interact with the installation for the time being. 
# It is of interest to note that this solution also allows for fast testing in
# an environment where the Kinect setup is not possible.


from pyo import *
import variables as vari
import utilities as util


# to get CC for voice, independant as voice stops this when playing
class MidiCCIn():
    def __init__(self):
        self.ctl = Midictl(ctlnumber=0, minscale=0, maxscale=127)
        self.p = Port(self.ctl, .02)

    def retVal(self):
        updateVal = self.ctl.get()
        vari.currentCCVoix = updateVal

# to get CC for everything else
class MidiCCInSnd():
    def __init__(self):
        self.ctl = Midictl(ctlnumber=0, minscale=0, maxscale=127)
        self.p = Port(self.ctl, .02)

    def retVal(self):
        updateVal = self.ctl.get()
        vari.currentCCSnd = updateVal




class OSCIn():
    def __init__(self):
        self.rec = OscReceive(port=10001, address = ['/depth'])

    def getSig(self):
        return self.rec['/depth']

    def getVal(self):
        return self.rec.get(identifier = '/depth')



# To retrieve MIDI CC and affect the sound accordingly
midiMet = util.eventMetSnd
signalIn = MidiCCInSnd()
tr = TrigFunc(midiMet, signalIn.retVal)

# To change the variables according to CC data

def distance():
    # must be a better way for the variables...
    filtFreq = vari.currentCCSnd
    sineMul = vari.currentCCSnd
    synthMul = vari.currentCCSnd
    tempo = vari.currentCCSnd
    mTempo = vari.currentCCSnd
    # adjusting hipass 
    if filtFreq < 40:
        vari.outFiltFreq = util.translate(filtFreq, 0,40, 0, 2000)
    elif filtFreq >= 40:
        if filtFreq > 100:
            filtFreq = 100
        vari.outFiltFreq = util.translate(filtFreq, 40,100, 2000, 8000)
    if sineMul < 10:
        sineMul = 10
    if sineMul > 85:
        sineMul = 85
    vari.sineGenMul = util.translate(sineMul, 10, 85, 0,1)
    if synthMul < 50:
        synthMul = 50
    if synthMul > 100:
        synthMul = 100
    vari.synthGenMul.setValue(Scale(Sig(synthMul),10,100,1,0.1,1.5))
    # vari.synthGenMul = util.translate(synthMul, 10, 80, 1,0.1)
    vari.sineTempo = util.translate(tempo, 0, 127, 0.7,0.3)
    if mTempo > 80:
        mTempo = 80
    vari.mainTempo = util.translate(mTempo, 0, 80, vari.mainTempoInit,8)


patMIDI = Pattern(distance,0.01).play(delay=2)

    


