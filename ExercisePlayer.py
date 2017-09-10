#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 13:03:37 2017

@author: yolandatiao

#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#
# Purpose: Play custom audio in with a certain time order                     #
# Input: A "instruction" file (orders) and recorded wav files                 #
# Input dependent: Mac recorder and ffmpeg package                            #
# Last update: 9/10/17                                                        #
#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#-----#

"""

#####------------------ Import START ------------------#####
import os
import pyaudio
import wave
import time
import csv
from Tkinter import Tk    # For opening file user interface
from tkFileDialog import askopenfilename    # For opening file user interface
from astropy.io import ascii    # For using ascii table to open csv
from astropy.table import Table, Column    # For using astropy table functions
#####------------------ Import END ------------------#####

#####------------------ Config START ------------------#####
audioGal="/Users/yolandatiao/Documents/0_Programming/PythonWorkShop/ExercisePlayer/sound_gallary"
insGal="/Users/yolandatiao/Documents/0_Programming/PythonWorkShop/ExercisePlayer/Instruction_gallary"
ins=""

courseEndSound="TheSNCFJingle2.wav"
endSound="RainAndStorm.wav"
startSound="Start.wav"

#Flags "testSound","testNoSound","Real"
testFlag="testSound"

#User ("Eddie","Yolanda")
usrList=["Eddie","Yolanda"]
usrLog=["No","No"]
logfile="/Users/yolandatiao/Documents/0_Programming/PythonWorkShop/Exercise_player/ExerciseLogBook.csv"
#####------------------ Config END ------------------#####

#####------------------ Self Defined functions START ------------------#####
def playWav(audioPath,fname):
    print "play %s"%fname
    if (testFlag=="testSound" or testFlag=="Real"):
        os.chdir(audioGal)
        #define stream chunk   
        chunk = 1024  
        
        #open a wav format music  
        f = wave.open(fname,"rb")  
        #instantiate PyAudio  
        p = pyaudio.PyAudio()  
        #open stream  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        #read data  
        data = f.readframes(chunk)  
        
        #play stream  
        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  
        
        #stop stream  
        stream.stop_stream()  
        stream.close()  
        
        #close PyAudio  
        p.terminate()

def sleepTimer(secN):
    print "count down %s secondes" %secN
    if testFlag=="Real":
        time.sleep(secN)
        
def FindFile():
    print 'Please find your instruction file: '
    root = Tk()
    root.withdraw()
    root.update()
    inFile = askopenfilename()
    print 'You are opening file: %s'% inFile   
    print '\n'
    return inFile

def intList(listx):
    newlist=[]
    for i in listx:
        newlist.append(int(i))
    return newlist

#####------------------ Self Defined functions END ------------------#####

#####------------------ Main START ------------------#####
###----- Determine player
testFlag=raw_input("Real exercise time? (Real, testSound, testNoSound)")

if testFlag=="Real":
    print "Who is exercising today? (Yes/No)"
    print "\n"
    print "\n"
    for x in xrange(0,len(usrList)):
        usrLog[x]=raw_input("%s: "%usrList[x])
    for x in xrange(0, len(usrList)):
        if (usrLog[x]).lower()=="yes":
            print "%s is hardworking!!" %usrList[x]
        else:
            print "%s is a piggy!!" %usrList[x]

###----- Find instruction
print "\n"
ins=FindFile()


###----- Play
os.chdir(insGal)
with open(ins, "r") as fin:
    rfin=csv.reader(fin, delimiter=",")
    next(rfin)
    
    tmLag=0
    for row in rfin:
        playWav(audioGal, "%s.wav"%row[0])
        tmLag=int(row[1])
        if tmLag>=15:
            playWav(audioGal, startSound)
            tmN=int(tmLag/15)-1
            while tmN>0:
                tmReminder="%s.wav"%(tmN*15)
                sleepTimer(15)
                playWav(audioGal,tmReminder)
                tmN-=1
            playWav(audioGal,courseEndSound)
        print "\n"
    playWav(audioGal, endSound)

###----- Write Log
if testFlag=="Real":
    logTab=ascii.read(logfile)
    print logTab
    date=str((time.strftime("%m/%d/%y")))
    
    insfileNF=ins.split("/")[-1].split(".")[0]
    
    insTab=ascii.read(ins)
    insTabTime=list(insTab.columns[1])
    insTabTime=intList(insTabTime)
    sumInsTabTime=sum(insTabTime)
    insMin=int(sumInsTabTime/60)
    insSec=sumInsTabTime%60
    recTime="%s min %s sec" %(insMin, insSec)
    
    newRow=[date,insfileNF,recTime]+usrLog
    print newRow
    
    logTab.add_row(newRow)
    
    ascii.write(logTab,logfile,format="csv",overwrite=True)


#####------------------ Main END ------------------#####
