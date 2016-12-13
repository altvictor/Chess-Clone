from tkinter import *


class Login(Frame):

    def __init__(self, frame):
        Frame.__init__(self)
        self.grid()

        self._frame = frame
        self._frame.grid()

        self._p1nameVar = StringVar()
        self._p1nameVar.set("Player 1")
        self._p2nameVar = StringVar()
        self._p2nameVar.set("Player 2")
        self._p1nameEntry = Entry(self._frame, textvariable=self._p1nameVar)
        self._p2nameEntry = Entry(self._frame, textvariable=self._p2nameVar)
        self._p1nameEntry.grid(row=0, column=0)
        self._p2nameEntry.grid(row=1, column=0)

