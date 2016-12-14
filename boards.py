from tkinter import *
from pieces import Piece, King, PIECES
from random import randint
from time import sleep


class Board(Frame):

    def __init__(self, frame):
        # initialize the frame
        Frame.__init__(self)
        self.grid()

        # get the nested frame
        self._grids = frame
        self._grids.grid()

        # import the necessary images
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
        # array of the type of pieces both sides can have
        self._wpiece = [self._wk, self._wq, self._wb, self._wn, self._wr, self._wp]
        self._bpiece = [self._bk, self._bq, self._bb, self._bn, self._br, self._bp]
        # array of dead pieces both for both sides
        self._wdead = []
        self._bdead = []

        self._pressed = False                               # if the user has selected a piece or not
        self._turn = True                                   # if it is the white side's turn
        self._location = 0                                  # location of the piece the user has selected
        self._player1 = (True, "Player 1")                  # information about player 1 (mode/name)
        self._player2 = (True, "Player 2")                  # information about player 2 (mode/name)

        # initialize the 8x8 chess board
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

        # alive pieces for both sides
        self._wpieces = []
        self._bpieces = []
        # initialize the pieces for both players
        self.resetPieces()
        # update the chess board
        self.redraw()

    def press(self, row, column):
        # when the user has selected a button

        # if the user has already selected a piece
        if self._pressed:
            # move to the location
            self.moveTo(self._location, (row, column))

            # reset all the buttons
            for x in range(len(self._spaces)):
                self._spaces[x]["state"] = NORMAL
            self._pressed = False
            # check if it is the A.I.'s turn
            self.checkAImove()
        else:
            # store the location the user has selected
            self._location = (row, column)
            piece = self.find((row, column))
            # if the location has a piece
            if piece is not None:
                if (piece.isWhite() and self._turn) or (not piece.isWhite() and not self._turn):
                    # disable the places the piece cannot go
                    for x in range(len(self._spaces)):
                        self._spaces[x]["state"] = DISABLED
                    # enable the places the piece can go
                    possible = piece.checkValid(self)
                    self._spaces[row*8+column]["state"] = NORMAL
                    for x in range(len(possible)):
                        (a, b) = possible[x]
                        self._spaces[a*8+b]["state"] = NORMAL
                    self._pressed = True

    def resetPieces(self):
        # give the players their pieces
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
        # draw the board with the current information

        # clear the images on the board
        for a in range(len(self._spaces)):
            self._spaces[a]["image"] = self._blank
        # draw the white pieces
        for a in range(len(self._wpieces)):
            (x, y) = self._wpieces[a].getLocation()
            image = self._wpieces[a].getPiece()
            self._spaces[x*8+y]["image"] = self._wpiece[image]
        # draw the black pieces
        for b in range(len(self._bpieces)):
            (x, y) = self._bpieces[b].getLocation()
            image = self._bpieces[b].getPiece()
            self._spaces[x*8+y]["image"] = self._bpiece[image]

    def find(self, location):
        # find the piece at the location
        for a in range(len(self._wpieces)):
            if location == self._wpieces[a].getLocation():
                return self._wpieces[a]
        for b in range(len(self._bpieces)):
            if location == self._bpieces[b].getLocation():
                return self._bpieces[b]

    def getWPieces(self):
        # return the array of the pieces on the white side
        return self._wpieces

    def getBPieces(self):
        # return the array of the pieces on the black side
        return self._bpieces

    def moveTo(self, location1, location2):
        # move a piece from on location to another
        (a, b) = location1
        (c, d) = location2
        piece1 = self.find(location1)
        piece2 = self.find(location2)

        # if the player has not deselect a piece
        if piece1 != piece2 and type(piece2) != King:
            # move the image of the piece
            self._spaces[c * 8 + d]["image"] = self._spaces[a * 8 + b]["image"]
            image = self._spaces[a * 8 + b]["image"]
            self._spaces[a * 8 + b]["image"] = self._blank
            # if a piece is eating another piece
            if piece2 is not None:
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

            # move the piece's location
            piece1.setLocation(location2)

            # get the name of the player
            if piece1.isWhite():
                name = self._player1[1]
            else:
                name = self._player2[1]

            # check if the king is in check
            if self.checkCheck():
                print(name + " is in check")
                self.undo(location1, location2, image)
                return

            # log the move
            rank = piece1.getPiece()
            print(name + " has moved " + PIECES[rank] + " from " + str((a, b)) + " to " + str((c, d)))
            # check for checkmate
            self.checkCheckmate()
            # switch turns
            self._turn = not self._turn

    def updatePlayers(self, p1, p2):
        # update the players
        self._player1 = p1
        self._player2 = p2

    def AImove(self, team, opp):
        # how the A.I. moves

        # check for eating another piece
        priority = []
        for piece in team:
            possible = piece.checkValid(self)
            for moves in possible:
                for enemies in opp:
                    if moves == enemies.getLocation():
                        priority.append((enemies.getPiece(), piece.getLocation(), moves))
        # select the most important piece to eat
        if len(priority) > 0:
            priority.sort()
            (rank, piece1, piece2) = priority[0]
            self.moveTo(piece1, piece2)
        else:
            # move the a random valid location
            move = 0
            piece = 0
            while not move:
                piece = team[randint(0, len(team)-1)]
                moves = piece.checkValid(self)
                if moves:
                    move = moves[randint(0, len(moves)-1)]
            self.moveTo(piece.getLocation(), move)
        # pause and update the board
        sleep(1)
        self._grids.update()
        # check if the next move is the A.I.'s
        self.checkAImove()

    def checkAImove(self):
        # check if it is the A.I.'s turn
        if self._turn:
            if not self._player1[0]:
                self.AImove(self._wpieces, self._bpieces)
        else:
            if not self._player2[0]:
                self.AImove(self._bpieces, self._wpieces)

    def checkCheck(self):
        # check if a king is in check
        king = 0
        if self._turn:
            for piece in self._wpieces:
                if type(piece) == King:
                    king = piece
                    break
        else:
            for piece in self._bpieces:
                if type(piece) == King:
                    king = piece
                    break
        if king.check(self, self._bpieces):
            return True
        else:
            return False

    def checkCheckmate(self):
        # check if there is a checkmate
        wking = 0
        bking = 0
        for piece in self._wpieces:
            if piece.getPiece() == 0:
                wking = piece
                break
        for piece in self._bpieces:
            if piece.getPiece() == 0:
                bking = piece
                break
        if wking.checkmate(self, self._bpieces):
            print(self._player2[1] + " has won!")
            return True
        elif bking.checkmate(self, self._wpieces):
            print(self._player1[1] + " has won!")
            return True
        else:
            return False

    def undo(self, location1, location2, image):
        # undo the most recent move
        (a, b) = location1
        (c, d) = location2
        if self._turn:
            lastdead = self._bdead[-1]
        else:
            lastdead = self._wdead[-1]
        piece = self.find(location2)
        if lastdead.getLocation() == location2:
            piece.setLocation(location1)
            self._spaces[a*8+b]["image"] = self._spaces[c*8+d]["image"]
            self._spaces[c*8+d]["image"] = image
            if self._turn:
                self._bpieces.append(self._bdead.pop())
            else:
                self._wpieces.append(self._wdead.pop())


