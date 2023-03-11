from Classes.abstract_piece import Piece

class Player():
    """
        Class for holding the player's information
        Holds the array of pieces and the player colour which distinguishes which player is which.
    """
    def __init__(self, colour, pieces):
        """
            Initialize the player object.

            Parameters
            ----------
                colour: string
                    Distinguishes the two player
                pieces: array of piece objects
                    The array of all the pieces that each player has.
        """
        self.__player_error_handling(colour, pieces)
        self.colour = colour
        self.pieces = pieces

    def __player_error_handling(self, colour, pieces):
        if(colour == None or colour != 'white' and colour != 'black'):
            raise ValueError("Only white and black are supported as colours: {}".format(colour))

        if(pieces == None or len(pieces) != 16):
            raise ValueError("There need to be 16 pieces, not: {}".format(len(pieces)))
        for piece in pieces:
            if(not isinstance(piece, Piece)):
                raise ValueError("This isn't a chess pieces: {}".format(piece))


    def get_pieces(self):
        """
            Returns the player's current pieces.

            Returns
            -------
                self.pieces: array of piece objects
                    The current pieces the player has
        """
        return self.pieces

    def get_colour(self):
        """
            Returns
            -------
                self.colour: string
                    The player's distinguishing colour
        """
        return self.colour