# encoding: utf-8


########### MuPoSY - MAIN #####################################################
#
# Jean-Francois Primeau
# 2016
#
# The working title MuPoSY stands for Music Poetry System (Système de 
# Musique et Poésie).  The point of this software is to create an interactive 
# installation generating algorithmic music and poetry.
#
# Poems are generated from existing poems found in Gaston Miron's L'homme 
# rapaillé, Hector de Saint-Denys Garneau's Regards et jeux dans l’espace, and 
# Émile Nelligan's complete works.
#
# Sound generators are located in the SynthGen and SamplePlay files.
# Sound effects are located in the Effects file.
# Voice synthesis and text retrieval tools are located in the Voix file.
# The algorithmic engine is located in the Algo file. (TBD)
# The kinect interactions are managed in the Interactivity file.
# A few utilities are stored in the utilities file.
#
# Most variables are generated in the variables file. (TBD)
# Constants are stored in the constants file.
#
# To add text to the data file of the current run, use util.dataF.write(str).
#
# IMPORTANT : This script must be run on Mac OS or Linux in order to work.
#
# The "translate" function in utilities was taken from Adam Luchjenbroers on 
# 	http://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
#
###############################################################################
### Seeding is still useful to recall 'presets'.


from pyo import *
# Server booted here because it is needed when the resources are loaded
s = Server(sr = 48000) #, buffersize = 512)
print pm_list_devices()
# nanoKontrol is connected here.  See Midi.py for details.
s.setMidiInputDevice(0)
s.boot()

import Resources.utilities as util
import Resources.constants as cons
import Resources.variables as vari
import Resources.Interactivity as inte
import Resources.Voix as voix

import Resources.Engine as engi
import Resources.Algo as algo
import Resources.SynthGen as synt
import Resources.SamplePlay as samp
import Resources.Effects as effe



print cons.MAIN_PATH


########### What follows is only for early testing purposes...  #############


# All calling is now done from Engine.py and Voix.py


# engi.Engine()




s.gui(locals())
