#!/usr/bin/python

import Tkinter as g
import tkFont
import subprocess
import time
import threading

class WriteOrElse:
    def __init__(self, master):
        self.master=master
        self.Font = tkFont.Font(family="Arial", size=15)
        self.lFont = tkFont.Font(family="Arial", size=30)
        self.xxlFont = tkFont.Font(family="Arial", size=100)
        
        self.words=500 #target amount of words
        self.minutes=20 #total time in minutes
        self.threshold=5 #time before punishment starts
        self.music=0 #is the music on or not?
        self.paused = False #is the program currently paused
        self.timeElapsed = 0 #how much time has passed
        self.timeLeft = 0 #countdown in seconds
        self.totalwords = 0 #total number of words in the text
        self.wpm = 0 #current speed
        self.idle = 0 #time since last typing actitity in seconds
        self.difflength= 0 #last detected length of the text

        #button bar
        self.fBar=g.Frame(master, bd=1)
        self.fBar.grid(row=1,column=1, columnspan=30, sticky=g.W)

        self.bPause = g.Button(self.fBar, text="Pause", command=self.pause)
        self.bPause.grid(row=1, column=2)
        self.bStart = g.Button(self.fBar, text="Start", command=self.start)
        self.bStart.grid(row=1, column=3)
        self.bStop = g.Button(self.fBar, text="Stop", command = self.stop)
        self.bStop.grid(row=1, column=4)
        self.bQuit = g.Button(self.fBar, text="Exit", command=self.master.quit)
        self.bQuit.grid(row=1, column=5)
        self.bCopy= g.Button(self.fBar, text="Copy text to clipboard", command=self.clipboard)
        self.bCopy.grid(row=1, column=1)

        #some text
        self.lTitle = g.Label(self.master, text="Write or else!", font=self.lFont)
        self.lTitle.grid(row=2, column=5, sticky=g.W, columnspan=10)
        

        #writing area
        self.fWriting=g.Frame(master,width=600, height=600, bd=1)
        self.fWriting.grid(row=3, column=4, columnspan=10)

        self.txt = g.Text(self.fWriting, borderwidth=3, relief="sunken")
        self.txt.config(font=self.Font, undo=True, wrap='word')
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        self.scrollb = g.Scrollbar(self.fWriting, command=self.txt.yview)
        self.scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = self.scrollb.set
        
        #wpm count & timer, word count

        self.fStats = g.Frame(master, width=600, height=100, bd=1)
        self.fStats.grid(row=4, column=4, columnspan=10)

        self.lWords = g.Label(self.fStats, text="Words left:", font=self.lFont)
        self.lWords.grid(row=1, column=1)
        self.lWordsV = g.Label(self.fStats, text="0", font=self.lFont)
        self.lWordsV.grid(row=2, column=1)

        self.lTime = g.Label(self.fStats, text="Time left:", font=self.lFont)
        self.lTime.grid(row=1, column=2)
        self.lTimeV = g.Label(self.fStats, text="000:00", font=self.lFont)
        self.lTimeV.grid(row=2, column=2)

        self.lWpm = g.Label(self.fStats, text="WPM:", font=self.lFont)
        self.lWpm.grid(row=1, column=3)
        self.lWpmV = g.Label(self.fStats, text="0", font=self.lFont)
        self.lWpmV.grid(row=2, column=3)

        #settings
        self.fSettings = g.Frame(master, bd=1)
        self.fSettings.grid(row=3, column=15)

        self.lMinutes = g.Label(self.fSettings, text="Minutes:", font=self.Font)
        self.lMinutes.grid(row=1, column=1)
        self.iMinutes = g.Entry(self.fSettings, width=30)
        self.iMinutes.grid(row=2, column=1)

        self.lTargetWords = g.Label(self.fSettings, text="Words:", font=self.Font)
        self.lTargetWords.grid(row=3, column=1)
        self.iTargetWords = g.Entry(self.fSettings, width=30)
        self.iTargetWords.grid(row=4, column=1)

        self.bSave = g.Button(self.fSettings, text="Save", font=self.Font, command=self.settings)
        self.bSave.grid(row=5, column=1)

        #you can't pause or stop something that's not running, so disable these
        self.bPause.config(state=g.DISABLED)
        self.bStop.config(state=g.DISABLED)
    
        #timer state
        self.tstate=False

    def count(self):
        #print "count"
        self.timeElapsed+=1
        self.timeLeft-=1
        # update total words
        text=self.txt.get(0.0,g.END)
        self.totalwords=len(text.split())

        self.wpm=self.totalwords/(self.timeElapsed/60.) # calculate wpm
        
        #diff text, if idle, increment idle timer. If idle > threshold, punish, else, reward
        length=len(text)
        if(length>self.difflength):
            #active typing, way to go
            self.reward()
            self.idle=0
            self.difflength=length
        else:
            #idling! bad!
            self.idle+=1
            if(self.idle>=self.threshold):
                self.punish()

        #update visible stats
        self.lWordsV["text"]=self.words-self.totalwords
        self.lWpmV["text"]="%.2f" % self.wpm
        #construct time left string
        seconds=self.timeLeft%60
        minutes=(self.timeLeft-seconds)/60
        if(seconds<10):seconds="0"+str(seconds)
        if(minutes<10):minutes="0"+str(minutes)
        if(minutes<100):minutes="0"+str(minutes)
        self.lTimeV["text"]=str(minutes)+":"+str(seconds)
        
        #if timer is not cancelled, repeat self
        if(self.tstate):
            self.master.after(1000, self.count)

    def punish(self):
        #stop music if it is running
        if(self.music):
            subprocess.call(["mocp", "--pause"])
            self.music=False
        #set background to red
        self.txt["bg"]="red"
    def reward(self):
        #start music if it isn't on
        if(not self.music):
            subprocess.call(["mocp", "--unpause"])
            self.music=True
        #set background to white
        self.txt["bg"]="white"
    def start(self):
        #reset stats
        self.timeElapsed=0
        self.timeLeft=self.minutes*60
        self.totalwords=0
        self.wpm=0
        self.difftext=0

        #start timer if it isn't already running (not possible, but you never know)
        if(not self.tstate):
            self.tstate=True
            self.count()
        #disable start button
        self.bStart.config(state = g.DISABLED)
        #enable pause and stop buttons
        self.bPause.config(state=g.ACTIVE)
        self.bStop.config(state=g.ACTIVE)
    def stop(self):
        #reset stats
        #self.timeElapsed=0
        #self.timeLeft=0
        #self.difftext=0
        #self.totalwords=0
        
        #stop timer if it's running
        if(self.tstate):
            self.tstate=False
        
        #if music is on, stop it.
        if(self.music):
            subprocess.call(["mocp", "--pause"])
            self.music=False

        #update button states
        self.bPause.config(state=g.DISABLED)
        self.bStop.config(state=g.DISABLED)
        self.bStart.config(state=g.ACTIVE)

    def pause(self):
        #depends on state
        if(self.paused):
            #unpause
            
            if(not self.tstate):
                self.tstate=True
                self.count()
            self.paused=False

        else:
            #pause
            if(self.tstate):
                self.tstate=False
            if(self.music):
                subprocess.call(["mocp","--pause"])
                self.music=False
            self.paused=True


    def settings(self):
        self.minutes=int(self.iMinutes.get().strip())
        self.words=int(self.iTargetWords.get().strip())
        # debug print("Minuten: \""+str(self.minutes)+"\", woorden:\""+str(self.words)+"\"")
    def clipboard(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.txt.get(0.0,g.END))

root = g.Tk()
writeorelse= WriteOrElse(root)
root.mainloop()
root.destroy()
