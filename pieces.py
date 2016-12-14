PIECES = {0: "King", 1: "Queen", 2: "Bishop", 3: "Knight", 4: "Rook", 5: "Pawn"}


class Piece:

    def __init__(self, isWhite, location, pieceType):
        # initialize the piece's information
        self._isWhite = isWhite                                 # is the piece on the white side
        self._location = location                               # the location of the piece (row, column)
        self._type = pieceType                                  # the type/rank of piece it is
        self._moved = False                                     # if the piece has moved or not

        # array of function to select the appropriate type of move
        self._move = [self.king, self.queen, self.bishop, self.knight, self.rook, self.pawn]

    def __str__(self):
        # print the piece's location and type/rank
        string = "[" + str(self._location) + "|" + PIECES[self._type] + "]"
        return string

    def isWhite(self):
        # return True if the piece is white
        return self._isWhite

    def getLocation(self):
        # return the piece's location
        return self._location

    def getPiece(self):
        # return the piece's type/rank
        return self._type

    def setLocation(self, location):
        # move the piece
        self._location = location
        self._moved = True

    def checkValid(self, board):
        # check for the piece's valid moves and return them
        moves = self._move[self._type](board)
        impossible = self.getImpossible(board, moves)
        return self.getPossible(moves, impossible)

    def getImpossible(self, board, moves):
        # get where the piece cannot move
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
        # get the final valid possible moves
        possible = moves[:]
        destroy = []
        # remove the places where the pieces cannot move to
        for a in range(len(possible)):
            for b in range(len(impossible)):
                if possible[a] == impossible[b]:
                    destroy.append(possible[a])
        destroy = list(set(destroy))
        for item in destroy:
            possible.remove(item)
        return possible

    def king(self, board):
        # the possible moves for the king
        moves = []
        (x, y) = self._location
        # check one square around the king
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
        # the possible moves for the king
        moves = []
        (x, y) = self._location
        # horizontal and vertical
        for a in range(7):
            moves.append((x, a))
            moves.append((a, y))
        # the four diagonals
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
        # the possible moves for the bishop
        moves = []
        (x, y) = self._location
        # the four diagonals
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
        # the possible moves for the knight
        moves = []
        (x, y) = self._location
        # moves in a L-shape
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
        # the possible moves for the rook
        moves = []
        (x, y) = self._location
        # horizontal and vertical
        for a in range(7):
            moves.append((x, a))
            moves.append((a, y))
        return moves

    def pawn(self, board):
        # the possible moves for the pawn
        moves = []
        (x, y) = self._location
        # white pawn's direction
        if self._isWhite:
            # check if the pawn can move two spaces
            if not self._moved:
                moves.append((x-2, y))
            if x >= 1:
                moves.append((x-1, y))
            # check to eat diagonally
            pieces = board.getBPieces()
            for a in range(len(pieces)):
                if pieces[a].getLocation() == (x-1, y-1):
                    moves.append((x-1, y-1))
                if pieces[a].getLocation() == (x-1, y+1):
                    moves.append((x-1, y+1))
        # black pawn's direction
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
        # check if the piece gets blocked diagonally
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
        # check if the piece gets blocked horizontally or vertically
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
        # initialize the king
        Piece.__init__(self, isWhite, location, 0)

    def check(self, board, pieces):
        # check if it is in check
        for a in range(len(pieces)):
            moves = pieces[a].checkValid(board)
            for b in range(len(moves)):
                if moves[b] == Piece.getLocation(self):
                    return True
        return False

    def checkmate(self, board, pieces):
        # check if it is in checkmate
        if not self.check(board, pieces):
            return False
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
