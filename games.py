from tkinter import *


class Game(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.master.title("Chess")

        self._loginGrid = Frame(self)

        self._p1nameVar = StringVar()
        self._p2nameVar = StringVar()
        self._p1nameEntry = Entry(self, textvariable=self._p1nameVar)
        self._p2nameEntry = Entry(self, textvariable=self._p2nameVar)


