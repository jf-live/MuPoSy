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


# to get CC value
class MidiCCIn():
    def __init__(self, which):
        """
        which should be either "Snd" or "Voice"
        """
        self.which = which
        self.ctl = Midictl(ctlnumber=0, minscale=0, maxscale=127)
        self.p = Port(self.ctl, .02)

    def retVal(self):
        updateVal = self.ctl.get()
        if self.which == "Snd":
            vari.currentCCSnd = updateVal
        elif self.which == "Voice":
            vari.currentCCVoix = updateVal


# not in use right now, to be used with kinect
class OSCIn():
    def __init__(self):
        self.rec = OscReceive(port=10001, address = ['/depth'])

    def getSig(self):
        return self.rec['/depth']

    def getVal(self):
        return self.rec.get(identifier = '/depth')



# To retrieve MIDI CC and affect the sound accordingly
midiMet = util.eventMetSnd
signalInSnd = MidiCCIn("Snd")
signalInVoice = MidiCCIn("Voice")
trSnd = TrigFunc(midiMet, signalInSnd.retVal)
trVoice = TrigFunc(midiMet, signalInVoice.retVal)

# To change the variables according to CC data

def distance():
    # all variables are taken from the same MIDI CC value
    # various names are used for clarity
    sineRev = synthMul = sineMul = filtFreq = vari.currentCCSnd
    mTempo = tempo = vari.currentCCSnd

    # adjusting hipass for samples
    if filtFreq < 40:
        vari.outFiltFreqSig.setValue(rescale(filtFreq, 0,40, 30, 2000))
    elif filtFreq >= 40 and filtFreq < 80:
        vari.outFiltFreqSig.setValue(rescale(filtFreq, 40,80, 2000, 7000))
    elif filtFreq >= 80:
        if filtFreq > 100:
            filtFreq = 100
        vari.outFiltFreqSig.setValue(rescale(filtFreq, 80,100, 7000, 12000))
    if sineMul < 10:
        sineMul = 10
    if sineMul > 85:
        sineMul = 85
    vari.sineGenMul = rescale(sineMul, 10, 85, 0,1)
    if synthMul < 10:
        synthMul = 10
    if synthMul > 100:
        synthMul = 100
    vari.synthGenMul.setValue(Scale(Sig(synthMul),10,100,1,0.1,1.5))
    if sineRev < 50:
        sineRev = 50
    if sineRev > 100:
        sineRev = 100
    vari.sineRevMul = rescale(sineRev,50,100,0.8,0.99,1)
    vari.sineTempo = rescale(tempo, 0, 127, 0.7,0.3)
    if mTempo < 30:
        vari.mainTempo = rescale(mTempo, 0, 30, vari.mainTempoInit,vari.mainTempoInit/2)
    elif mTempo >= 30 and mTempo < 45:
        vari.mainTempo = rescale(mTempo, 30, 45, vari.mainTempoInit/2,vari.mainTempoInit/8)
    elif mTempo >= 45 and mTempo < 65:
        vari.mainTempo = rescale(mTempo, 45, 65, vari.mainTempoInit/8,vari.mainTempoInit/16)
    elif mTempo >= 65:
        if mTempo > 100:
            mTempo = 100
        vari.mainTempo = rescale(mTempo, 65, 100, vari.mainTempoInit/16,0.01)


patMIDI = Pattern(distance,0.001).play(delay=2)

    


