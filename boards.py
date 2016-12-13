from tkinter import *
from pieces import Piece, King, PIECES
from random import randint


class Board(Frame):

    def __init__(self, frame):
        Frame.__init__(self)
        self.grid()

        self._grids = frame
        self._grids.grid()

        self._blank = PhotoImage(file="images/blank.gif")
        self._wp = PhotoImage(file="images/wp.gif")
        self._wr = PhotoImage(file="images/wr.gif")
        self._wn = PhotoImage(file="images/wn.gif")
        self._wb = PhotoImage(file="images/wb.gif")
        self._wq = PhotoImage(file="images/wq.gif")
        self._wk = PhotoImage(file="images/wk.gif")
        self._bp = PhotoImage(file="images/bp.gif")
        self._br = PhotoImage(file="images/br.gif")
        self._bn = PhotoImage(file="images/bn.gif")
        self._bb = PhotoImage(file="images/bb.gif")
        self._bq = PhotoImage(file="images/bq.gif")
        self._bk = PhotoImage(file="images/bk.gif")
        self._wpiece = [self._wk, self._wq, self._wb, self._wn, self._wr, self._wp]
        self._bpiece = [self._bk, self._bq, self._bb, self._bn, self._br, self._bp]
        self._wdead = []
        self._bdead = []

        self._pressed = False
        self._turn = True
        self._location = 0
        self._player1 = (True, "Player 1")
        self._player2 = (True, "Player 2")

        self._spaces = []
        for y in range(8):
            for x in range(8):
                if y % 2 == 0:
                    if x % 2 == 0:
                        self._spaces.append(Button(self._grids, image=self._blank, height=50, width=50,
                                                   command=lambda a=y, b=x: self.press(a, b)))
                    else:
                        self._spaces.append(Button(self._grids, image=self._blank, height=50, width=50,
                                                   command=lambda a=y, b=x: self.press(a, b)))
                else:
                    if x % 2 == 0:
                        self._spaces.append(Button(self._grids, image=self._blank, height=50, width=50,
                                                   command=lambda a=y, b=x: self.press(a, b)))
                    else:
                        self._spaces.append(Button(self._grids, image=self._blank, height=50, width=50,
                                                   command=lambda a=y, b=x: self.press(a, b)))
                self._spaces[-1].grid(row=y, column=x)

        self._wpieces = []
        self._bpieces = []
        self.resetPieces()
        self.redraw()

    def press(self, row, column):
        if self._pressed:
            self.moveTo(self._location, (row, column))

            for x in range(len(self._spaces)):
                self._spaces[x]["state"] = NORMAL
            self._pressed = False
            self.checkAImove()
        else:
            self._location = (row, column)
            piece = self.find((row, column))
            if piece is not None:
                if (piece.isWhite() and self._turn) or (not piece.isWhite() and not self._turn):
                    for x in range(len(self._spaces)):
                        self._spaces[x]["state"] = DISABLED
                    possible = piece.checkValid(self)
                    self._spaces[row*8+column]["state"] = NORMAL
                    for x in range(len(possible)):
                        (a, b) = possible[x]
                        self._spaces[a*8+b]["state"] = NORMAL
                    self._pressed = True

    def resetPieces(self):
        self._wpieces.clear()
        self._bpieces.clear()
        self._bpieces.append(Piece(False, (0, 0), 4))
        self._bpieces.append(Piece(False, (0, 1), 3))
        self._bpieces.append(Piece(False, (0, 2), 2))
        self._bpieces.append(Piece(False, (0, 3), 1))
        self._bpieces.append(King(False, (0, 4)))
        self._bpieces.append(Piece(False, (0, 5), 2))
        self._bpieces.append(Piece(False, (0, 6), 3))
        self._bpieces.append(Piece(False, (0, 7), 4))
        self._bpieces.append(Piece(False, (1, 0), 5))
        self._bpieces.append(Piece(False, (1, 1), 5))
        self._bpieces.append(Piece(False, (1, 2), 5))
        self._bpieces.append(Piece(False, (1, 3), 5))
        self._bpieces.append(Piece(False, (1, 4), 5))
        self._bpieces.append(Piece(False, (1, 5), 5))
        self._bpieces.append(Piece(False, (1, 6), 5))
        self._bpieces.append(Piece(False, (1, 7), 5))
        self._wpieces.append(Piece(True, (6, 0), 5))
        self._wpieces.append(Piece(True, (6, 1), 5))
        self._wpieces.append(Piece(True, (6, 2), 5))
        self._wpieces.append(Piece(True, (6, 3), 5))
        self._wpieces.append(Piece(True, (6, 4), 5))
        self._wpieces.append(Piece(True, (6, 5), 5))
        self._wpieces.append(Piece(True, (6, 6), 5))
        self._wpieces.append(Piece(True, (6, 7), 5))
        self._wpieces.append(Piece(True, (7, 0), 4))
        self._wpieces.append(Piece(True, (7, 1), 3))
        self._wpieces.append(Piece(True, (7, 2), 2))
        self._wpieces.append(Piece(True, (7, 3), 1))
        self._wpieces.append(King(True, (7, 4)))
        self._wpieces.append(Piece(True, (7, 5), 2))
        self._wpieces.append(Piece(True, (7, 6), 3))
        self._wpieces.append(Piece(True, (7, 7), 4))

    def redraw(self):
        for a in range(len(self._spaces)):
            self._spaces[a]["image"] = self._blank
        for a in range(len(self._wpieces)):
            (x, y) = self._wpieces[a].getLocation()
            image = self._wpieces[a].getPiece()
            self._spaces[x*8+y]["image"] = self._wpiece[image]
        for b in range(len(self._bpieces)):
            (x, y) = self._bpieces[b].getLocation()
            image = self._bpieces[b].getPiece()
            self._spaces[x*8+y]["image"] = self._bpiece[image]

    def find(self, location):
        for a in range(len(self._wpieces)):
            if location == self._wpieces[a].getLocation():
                return self._wpieces[a]
        for b in range(len(self._bpieces)):
            if location == self._bpieces[b].getLocation():
                return self._bpieces[b]

    def getWPieces(self):
        return self._wpieces

    def getBPieces(self):
        return self._bpieces

    def moveTo(self, location1, location2):
        (a, b) = location1
        (c, d) = location2
        piece1 = self.find(location1)
        piece2 = self.find(location2)

        if piece1 != piece2:
            if piece2 is None:
                image = self._spaces[c*8+d]["image"]
                self._spaces[c*8+d]["image"] = self._spaces[a*8+b]["image"]
                self._spaces[a*8+b]["image"] = image
            else:
                self._spaces[c*8+d]["image"] = self._spaces[a*8+b]["image"]
                self._spaces[a*8+b]["image"] = self._blank
                if piece2.isWhite():
                    for x in range(len(self._wpieces)):
                        if self._wpieces[x] == piece2:
                            self._wdead.append(self._wpieces.pop(x))
                            break
                else:
                    for x in range(len(self._bpieces)):
                        if self._bpieces[x] == piece2:
                            self._bdead.append(self._bpieces.pop(x))
                            break

            piece1.setLocation(location2)
            self._turn = not self._turn

            # print result
            if piece1.isWhite():
                name = self._player1[1]
                rank = piece1.getPiece()
            else:
                name = self._player2[1]
                rank = piece2.getPiece()
            print(name + " has moved " + PIECES[rank] + " from " + str((a, b)) + " to " + str((c, d)))

    def updatePlayers(self, p1, p2):
        self._player1 = p1
        self._player2 = p2

    def AImove(self, team, opp):
        # check for eating
        priority = []
        for piece in team:
            possible = piece.checkValid(self)
            for moves in possible:
                for enemies in opp:
                    if moves == enemies.getLocation():
                        priority.append((enemies.getPiece(), piece.getLocation(), moves))

        if len(priority) > 0:
            priority.sort()
            (rank, piece1, piece2) = priority[0]
            self.moveTo(piece1, piece2)
        else:
            move = 0
            piece = 0
            while not move:
                piece = team[randint(0, len(team)-1)]
                moves = piece.checkValid(self)
                if moves:
                    move = moves[randint(0, len(moves)-1)]
            self.moveTo(piece.getLocation(), move)
        self.checkAImove()

    def checkAImove(self):
        if self._turn:
            if not self._player1[0]:
                self.AImove(self._wpieces, self._bpieces)
        else:
            if not self._player2[0]:
                self.AImove(self._bpieces, self._wpieces)
