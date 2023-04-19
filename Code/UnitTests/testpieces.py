import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.piece_factory import PieceFactory

class TestPieceMethods(unittest.TestCase):
    def test_create_pieces_properly(self):
        factory = PieceFactory()
        pieces = ['pawn', 'rook', 'bishop', 'knight', 'queen', 'king']
        # Loop through all of the piece types to make sure the factory creates the pieces properly.
        for piece in pieces:
            self.assertEqual(piece, factory.create_piece(piece, 'black', 0, 0).get_piece_type())

    def test_create_non_existant_piece(self):
        factory = PieceFactory()
        self.assertRaises(ValueError, lambda: factory.create_piece('p4wn', 'black', 0, 0))

    def test_create_non_supported_colour(self):
        factory = PieceFactory()
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'yellow', 0, 0))

    def test_create_piece_out_of_bounds(self):
        factory = PieceFactory()
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', -1, 5))
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', 12, 5))
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', 2, -5))
        self.assertRaises(ValueError, lambda: factory.create_piece('pawn', 'white', 6, 15))

    def test_pieces_get_white_images(self):
        factory = PieceFactory()
        white_piece_images = {
            'pawn': 'Images/pawn.png',
            'rook': 'Images/rook.png',
            'bishop': 'Images/bishop.png',
            'knight': 'Images/knight.png',
            'queen': 'Images/queen.png',
            'king': 'Images/king.png'
        }
        for piece, image in white_piece_images.items():
            self.assertEqual(image, factory.create_piece(piece, 'white', 0, 0).get_image_path())

    def test_pieces_get_black_images(self):
        factory = PieceFactory()
        white_piece_images = {
            'pawn': 'Images/pawn_b.png',
            'rook': 'Images/rook_b.png',
            'bishop': 'Images/bishop_b.png',
            'knight': 'Images/knight_b.png',
            'queen': 'Images/queen_b.png',
            'king': 'Images/king_b.png'
        }
        for piece, image in white_piece_images.items():
            self.assertEqual(image, factory.create_piece(piece, 'black', 0, 0).get_image_path())

    def test_move_piece_with_valid_input(self):
        factory = PieceFactory()
        piece = factory.create_piece('pawn', 'black', 0, 0)
        new_coordinates = (3, 4)
        self.assertEqual(False, piece.has_moved())
        self.assertEqual((0, 0), piece.get_board_index())
        piece.move(new_coordinates)
        self.assertNotEqual((0, 0), piece.get_board_index())
        self.assertEqual(new_coordinates, piece.get_board_index())
        self.assertEqual(True, piece.has_moved())

    def test_move_piece_with_invalid_input(self):
        factory = PieceFactory()
        piece = factory.create_piece('pawn', 'black', 0, 0)
        self.assertEqual((0, 0), piece.get_board_index())
        self.assertRaises(ValueError, lambda: piece.move(2))
        self.assertRaises(ValueError, lambda: piece.move('2, 2'))
        self.assertRaises(ValueError, lambda: piece.move(('f', 'g')))

if __name__ == '__main__':
    unittest.main()