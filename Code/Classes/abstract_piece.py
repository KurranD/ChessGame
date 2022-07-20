from abc import abstractmethod
import pygame
import os

class Piece():
    def __init__(self, colour, boardpos):
        self.colour = colour
        self.boardx = boardpos[0]
        self.boardy = boardpos[1]
        self.moved = False
        self.button = None

    @abstractmethod
    def initButton(self):
        pass

    @abstractmethod
    def pieceType(self):
        pass

    @abstractmethod
    def possible_moves(self):
        pass

    @abstractmethod
    def possible_attack_moves(self):
        pass

    def piece_clicked(self):
        return self.button.click()

    def get_colour(self):
        return self.colour

    def move(self, board_pos):
        self.boardx = board_pos[0]
        self.boardy = board_pos[1]

    def set_button(self, button):
        self.button = button

    def get_button(self):
        return self.button

    def draw(self, screen):
        self.button.draw(screen)

    def get_board_index(self):
        return (self.boardx, self.boardy)

class Pawn(Piece):
    def initButton(self):
        self.image = 'Images/pawn.png' if self.colour == 'white' else 'Images/pawn_b.png'

    def pieceType(self):
        return 'pawn'

    def get_image(self):
        return self.image

    def has_moved(self):
        if(self.moved):
            return True
        else:
            return False

    def move(self, board_pos):
        self.moved = True
        Piece.move(self, board_pos)

    def possible_moves(self):
        possibleMoves = []
        yoffset = 1 if self.colour == 'black' else -1
        possibleMoves.append((self.boardx, self.boardy+yoffset))
        if(not self.has_moved()):
            possibleMoves.append((self.boardx, self.boardy+yoffset*2))
        return possibleMoves

    def possible_attack_moves(self):
        possibleMoves = []
        yoffset = 1 if self.colour == 'black' else -1
        possibleMoves.append((self.boardx+1, self.boardy+yoffset))
        possibleMoves.append((self.boardx-1, self.boardy+yoffset))
        return possibleMoves

class Rook(Piece):
    def initButton(self):
        self.image = 'Images/rook.png' if self.colour == 'white' else 'Images/rook_b.png'

    def pieceType(self):
        return 'rook'

    def get_image(self):
        return self.image

    def has_moved(self):
        if(self.moved):
            return True
        else:
            return False

    def move(self, board_pos):
        self.moved = True
        Piece.move(self, board_pos)

    def __moves_helper(self):
        possibleMoves = []
        for i in range(1, 7):
            possibleMoves.append((self.boardx, self.boardy+i))
            possibleMoves.append((self.boardx, self.boardy-i))
            possibleMoves.append((self.boardx+i, self.boardy))
            possibleMoves.append((self.boardx-i, self.boardy))
        return possibleMoves

    def possible_moves(self):
        return self.__moves_helper()

    def possible_attack_moves(self):
        return self.__moves_helper()

class Bishop(Piece):
    def initButton(self):
        self.image = 'Images/bishop.png' if self.colour == 'white' else 'Images/bishop_b.png'

    def pieceType(self):
        return 'bishop'

    def get_image(self):
        return self.image

    def move(self, board_pos):
        self.moved = True
        Piece.move(self, board_pos)

    def __moves_helper(self):
        possibleMoves = []
        for i in range(1, 7):
            possibleMoves.append((self.boardx+i, self.boardy+i))
            possibleMoves.append((self.boardx+i, self.boardy-i))
            possibleMoves.append((self.boardx-i, self.boardy+i))
            possibleMoves.append((self.boardx-i, self.boardy-i))
        return possibleMoves

    def possible_moves(self):
        return self.__moves_helper()

    def possible_attack_moves(self):
        return self.__moves_helper()

class Knight(Piece):
    def initButton(self):
        self.image = 'Images/knight.png' if self.colour == 'white' else 'Images/knight_b.png'

    def pieceType(self):
        return 'knight'

    def get_image(self):
        return self.image

    def move(self, board_pos):
        self.moved = True
        Piece.move(self, board_pos)

    def __moves_helper(self):
        possibleMoves = []
        possibleMoves.append((self.boardx+1, self.boardy+2))
        possibleMoves.append((self.boardx+1, self.boardy-2))
        possibleMoves.append((self.boardx-1, self.boardy+2))
        possibleMoves.append((self.boardx-1, self.boardy-2))
        possibleMoves.append((self.boardx+2, self.boardy+1))
        possibleMoves.append((self.boardx+2, self.boardy-1))
        possibleMoves.append((self.boardx-2, self.boardy+1))
        possibleMoves.append((self.boardx-2, self.boardy-1))
        return possibleMoves

    def possible_moves(self):
        return self.__moves_helper()

    def possible_attack_moves(self):
        return self.__moves_helper()

class Queen(Piece):
    def initButton(self):
        self.image = 'Images/queen.png' if self.colour == 'white' else 'Images/queen_b.png'

    def pieceType(self):
        return 'queen'

    def get_image(self):
        return self.image

    def move(self, board_pos):
        self.moved = True
        Piece.move(self, board_pos)

    def __moves_helper(self):
        possibleMoves = []
        for i in range(1, 7):
            possibleMoves.append((self.boardx, self.boardy+i))
            possibleMoves.append((self.boardx, self.boardy-i))
            possibleMoves.append((self.boardx+i, self.boardy))
            possibleMoves.append((self.boardx-i, self.boardy))
            possibleMoves.append((self.boardx+i, self.boardy+i))
            possibleMoves.append((self.boardx+i, self.boardy-i))
            possibleMoves.append((self.boardx-i, self.boardy+i))
            possibleMoves.append((self.boardx-i, self.boardy-i))
        return possibleMoves

    def possible_moves(self):
        return self.__moves_helper()

    def possible_attack_moves(self):
        return self.__moves_helper()

class King(Piece):
    def initButton(self):
        self.image = 'Images/king.png' if self.colour == 'white' else 'Images/king_b.png'

    def pieceType(self):
        return 'king'

    def get_image(self):
        return self.image

    def has_moved(self):
        if(self.moved):
            return True
        else:
            return False

    def move(self, board_pos):
        self.moved = True
        Piece.move(self, board_pos)

    def __moves_helper(self):
        possibleMoves = []
        for i in range(1, 2):
            possibleMoves.append((self.boardx, self.boardy+i))
            possibleMoves.append((self.boardx, self.boardy-i))
            possibleMoves.append((self.boardx+i, self.boardy))
            possibleMoves.append((self.boardx-i, self.boardy))
            possibleMoves.append((self.boardx+i, self.boardy+i))
            possibleMoves.append((self.boardx+i, self.boardy-i))
            possibleMoves.append((self.boardx-i, self.boardy+i))
            possibleMoves.append((self.boardx-i, self.boardy-i))

        return possibleMoves

    def possible_moves(self):
        return self.__moves_helper()

    def possible_attack_moves(self):
        return self.__moves_helper()