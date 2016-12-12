KING = 0
QUEEN = 1
BISHOP = 2
KNIGHT = 3
ROOK = 4
PAWN = 5


class Piece:

    def __init__(self, isWhite, location, pieceType):
        self._isWhite = isWhite
        self._location = location
        self._type = pieceType
        self._moved = False

        self._moves = []
        self._possible = []
        self._impossible = []

        self._move = [self.king, self.queen, self.bishop, self.knight, self.rook, self.pawn]

    def __str__(self):
        string = "[" + str(self._location) + str(self._type) + "]"
        return string

    def isWhite(self):
        return self._isWhite

    def getLocation(self):
        return self._location

    def getPiece(self):
        return self._type

    def getMoves(self):
        return self._moves

    def getPossible(self):
        return self._possible

    def getImpossible(self):
        return self._impossible

    def setLocation(self, location):
        self._location = location
        self._moved = True

    def checkMoves(self, board):
        # separate
        self._moves.clear()

        self._move[self._type](board)
        self._possible = self._moves[:]
        self._impossible.clear()

        # check for own color
        if self._isWhite:
            pieces = board.getWPieces()
        else:
            pieces = board.getBPieces()
        for a in range(len(self._moves)):
            for b in range(len(pieces)):
                if self._moves[a] == pieces[b].getLocation():
                    self._impossible.append(self._moves[a])
        # check for in front of pawn
        if self._type == 5:
            (x, y) = self._location
            if self._isWhite:
                pieces = board.getBPieces()
            else:
                pieces = board.getWPieces()
            for a in range(len(pieces)):
                if self._isWhite:
                    if pieces[a].getLocation() == (x-1, y):
                        print("test")
                        self._impossible.append((x-1, y))
                else:
                    if pieces[a].getLocation() == (x+1, y):
                        print("test")
                        self._impossible.append((x+1, y))

        destroy = []
        for a in range(len(self._possible)):
            for b in range(len(self._impossible)):
                if self._possible[a] == self._impossible[b]:
                    destroy.append(self._possible.pop(a))
        # subtract arrays?

    def king(self, board):
        (x, y) = self._location
        if x-1 >= 0 and y-1 >= 0:
            self._moves.append((x-1, y-1))
        if x-1 >= 0:
            self._moves.append((x-1, y))
        if x-1 >= 0 and y+1 <= 7:
            self._moves.append((x-1, y+1))
        if y-1 >= 0:
            self._moves.append((x, y-1))
        if y+1 <= 7:
            self._moves.append((x, y+1))
        if x+1 <= 7 and y-1 >= 0:
            self._moves.append((x+1, y-1))
        if x+1 <= 7:
            self._moves.append((x+1, y))
        if x+1 <=7 and y <= 1:
            self._moves.append((x+1, y+1))

    def queen(self, board):
        (x, y) = self._location
        for a in range(7):
            self._moves.append((x, a))
            self._moves.append((a, y))
        count = 1
        while x-count >= 0 and y-count >= 0:
            self._moves.append((x-count, y-count))
            count += 1
        count = 1
        while x-count >= 0 and y+count <= 7:
            self._moves.append((x-count, y+count))
            count += 1
        count = 1
        while x+count <= 7 and y-count >= 0:
            self._moves.append((x+count, y-count))
            count += 1
        count = 1
        while x+count <= 7 and y+count <= 7:
            self._moves.append((x+count, y+count))
            count += 1

    def bishop(self, board):
        (x, y) = self._location
        count = 1
        while x - count >= 0 and y - count >= 0:
            self._moves.append((x - count, y - count))
            count += 1
        count = 1
        while x - count >= 0 and y + count <= 7:
            self._moves.append((x - count, y + count))
            count += 1
        count = 1
        while x + count <= 7 and y - count >= 0:
            self._moves.append((x + count, y - count))
            count += 1
        count = 1
        while x + count <= 7 and y + count <= 7:
            self._moves.append((x + count, y + count))
            count += 1

    def knight(self, board):
        (x, y) = self._location
        if x >= 2:
            if y >= 1:
                self._moves.append((x-2, y-1))
            if y <= 6:
                self._moves.append((x-2, y+1))
        if x <= 5:
            if y >= 1:
                self._moves.append((x+2, y-1))
            if y <= 6:
                self._moves.append((x+2, y+1))
        if y >= 2:
            if x >= 1:
                self._moves.append((x-1, y-2))
            if x <= 6:
                self._moves.append((x+1, y-2))
        if y <= 5:
            if x >= 1:
                self._moves.append((x-1, y+2))
            if x <= 6:
                self._moves.append((x+1, y+2))

    def rook(self, board):
        (x, y) = self._location
        for a in range(7):
            self._moves.append((x, a))
            self._moves.append((a, y))

    def pawn(self, board):
        (x, y) = self._location
        if self._isWhite:
            if not self._moved:
                self._moves.append((x-2, y))
            if x >= 1:
                self._moves.append((x-1, y))
            pieces = board.getBPieces()
            for x in range(len(pieces)):
                if pieces[x].getLocation == (x-1, y-1):
                    self._moves.append((x-1, y-1))
                if pieces[x].getLocation == (x-1, y+1):
                    self._moves.append((x-1, y+1))
        else:
            if not self._moved:
                self._moves.append((x+2, y))
            if x <= 6:
                self._moves.append((x+1, y))
            pieces = board.getWPieces()
            for x in range(len(pieces)):
                if pieces[x].getLocation == (x+1, y-1):
                    self._moves.append((x+1, y-1))
                if pieces[x].getLocation == (x+1, y+1):
                    self._moves.append((x+1, y+1))


class King(Piece):

    def __init__(self, isWhite, location):
        Piece.__init__(self, isWhite, location, 0)

    def check(self, pieces):
        for a in range(len(pieces)):
            moves = pieces[a].getPossible()
            for b in range(len(moves)):
                if moves[b] == Piece.getLocation():
                    return True
        return False

    def checkmate(self, pieces):
        if not self.check(pieces):
            return False
        possible = []
        for a in range(len(pieces)):
            moves = pieces[a].getPossible()
            for b in range(len(moves)):
                possible = Piece.getPossible(self)
                for c in range(len(possible)):
                    if possible[c] == moves[b]:
                        possible.pop(c)
        if not possible:
            return True
        else:
            return False
