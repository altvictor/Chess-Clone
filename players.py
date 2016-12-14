from tkinter import *


class Player(Frame):

    def __init__(self, frame, name, isWhite):
        # initialize the grid
        Frame.__init__(self)
        self.grid()

        # get the nested frame
        self._frame = frame
        self._frame.grid()

        # get the player color
        self._isWhite = isWhite

        # player name
        self._nameVar = StringVar()
        self._nameVar.set(name)
        self._nameEntry = Entry(self._frame, textvariable=self._nameVar)
        self._nameEntry.grid(row=0, column=0)

        # options for the player's mode
        self._isHuman = -1
        self._humanButton = Button(self._frame, text="Human", command=self.makeHuman)
        self._aiButton = Button(self._frame, text="A.I.", command=self.makeAI)
        self._humanButton.grid(row=0, column=1)
        self._aiButton.grid(row=0, column=2)

    def getName(self):
        # return the player's name
        return self._nameVar.get()

    def isHuman(self):
        # return True if the player is human and not an A.I.
        return self._isHuman

    def isWhite(self):
        # return True if the player is on the white side
        return self._isWhite

    def makeHuman(self):
        # set the player mode to human
        self._isHuman = True
        self._humanButton["state"] = DISABLED
        self._aiButton["state"] = NORMAL

    def makeAI(self):
        # set the player mode to A.I.
        self._isHuman = False
        self._humanButton["state"] = NORMAL
        self._aiButton["state"] = DISABLED

    def disable(self):
        # disable the buttons in the frame
        self._nameEntry["state"] = DISABLED
        self._humanButton["state"] = DISABLED
        self._aiButton["state"] = DISABLED
