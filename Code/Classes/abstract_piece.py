from abc import abstractmethod, ABC
import pygame
import os

class Piece(ABC):
    """
    The Piece class is the generic abstract class for all the chess pieces
    Implement as one of the below specific classes.
    """

    def __init__(self, colour, board_pos):
        """
        Initialize the Piece by setting colour and square
        
        Paramters
        ---------
        colour: string
            'white' or 'black' to identify player
        board_pos: 2D coordinates, (x, y) 
            2D index referring to square on board array 
            (NOTE: THIS IS THE POSITION IN THE Board objects array, not 
            the position on the screen)
        """

        if(colour == None or colour != 'white' and colour != 'black'):
            raise ValueError("Only white and black are supported as colours: {}".format(colour))

        self.__piece_error_handling(board_pos)

        self.__colour = colour
        self.__boardx = board_pos[0]
        self.__boardy = board_pos[1]
        self.__moved = False
        self.__button = None

    def __piece_error_handling(self, board_pos):
        if(not isinstance(board_pos, tuple) or not isinstance(board_pos[0], int) or not isinstance(board_pos[1], int) or board_pos[0] < 0 or board_pos[0] > 8 or board_pos[1] < 0 or board_pos[1] > 8):
            raise ValueError("Assigned positions must be within the board's 9x9 grid.")

    @abstractmethod
    def get_piece_type(self):
        """
        Abstract method to return piece type
        
        Returns
        -------
        string
            Name of the piece, ex: 'pawn', 'king'
        """
        pass

    @abstractmethod
    def get_possible_moves(self):
        """
        Abstract method for calculating the potential moves a piece is capable of making. (All pieces calculate their moves generically. The board will be responsable for preventing pieces from going over the edge or moving over one another)
        
        Returns
        -------
        array
            An array of the board positions the piece can move to.
        """
        pass

    @abstractmethod
    def get_possible_attack_moves(self):
        """
        Abstract method for calculating the potential moves a piece is capable of making to take another piece (All pieces calculate their moves generically. The board will be responsable for preventing pieces from going over the edge or moving over one another)
        
        Returns
        -------
        array
            An array of the board positions the piece can move to occupied by an opposing piece
        """
        pass

    def piece_clicked(self):
        """
        Calls the piece's Button's object's click method
        Runs in a loop, returning False until a mouse click is registered.
        
        Returns
        -------
        boolean
            Returns True if the button is clicked, otherwise False
        """
        return self.__button.click()

    def get_colour(self):
        """
        Returns the piece's colour according to what was set in __init__
        
        Returns
        -------
        string
            Returns 'white' or 'black'
        """
        return self.__colour

    def move(self, board_pos):
        """
        Updates the piece's position in the Board object's array

        Parameters
        ----------
        board_pos: 2D coordinates, (x, y)
            The new coordinates the piece is expected to move to in the Board object's array        
        """
        self.__piece_error_handling(board_pos)
        self.__moved = True
        self.__boardx = board_pos[0]
        self.__boardy = board_pos[1]

    def has_moved(self):
        """
        Returns whether or not the piece has moved already.
        Used for several pieces which have different behaviour for first moves.

        Returns
        -------
        Boolean
            True if the piece has already been moved, False otherwise.
        """
        return self.__moved

    def set_button(self, button):
        """
        Updates the piece's Button object

        Parameters
        ----------
        button: Button obj
            A button object for registering clicks and loading the image    
        """
        self.__button = button

    def get_button(self):
        """
        Returns the piece's Button object

        Returns
        -------
        Button obj
            A button object for registering clicks and loading the image    
        """
        return self.__button

    def draw(self, screen):
        """
        Draws the piece to the screen via it's Button obj

        Parameters
        ----------
        screen: Pygame Display obj
            The display screen upon which the image is drawn   
        """
        self.__button.draw(screen)

    def get_board_index(self):
        """
        Returns the piece's 2D coordinates in the Board obj's array

        Parameters
        ----------
        2D Coordinates
            The location in the board array where the piece is currently located
        """
        return (self.__boardx, self.__boardy)

