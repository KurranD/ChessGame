import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.board import Board
from Classes.player import Player
from Classes.piece_factory import PieceFactory

class TestBoardMethods(unittest.TestCase):
    def test_createBoardProperly(self):
        first_player = Player('white', self.helper_createCorrectPieces())
        second_player = Player('black', self.helper_createCorrectPieces())
        board_pos = self.helper_createBoard()
        testBoard = Board(board_pos, first_player, second_player)
        self.assertIsNotNone(testBoard)

    def test_createBoardWithIdenticalPlayerColours(self):
        first_player = Player('white', self.helper_createCorrectPieces())
        second_player = Player('white', self.helper_createCorrectPieces())
        board_pos = self.helper_createBoard()
        self.assertRaises(ValueError, lambda: Board(board_pos, first_player, second_player))
        self.assertRaises(ValueError, lambda: Board(board_pos, first_player, first_player))

    def test_createBoardWithBadInputForBoardPositions(self):
        first_player = Player('white', self.helper_createCorrectPieces())
        second_player = Player('black', self.helper_createCorrectPieces())
        board_pos = self.helper_createBoard() + self.helper_createBoard()
        self.assertRaises(ValueError, lambda: Board(board_pos, first_player, second_player))
        board_pos = [ ['a']*8 for i in range(8)]
        self.assertRaises(ValueError, lambda: Board(board_pos, first_player, second_player))
        

    def helper_createBoard(self):
        board = [ [0]*8 for i in range(8)]
        x_coord = 60
        y_coord = 55
        for y in range(0, 8):
            for x in range(0, 8):
                board[x][y] = (x_coord, y_coord)
                x_coord += 75
            y_coord += 75
            x_coord = 60
        return board

    def helper_createCorrectPieces(self):
        factory = PieceFactory()
        pieces_to_create = ['rook', 'bishop', 'knight', 'queen', 'king', 'knight', 'bishop', 'rook']
        pieces = []
        for pawn_counter in range(0, 8):
            pieces.append(factory.create_piece('pawn', 'black', 6, pawn_counter))

        other_piece_counter = 0
        for piece in pieces_to_create:
            pieces.append(factory.create_piece(piece, 'black', 7, other_piece_counter))
            other_piece_counter += 1
        
        for piece in pieces:
            piece.init_piece()
        
        return pieces

if __name__ == '__main__':
    unittest.main()