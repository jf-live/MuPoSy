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


