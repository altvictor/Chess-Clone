PIECES = {0: "King", 1: "Queen", 2: "Bishop", 3: "Knight", 4: "Rook", 5: "Pawn"}


class Piece:

    def __init__(self, isWhite, location, pieceType):
        self._isWhite = isWhite
        self._location = location
        self._type = pieceType
        self._moved = False

        self._move = [self.king, self.queen, self.bishop, self.knight, self.rook, self.pawn]

    def __str__(self):
        string = "[" + str(self._location) + "|" + PIECES[self._type] + "]"
        return string

    def isWhite(self):
        return self._isWhite

    def getLocation(self):
        return self._location

    def getPiece(self):
        return self._type

    def setLocation(self, location):
        self._location = location
        self._moved = True

    def checkValid(self, board):
        moves = self._move[self._type](board)
        impossible = self.getImpossible(board, moves)
        return self.getPossible(moves, impossible)

    def getImpossible(self, board, moves):
        impossible = []
        # check for own color
        if self._isWhite:
            pieces = board.getWPieces()
        else:
            pieces = board.getBPieces()
        for a in range(len(moves)):
            for b in range(len(pieces)):
                if moves[a] == pieces[b].getLocation():
                    impossible.append(moves[a])
        # check for going through pieces
        if self._type == 1 or self._type == 2:
            impossible += self.diagonalBlock(board)
        if self._type == 1 or self._type == 4:
            impossible += self.parallelBlock(board)
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
                        impossible.append((x-1, y))
                else:
                    if pieces[a].getLocation() == (x+1, y):
                        impossible.append((x+1, y))

        return impossible

    def getPossible(self, moves, impossible):
        possible = moves[:]
        destroy = []
        for a in range(len(possible)):
            for b in range(len(impossible)):
                if possible[a] == impossible[b]:
                    destroy.append(possible[a])
        destroy = list(set(destroy))
        for item in destroy:
            possible.remove(item)
        return possible

    def king(self, board):
        moves = []
        (x, y) = self._location
        if x-1 >= 0 and y-1 >= 0:
            moves.append((x-1, y-1))
        if x-1 >= 0:
            moves.append((x-1, y))
        if x-1 >= 0 and y+1 <= 7:
            moves.append((x-1, y+1))
        if y-1 >= 0:
            moves.append((x, y-1))
        if y+1 <= 7:
            moves.append((x, y+1))
        if x+1 <= 7 and y-1 >= 0:
            moves.append((x+1, y-1))
        if x+1 <= 7:
            moves.append((x+1, y))
        if x+1 <=7 and y <= 1:
            moves.append((x+1, y+1))
        return moves

    def queen(self, board):
        moves = []
        (x, y) = self._location
        for a in range(7):
            moves.append((x, a))
            moves.append((a, y))
        count = 1
        while x-count >= 0 and y-count >= 0:
            moves.append((x-count, y-count))
            count += 1
        count = 1
        while x-count >= 0 and y+count <= 7:
            moves.append((x-count, y+count))
            count += 1
        count = 1
        while x+count <= 7 and y-count >= 0:
            moves.append((x+count, y-count))
            count += 1
        count = 1
        while x+count <= 7 and y+count <= 7:
            moves.append((x+count, y+count))
            count += 1
        return moves

    def bishop(self, board):
        moves = []
        (x, y) = self._location
        count = 1
        while x - count >= 0 and y - count >= 0:
            moves.append((x - count, y - count))
            count += 1
        count = 1
        while x - count >= 0 and y + count <= 7:
            moves.append((x - count, y + count))
            count += 1
        count = 1
        while x + count <= 7 and y - count >= 0:
            moves.append((x + count, y - count))
            count += 1
        count = 1
        while x + count <= 7 and y + count <= 7:
            moves.append((x + count, y + count))
            count += 1
        return moves

    def knight(self, board):
        moves = []
        (x, y) = self._location
        if x >= 2:
            if y >= 1:
                moves.append((x-2, y-1))
            if y <= 6:
                moves.append((x-2, y+1))
        if x <= 5:
            if y >= 1:
                moves.append((x+2, y-1))
            if y <= 6:
                moves.append((x+2, y+1))
        if y >= 2:
            if x >= 1:
                moves.append((x-1, y-2))
            if x <= 6:
                moves.append((x+1, y-2))
        if y <= 5:
            if x >= 1:
                moves.append((x-1, y+2))
            if x <= 6:
                moves.append((x+1, y+2))
        return moves

    def rook(self, board):
        moves = []
        (x, y) = self._location
        for a in range(7):
            moves.append((x, a))
            moves.append((a, y))
        return moves

    def pawn(self, board):
        moves = []
        (x, y) = self._location
        if self._isWhite:
            if not self._moved:
                moves.append((x-2, y))
            if x >= 1:
                moves.append((x-1, y))
            # check to eat
            pieces = board.getBPieces()
            for a in range(len(pieces)):
                if pieces[a].getLocation() == (x-1, y-1):
                    moves.append((x-1, y-1))
                if pieces[a].getLocation() == (x-1, y+1):
                    moves.append((x-1, y+1))
        else:
            if not self._moved:
                moves.append((x+2, y))
            if x <= 6:
                moves.append((x+1, y))
            # check to eat
            pieces = board.getWPieces()
            for a in range(len(pieces)):
                if pieces[a].getLocation() == (x+1, y-1):
                    moves.append((x+1, y-1))
                if pieces[a].getLocation() == (x+1, y+1):
                    moves.append((x+1, y+1))
        return moves

    def diagonalBlock(self, board):
        impossible = []
        (x, y) = self._location
        if self._isWhite:
            pieces1 = board.getBPieces()
            pieces2 = board.getWPieces()
        else:
            pieces1 = board.getWPieces()
            pieces2 = board.getBPieces()

        blocked = False
        count = 1
        while x - count >= 0 and y - count >= 0:
            if blocked:
                impossible.append((x - count, y - count))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x - count, y - count):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x - count, y - count):
                        impossible.append((x - count, y - count))
                        blocked = True
            count += 1
        blocked = False
        count = 1
        while x - count >= 0 and y + count <= 7:
            if blocked:
                impossible.append((x - count, y + count))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x - count, y + count):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x - count, y + count):
                        impossible.append((x - count, y + count))
                        blocked = True
            count += 1
        blocked = False
        count = 1
        while x + count <= 7 and y - count >= 0:
            if blocked:
                impossible.append((x + count, y - count))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x + count, y - count):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x + count, y - count):
                        impossible.append((x + count, y - count))
                        blocked = True
            count += 1
        blocked = False
        count = 1
        while x + count <= 7 and y + count <= 7:
            if blocked:
                impossible.append((x + count, y + count))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x + count, y + count):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x + count, y + count):
                        impossible.append((x + count, y + count))
                        blocked = True
            count += 1
        return impossible

    def parallelBlock(self, board):
        impossible = []
        (x, y) = self._location
        if self._isWhite:
            pieces1 = board.getBPieces()
            pieces2 = board.getWPieces()
        else:
            pieces1 = board.getWPieces()
            pieces2 = board.getBPieces()
        blocked = False
        count = 1
        while x - count >= 0:
            if blocked:
                impossible.append((x - count, y))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x - count, y):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x - count, y):
                        impossible.append((x - count, y))
                        blocked = True
            count += 1
        blocked = False
        count = 1
        while x + count <= 7:
            if blocked:
                impossible.append((x + count, y))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x + count, y):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x + count, y):
                        impossible.append((x + count, y))
                        blocked = True
            count += 1
        blocked = False
        count = 1
        while y - count >= 0:
            if blocked:
                impossible.append((x, y - count))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x, y - count):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x, y - count):
                        impossible.append((x, y - count))
                        blocked = True
            count += 1
        blocked = False
        count = 1
        while y + count <= 7:
            if blocked:
                impossible.append((x, y + count))
            else:
                for piece in pieces1:
                    if piece.getLocation() == (x, y + count):
                        blocked = True
                for piece in pieces2:
                    if piece.getLocation() == (x, y + count):
                        impossible.append((x, y + count))
                        blocked = True
            count += 1
        return impossible


class King(Piece):

    def __init__(self, isWhite, location):
        Piece.__init__(self, isWhite, location, 0)

    def check(self, board, pieces):
        for a in range(len(pieces)):
            moves = pieces[a].checkValid(board)
            for b in range(len(moves)):
                if moves[b] == Piece.getLocation(self):
                    return True
        return False

    def checkmate(self, board, pieces):
        if not self.check(board, pieces):
            return False
        possible = []
        for a in range(len(pieces)):
            moves = pieces[a].checkValid(board)
            for b in range(len(moves)):
                possible = Piece.checkValid(self, board)
                destroy = []
                for c in range(len(possible)):
                    if possible[c] == moves[b]:
                        destroy.append(possible[c])
                destroy = list(set(destroy))
                for item in destroy:
                    possible.remove(item)
                if not possible:
                    return True
        return False