class Pawn(Piece):
    def __init__(self, colour, board_pos):
        super().__init__(colour, board_pos)
        self.__init_piece()
    
    def __init_piece(self):
        self.__image_path = 'Images/pawn.png' if self.get_colour() == 'white' else 'Images/pawn_b.png'

    def get_piece_type(self):
        return 'pawn'

    def get_image_path(self):
        return self.__image_path

    def move(self, board_pos):
        super().move(board_pos)

    def get_possible_moves(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        yoffset = 1 if self.get_colour() == 'black' else -1
        possible_moves.append((board_pos_x, board_pos_y+yoffset))
        if(not self.has_moved()):
            possible_moves.append((board_pos_x, board_pos_y+yoffset*2))
        return possible_moves

    def get_possible_attack_moves(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        yoffset = 1 if self.get_colour() == 'black' else -1
        possible_moves.append((board_pos_x+1, board_pos_y+yoffset))
        possible_moves.append((board_pos_x-1, board_pos_y+yoffset))
        return possible_moves

class Rook(Piece):
    def __init__(self, colour, board_pos):
        super().__init__(colour, board_pos)
        self.__init_piece()
    
    def __init_piece(self):
        self.__image_path = 'Images/rook.png' if self.get_colour() == 'white' else 'Images/rook_b.png'

    def get_piece_type(self):
        return 'rook'

    def get_image_path(self):
        return self.__image_path

    def move(self, board_pos):
        super().move(board_pos)

    def __moves_helper(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        for i in range(1, 8):
            possible_moves.append((board_pos_x, board_pos_y+i))
            possible_moves.append((board_pos_x, board_pos_y-i))
            possible_moves.append((board_pos_x+i, board_pos_y))
            possible_moves.append((board_pos_x-i, board_pos_y))
        return possible_moves

    def get_possible_moves(self):
        return self.__moves_helper()

    def get_possible_attack_moves(self):
        return self.__moves_helper()

class Bishop(Piece):
    def __init__(self, colour, board_pos):
        super().__init__(colour, board_pos)
        self.__init_piece()
    
    def __init_piece(self):
        self.__image_path = 'Images/bishop.png' if self.get_colour() == 'white' else 'Images/bishop_b.png'

    def get_piece_type(self):
        return 'bishop'

    def get_image_path(self):
        return self.__image_path

    def move(self, board_pos):
        super().move(board_pos)

    def __moves_helper(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        for i in range(1, 8):
            possible_moves.append((board_pos_x+i, board_pos_y+i))
            possible_moves.append((board_pos_x+i, board_pos_y-i))
            possible_moves.append((board_pos_x-i, board_pos_y+i))
            possible_moves.append((board_pos_x-i, board_pos_y-i))
        return possible_moves

    def get_possible_moves(self):
        return self.__moves_helper()

    def get_possible_attack_moves(self):
        return self.__moves_helper()

class Knight(Piece):
    def __init__(self, colour, board_pos):
        super().__init__(colour, board_pos)
        self.__init_piece()
    
    def __init_piece(self):
        self.__image_path = 'Images/knight.png' if self.get_colour() == 'white' else 'Images/knight_b.png'

    def get_piece_type(self):
        return 'knight'

    def get_image_path(self):
        return self.__image_path

    def move(self, board_pos):
        super().move(board_pos)

    def __moves_helper(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        possible_moves.append((board_pos_x+1, board_pos_y+2))
        possible_moves.append((board_pos_x+1, board_pos_y-2))
        possible_moves.append((board_pos_x-1, board_pos_y+2))
        possible_moves.append((board_pos_x-1, board_pos_y-2))
        possible_moves.append((board_pos_x+2, board_pos_y+1))
        possible_moves.append((board_pos_x+2, board_pos_y-1))
        possible_moves.append((board_pos_x-2, board_pos_y+1))
        possible_moves.append((board_pos_x-2, board_pos_y-1))
        return possible_moves

    def get_possible_moves(self):
        return self.__moves_helper()

    def get_possible_attack_moves(self):
        return self.__moves_helper()

class Queen(Piece):
    def __init__(self, colour, board_pos):
        super().__init__(colour, board_pos)
        self.__init_piece()
    
    def __init_piece(self):
        self.__image_path = 'Images/queen.png' if self.get_colour() == 'white' else 'Images/queen_b.png'

    def get_piece_type(self):
        return 'queen'

    def get_image_path(self):
        return self.__image_path

    def move(self, board_pos):
        super().move(board_pos)

    def __moves_helper(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        for i in range(1, 8):
            possible_moves.append((board_pos_x, board_pos_y+i))
            possible_moves.append((board_pos_x, board_pos_y-i))
            possible_moves.append((board_pos_x+i, board_pos_y))
            possible_moves.append((board_pos_x-i, board_pos_y))
            possible_moves.append((board_pos_x+i, board_pos_y+i))
            possible_moves.append((board_pos_x+i, board_pos_y-i))
            possible_moves.append((board_pos_x-i, board_pos_y+i))
            possible_moves.append((board_pos_x-i, board_pos_y-i))
        return possible_moves

    def get_possible_moves(self):
        return self.__moves_helper()

    def get_possible_attack_moves(self):
        return self.__moves_helper()

class King(Piece):
    def __init__(self, colour, board_pos):
        super().__init__(colour, board_pos)
        self.__init_piece()
    
    def __init_piece(self):
        self.__image_path = 'Images/king.png' if self.get_colour() == 'white' else 'Images/king_b.png'

    def get_piece_type(self):
        return 'king'

    def get_image_path(self):
        return self.__image_path

    def move(self, board_pos):
        super().move(board_pos)

    def __moves_helper(self):
        possible_moves = []
        board_pos_x, board_pos_y = super().get_board_index()
        for i in range(1, 2):
            possible_moves.append((board_pos_x, board_pos_y+i))
            possible_moves.append((board_pos_x, board_pos_y-i))
            possible_moves.append((board_pos_x+i, board_pos_y))
            possible_moves.append((board_pos_x-i, board_pos_y))
            possible_moves.append((board_pos_x+i, board_pos_y+i))
            possible_moves.append((board_pos_x+i, board_pos_y-i))
            possible_moves.append((board_pos_x-i, board_pos_y+i))
            possible_moves.append((board_pos_x-i, board_pos_y-i))

        return possible_moves

    def get_possible_moves(self):
        return self.__moves_helper()

    def get_possible_attack_moves(self):
        return self.__moves_helper()