#!/usr/bin/env python
# encoding: utf-8

# Jean-Francois Primeau
# 2016
# This script file is to be filed under the Resources directory of the MuPoSy
# project.
#
# Voice Synthesis from textual content.
#
# Original concept was to retrieve content directly from the web, but problems 
# with html parsing and special characters encoding forced me to redirect my 
# efforts elsewhere for the time being.

# Use util.dataF.writeln(str) to add a line of text to the data file.



import constants as cons
import variables as vari
import utilities as util
import Interactivity as inte
import SamplePlay as samp
import time, random, subprocess, os, threading, sys
from itertools import islice
from HTMLParser import HTMLParser
from pyo import *



# s = Server().boot()
# s.start()


# Lines of poems are selected
class TxtSelect:
    def __init__(self,  listOfTxts = cons.POEMS):
        #Creation of a temp txt file that is passed on to generate the Tts audio file
        tempTxt = util.TxtFile(os.path.join(cons.TEMP_PATH,'tempo.txt'))
        # Add pauses between lines of text for a more natural flow
        pause = str(random.randint(250,600))
        pauseMSG = '[[slnc ' + pause + ']]'

        for i in range(random.randint(1,3)):
            numLines = random.randint(2,4)
            for i in range(numLines):
                if i == 0:
                    poemChoices = self.pickALine(listOfTxts)
                    vers = random.choice(poemChoices)
                    #First line starts with a Capital letter
                    while vers.startswith(' ') or vers.startswith(' ') \
                                               or self.hasNumbers(vers)==True \
                                               or vers[0].isupper()==False:
                        vers = random.choice(poemChoices)
                    util.dataF.writeln(vers)
                    tempTxt.writelnln(vers)
                    tempTxt.writelnln(pauseMSG)
                elif i != numLines - 1:
                    poemChoices = self.pickALine(listOfTxts)
                    vers = random.choice(poemChoices)
                    #Middle verses start with lowercase letter.
                    while vers.startswith(' ') or vers.startswith(' ') \
                                               or self.hasNumbers(vers)==True \
                                               or vers[0].isupper()==True \
                                               or vers.endswith('.'):
                        vers = random.choice(poemChoices)
                    util.dataF.writeln(vers)
                    tempTxt.writelnln(vers)
                    tempTxt.writelnln(pauseMSG)
                else:
                    poemChoices = self.pickALine(listOfTxts)
                    vers = random.choice(poemChoices)
                    #Final line ends with . or ... or !
                    # Except for Miron, because the same ! line is always selected
                    miron = os.path.join(cons.RESOURCE_PATH, 'GastonMiron.txt')
                    if self.selPoem == miron:
                        print 'miron!'
                        while vers.startswith(' ') or vers.startswith(' ') \
                                                   or self.hasNumbers(vers)==True \
                                                   or vers[0].isupper()==True \
                                                   or vers.startswith('*'):
                            vers = random.choice(poemChoices)
                            vers = vers + '.'
                    else:
                        while (vers.endswith('.') or vers.endswith('!')) == False:
                            vers = random.choice(poemChoices)
                    util.dataF.writeln(vers)
                    tempTxt.writelnln(vers)
                    tempTxt.writelnln(pauseMSG)
            util.dataF.writeln('\n')
            tempTxt.writeln('\n')
            tempTxt.writelnln(pauseMSG)
        tempTxt.close()

    def pickALine(self, listOfTxts):
        self.selPoem = random.choice(listOfTxts)
        print self.selPoem
        with open(self.selPoem) as txtIn:
            poemTxt = (line.rstrip() for line in txtIn)
            poemTxt = (line.replace('ô', 'oh') for line in poemTxt)
            poemTxt = (line.replace('Ô', 'Oh') for line in poemTxt)
            poemTxt = list(line for line in poemTxt if line)

        return poemTxt

    def hasNumbers(self,inputString):
        return any(char.isdigit() for char in inputString)

    def txtPath(self):
        # dirPath = os.path.dirname(os.path.realpath('tempo.txt'))
        txtPath = os.path.join(cons.TEMP_PATH, 'tempo.txt')
        return txtPath

