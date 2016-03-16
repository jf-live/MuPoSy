# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.


import time, random, os
import variables as vari
import constants as cons
from pyo import *


#seeding to replay a set of sounds, kinda like presets
#imported first so that the seed is effective when the variables are picked
rSeed = random.randint(1,9999999999999999999999999999999)
print 'Seed: ', rSeed
random.seed(rSeed)


# Trigger generators for synthGens
genMet = Metro(vari.mainTempo).play()
genEuc = Euclide(vari.mainTempo, onsets = [8,5],poly=4).play()


# Trigger generator for event detection
eventMetVoix = Metro(0.05).play()
eventMetSnd = Metro(0.05).play()


changeMet = Metro(vari.mainTempo*4)



# to map values
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


class TxtFile:
    def __init__(self, name):
        """
        Name should include path to Stats folder.
        """
        self.dataFile=open(name, 'w')

    def write(self, string):
        self.dataFile.write(string)
        return self

    def writeln(self, string):
        self.dataFile.write(string + '\n')
        return self
    def writelnln(self, string):
        self.dataFile.write(string + '\n\n')
        return self

    def close(self):
        self.dataFile.close()
        return self

# Create and write txt file at initialization with date/time as name.
createTime = time.strftime("%c").replace(' ','_')
createTime = createTime.replace('/','').replace(':','')
fileName = 'Test_' + createTime[:-5] + '.txt'
fileName = os.path.join(cons.STATS_PATH,fileName)
dataF = TxtFile(fileName)
dataF.write('\n' + 'seed is: ' + str(rSeed) + '\n')


