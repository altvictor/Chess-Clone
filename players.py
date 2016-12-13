from tkinter import *


class Player(Frame):

    def __init__(self, frame, name, isWhite):
        Frame.__init__(self)
        self.grid()

        self._frame = frame
        self._frame.grid()

        self._isWhite = isWhite

        self._nameVar = StringVar()
        self._nameVar.set(name)
        self._nameEntry = Entry(self._frame, textvariable=self._nameVar)
        self._nameEntry.grid(row=0, column=0)

        self._isHuman = -1
        self._humanButton = Button(self._frame, text="Human", command=self.makeHuman)
        self._aiButton = Button(self._frame, text="A.I.", command=self.makeAI)
        self._humanButton.grid(row=0, column=1)
        self._aiButton.grid(row=0, column=2)

    def getName(self):
        return self._nameVar.get()

    def isHuman(self):
        return self._isHuman

    def isWhite(self):
        return self._isWhite

    def makeHuman(self):
        self._isHuman = True
        self._humanButton["state"] = DISABLED
        self._aiButton["state"] = NORMAL

    def makeAI(self):
        self._isHuman = False
        self._humanButton["state"] = NORMAL
        self._aiButton["state"] = DISABLED

    def disable(self):
        self._nameEntry["state"] = DISABLED
        self._humanButton["state"] = DISABLED
        self._aiButton["state"] = DISABLED