class Tts:
    def __init__(self, inTxt):#, outPath):
        # Here is the terminal command line to use.  say is the TTS app, a string 
        # to be read, -o is the audio file to save the spoken text to.
        #Outputs aiff file, 48kHz 24bit
        # self.outPath = outPath
        # print 'test', self.outPath
        self.inTxt = inTxt
        self.outName = int(time.time()*1000)

        ### Text-to-speech on OSX
        if sys.platform.startswith("darwin"):
            self.outFullName = str(self.outName) + ".aiff"
            self.outFullName = os.path.join(cons.TEMP_PATH, self.outFullName)
            self.outSettings = " --data-format=BEI24@48000 -r 120 -f"
            command = "say -o " + self.outFullName + self.outSettings + self.inTxt
        ### Text-to-speech on linux
        elif sys.platform.startswith("linux"):
            self.outFullName = str(self.outName) + ".wav"
            self.outSettings = " "
            command = "espeak -w " + self.outFullName + self.outSettings
            command = command + '-f "%s"' % self.inTxt

        print 'command', command

        # Here the command line is processed in a separate thread, not blocking 
        # the rest of the code.  shell=True needs to be included.
        self.process=subprocess.Popen(command, shell=True)
        # sf = SfPlayer(myPath).out(delay = 4) #This never worked...

    def getPath(self):
        somePath = os.path.dirname(os.path.realpath(self.outFullName))
        fulPath = os.path.join(somePath, self.outFullName)
        return fulPath

    def getName(self):
        return self.outFullName

    def clean(self):
        print "test clean"
        os.remove(self.inTxt)
        os.remove(self.outFullName)
        print 'clean'



class ReadPoem:
    def __init__(self, delay):
        self.delay = delay
        #Generates sound from poems
        self.poem = TxtSelect()
        self.poem1 = Tts(self.poem.txtPath())
        vari.poemPath = self.poem1.getPath()

    def playVoice(self):
        self.c = samp.SoundRead(1, speed=1, fileSel = vari.poemPath)
        self.c1 = self.c.getOut()
        self.c2 = Biquad(self.c1, 800,type=1, mul=1.).out()
        self.time = random.uniform(0.03,0.2)
        self.randTime = [random.uniform(0.9,1.1)*self.time for i in range(2)]
        self.c3 = Delay(self.c2, self.randTime, 
                                 random.uniform(0.1,0.5), 
                                 mul = 0.9)
        self.c23 = self.c2 + self.c3
        self.c4 = Freeverb(self.c23, .5, mul = 0.8, bal = 0.3).out()
        self.done = self.cleanUp()

    def cleanUp(self):
        self.clean = TrigFunc(self.c1['trig'], self.poem1.clean)

def midiCcDetectOn():
    midiMet.play()

def ccValReset():
    # time.sleep(15)
    vari.currentCCVoix = 0
    midiMet.play()

# For CallAfter-ing, to prevent the instances from being garbaged after the
# function is processed.
callerSnd = None
callerReset = None
po = None
def playing(delay):
    global callerSnd
    global callerReset
    global po
    # print "Voix"
    # print "vari",vari.currentCCVoix
    if vari.currentCCVoix > 110:
        midiMet.stop()
        po = ReadPoem(delay)
        callerSnd = CallAfter(po.playVoice, time=2)
        callerReset = CallAfter(ccValReset, time=30)

signalIn = inte.MidiCCIn()

# Allow enough time to render the Tts
ttsDel = 2

# Triggers the Tts if MIDI CC 0 returns >100
midiMet = util.eventMetVoix
tr = TrigFunc(midiMet, signalIn.retVal)
tr2 = TrigFunc(midiMet, playing, ttsDel)




# s.gui(locals())

