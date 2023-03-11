from Classes.abstract_piece import *

class PieceFactory():
    """
        Class for creation of different piece types.
    """
    def create_piece(self, p_type, colour, x_pos, y_pos):
        """
            Handles the creation of each piece type so that the game logic interacts with only generic pieces.

            Parameters
            ----------
                p_type: string
                    The specific piece to be created
                colour: string
                    The piece's colour, to select the appropriate image.
                x_pos: integer
                    Indicates the x-coordinate of the piece with respect to its array position on the board.
                y_pos: integer
                    Indicates the y-coordinate of the piece with respect to its array position on the board.

            Returns
            -------
                The created piece object.
        """
        if p_type == "pawn":
            return Pawn(colour, (x_pos, y_pos))
        elif p_type == "rook":
            return Rook(colour, (x_pos, y_pos))
        elif p_type == "bishop":
            return Bishop(colour, (x_pos, y_pos))
        elif p_type == "knight":
            return Knight(colour, (x_pos, y_pos))
        elif p_type == "king":
            return King(colour, (x_pos, y_pos))
        elif p_type == "queen":
            return Queen(colour, (x_pos, y_pos))
        else:
            raise ValueError("Invalid Piece Type: {}".format(p_type))