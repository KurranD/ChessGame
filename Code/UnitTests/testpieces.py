import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.piece_factory import PieceFactory

class TestPieceMethods(unittest.TestCase):
    def test_createPiecesProperly(self):
        factory = PieceFactory()
        pieces = ['pawn', 'rook', 'bishop', 'knight', 'queen', 'king']
        # Loop through all of the piece types to make sure the factory creates the pieces properly.
        for piece in pieces:
            self.assertEqual(piece, factory.create_piece(piece, 'black', 0, 0).piece_type())

    def test_createNonExistantPiece(self):
        factory = PieceFactory()
        self.assertRaises(ValueError, lambda: factory.create_piece('p4wn', 'black', 0, 0))

    def test_createNonSupportedColour(self):
        factory = PieceFactory()
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'yellow', 0, 0))

    def test_createPieceOutOfBounds(self):
        factory = PieceFactory()
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', -1, 5))
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', 12, 5))
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', 2, -5))
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', 6, 15))

if __name__ == '__main__':
    unittest.main()