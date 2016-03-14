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


#### For testing purposes
# print pm_list_devices()
# s = Server()
# s.setMidiInputDevice(0)
# s.boot()


class MidiCCIn():
	def __init__(self):

		self.ctl = Midictl(ctlnumber=0, minscale=0, maxscale=100)
		self.p = Port(self.ctl, .02)


	def retVal(self):
		val = self.ctl.get()
		if val < 20:
			# print "wow"
			vari.currentCC0Val = val

		elif val >=20 and val <60:
			# print "WoooT"
			vari.currentCC0Val = val

		elif val >= 60:
			# print "MAX POWER!"
			vari.currentCC0Val = val
			

# a = MidiCCIn()

# met = Metro(.1).play()
# tr = TrigFunc(met, a.printin)



# s.gui(locals())