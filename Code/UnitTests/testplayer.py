import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.player import Player
from Classes.piece_factory import PieceFactory

class TestPlayerMethods(unittest.TestCase):
    def test_createPlayerWithCorrectValues(self):
        pieces = self.helper_createCorrectPieces()
        self.assertEqual(pieces, Player('white', pieces).get_pieces())
        self.assertEqual(pieces, Player('black', pieces).get_pieces())

    def test_createPlayerWithNonSupportedColour(self):
        pieces = self.helper_createCorrectPieces()
        self.assertRaises(ValueError, lambda: Player('green', pieces))

    def test_addPiecesThatDontFitRequirement(self):
        self.assertRaises(ValueError, lambda: Player('white', []))
        pieces = self.helper_createCorrectPieces() + self.helper_createCorrectPieces()
        self.assertRaises(ValueError, lambda: Player('white', pieces))

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
        
        return pieces

if __name__ == '__main__':
    unittest.main()