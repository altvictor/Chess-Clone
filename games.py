from tkinter import *
from boards import Board
from players import Player


class Game(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.master.title("Chess")
        self.grid()

        self._loginGrid1 = Frame(self)
        self._loginGrid1.grid(row=0, column=0)
        self._player1 = Player(self._loginGrid1, "Player 1", True)

        self._loginGrid2 = Frame(self)
        self._loginGrid2.grid(row=1, column=0)
        self._player2 = Player(self._loginGrid2, "Player 2", False)

        self._login = Button(self, text="Login", command=self.checkLogin)
        self._login.grid(row=0, column=1)
        self._statusVar = StringVar()
        self._statusLabel = Label(self, textvariable=self._statusVar)
        self._statusLabel.grid(row=1, column=1)

        self._boardGrid = Frame(self)
        self._boardGrid.grid(row=2, column=0)
        self._board = Board(self._boardGrid)
        for child in self._boardGrid.winfo_children():
            child.configure(state=DISABLED)

    def checkLogin(self):
        if self._player1.isHuman() == -1 or self._player2.isHuman() == -1:
            self._statusVar.set("Select the player mode")
            return False
        else:
            self._player1.disable()
            self._player2.disable()
            self._login["state"] = DISABLED
            for child in self._boardGrid.winfo_children():
                child.configure(state=NORMAL)
            p1 = self._player1.isHuman()
            p2 = self._player2.isHuman()
            self._board.updatePlayers((p1, self._player1.getName()), (p2, self._player2.getName()))
            self._board.checkAImove()
            return True

