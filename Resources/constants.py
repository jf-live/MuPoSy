# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.

import os

#### How many outputs to use
NUMOUTS = 2

#### How many SynthGen and Samples streams to create
NUMGENS = 1

NUMSAMPS = 1


#### Path to the 'Resources' folder
RESOURCE_PATH = os.path.join(os.path.split(__file__)[0])
MAIN_PATH = os.getcwd()
STATS_PATH = os.path.join(MAIN_PATH, 'Stats')
TEMP_PATH = os.path.join(RESOURCE_PATH,'TempFiles')

### For init, tests if path exists, if not creates it
if os.path.isdir(STATS_PATH) is True:
    print "Stats folder is go"
else:
    os.makedirs(STATS_PATH)

if os.path.isdir(TEMP_PATH) is True:
    print "Temp folder is go"
else:
    os.makedirs(TEMP_PATH)


#### List of poetry txt files available for Tts
POEMS = ['GastonMiron.txt', 'Nelligan.txt', 'SaintDenysGarneau.txt']
POEMS = [os.path.join(RESOURCE_PATH, POEMS[i]) for i in range(len(POEMS))]


#### Folder where sound files are located for playback
SFFOLDER_PATH = os.path.join(RESOURCE_PATH, "SoundFiles" )
SONTEST = os.path.join(SFFOLDER_PATH, "Scratch tete.wav")



SCALES = {'Power':[0,7],'M':[0,2,4,5,7,9,11], 'm':[0,2,3,5,7,8,11], 'Whole':[0,2,4,6,8,10],
            'Half':[0,1,2,3,4,5,6,7,8,9,10,11], 'Tri_M':[0,4,7],
            'Tri_m':[0,3,7], 'Quad_M7':[0,4,7,10],'Quad_m7':[0,3,7,10]}

KEYS = {'C':0, 'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'G':7,
        'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}



EVAL_CHOICES = ['Keep','Change','Whatevs']



