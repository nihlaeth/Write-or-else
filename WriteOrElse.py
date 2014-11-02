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
        
        self.words=500
        self.minutes=20
        self.paused = False
        self.timeElapsed = 0
        self.timeLeft = 0

        #button bar
        self.fBar=g.Frame(master, bd=1)
        self.fBar.grid(row=1,column=1, columnspan=30, sticky=g.W)

        self.bpause = g.Button(self.fBar, text="Pause", command=self.pause)
        self.bpause.grid(row=1, column=1)
        self.bstart = g.Button(self.fBar, text="Start", command=self.start)
        self.bstart.grid(row=1, column=2)
        self.bstop = g.Button(self.fBar, text="Stop", command = self.stop)
        self.bstop.grid(row=1 column=3)
        self.bquit = g.Button(self.fBar, text="Exit", command=self.master.quit)
        self.bquit.grid(row=1, column=4)
        
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

        self.lWords = g.Label(self.fStats, text="Words:", font=self.lFont)
        self.lWords.grid(row=1, column=1)
        self.lWordsV = g.Label(self.fStats, text="0", font=self.lFont)
        self.lWordsV.grid(row=2, column=1)

        self.lTime = g.Label(self.fStats, text="Time left:", font=self.lFont)
        self.lTime.grid(row=1, column=2)
        self.lTimeV = g.Label(self.fStats, text="00:00:00", font=self.lFont)
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




    def punish(self):
        #stop music
        subprocess.call(["mocp", "--pause"])
    def reward(self):
        #start music
        subprocess.call(["mocp", "--unpause"])
    def start(self):
        pass
    def stop(self):
        pass
    def pause(self):
        pass
    def settings(self):
        self.minutes=int(self.iMinutes.get().strip())
        self.words=int(self.iTargetWords.get().strip())
        print("Minuten: \""+str(self.minutes)+"\", woorden:\""+str(self.words)+"\"")

root = g.Tk()
writeorelse= WriteOrElse(root)
root.mainloop()
root.destroy()
