from Classes.button import Button
import json
from Classes.abstract_piece import Piece

class Board():
    """
        Class for the game board object. Handles holding the board's objects and the logic associated with board squares.
    """
    def __init__(self, board_pos, first_player, second_player):
        """
            Initialize the Board object

            Parameters
            ----------
                board_pos: 2D Array
                    Array initialized with coordinates which map to the Chess board image so that each array position is a square on the board.
                first_player: Player object
                    Reference to player one.
                second_player: Player object
                    Reference to player two.
        """
        self.__board_error_handling(board_pos, first_player, second_player)
        self.__board_pos = board_pos
        self.__first_player = first_player
        self.__second_player = second_player
        self.__pieces_board = [ [None]*8 for i in range(8)]
        self.__create_board()
        self.__potential_positions = []

    def __board_error_handling(self, board_pos, first_player, second_player):
        if(board_pos == None or len(board_pos) != 8 or len(board_pos[0]) != 8):
            raise ValueError("The board needs to be 8x8: {}".format(board_pos))
        for index in range(0, 8):
            for second_index in range(0, 8):
                if(not isinstance(board_pos[index][second_index], tuple)):
                    raise ValueError("The values in the board_pos need to beintegers {}".format(board_pos[index][second_index]))

        if(first_player == None or second_player == None or first_player == second_player or first_player.get_colour() == second_player.get_colour()):
            raise ValueError("The players need to be different objects with different colours")

    def get_pieces_board(self):
        """
            Returns
            -------
                2D Array: Array of the squares on the board, tracking where pieces move.
        """
        return self.__pieces_board

    def return_board_pos(self):
        """
            Returns
            -------
                2D Array: Array of the coordinates corresponding to each square on the board.
        """
        return self.__board_pos

    def __exchange_pawn_piece(self, piece):
        """
            When a pawn reaches the end of the board it is automatically exchanged for a queen.

            Parameters
            ----------
                piece: Piece object
                    The pawn that has arrived at the end of the board
        """
        y_coord = piece.get_board_index()[1]
        if piece.get_piece_type() == 'pawn' and (y_coord == 0 or y_coord == 7):
            temp_button = piece.get_button()
            temp_colour = piece.get_colour()
            temp_index = piece.get_board_index()
            player = self.__first_player if temp_colour == self.__first_player.get_colour() else self.__second_player
            player.get_pieces().remove(piece)
            piece = Queen(temp_colour, temp_index)
            piece.set_button(temp_button)
            piece.get_button().update_image(piece.get_image_path())
            player.get_pieces().append(piece)

    def __check_square_for_player_piece(self, board_pos, piece, opposite_player):
        """
            This method is called for determining potential squares a piece can move to for taking an opponent's piece. All pieces require an unbroken line to move, except the pawn and knight, so the check_squares_in_line method is called to ensure an unbroken line to the square.
            Otherwise, the position is checked to see if it has an opponent's piece.

            Parameters
            ----------
                board_pos:
                    The coordinates of the board square to check for the opponent's piece
                piece: Piece object
                    The piece being used for potentially taking an opponent's piece
                opposite_player: Player object
                    The opposing player, to ensure the piece we're checking can be captured
            Returns
            -------
                None: if there is no piece capable of being captured
                Piece Object: If there is a piece which can be captured.
        """
        if piece.get_piece_type() != 'pawn' and piece.get_piece_type() != 'knight':
            if not self.__check_squares_in_line(board_pos, piece, opposite_player):
                return None
        return self.__pieces_board[board_pos[0]][board_pos[1]] if self.__pieces_board[board_pos[0]][board_pos[1]] in opposite_player.get_pieces() else None

    def __check_square_valid(self, board_pos, piece):
        """
            This method checks a specific square is valid to be added to the potential moves a piece can make.
            Moving a piece to valid square requires an unbroken line, one with no other pieces on it, to the square.
            The exception is the knight which just requires the square be unnoccupied.

            Parameters
            ----------
                board_pos:
                    The coordinates of the board square to check is a valid move
                piece: Piece object
                    The piece being used to move
            Returns
            -------
                False: If the square is occupied or unreachable
                True: If the square is unnocccupied and the piece can move to it
        """
        if piece.get_piece_type() != 'knight':
            return self.__check_squares_in_line(board_pos, piece)
        else:
            return self.__pieces_board[board_pos[0]][board_pos[1]] == None

    def __check_squares_in_line_helper(self, x_coord, y_coord, pieces_to_take, players):
        """
            Helper method for checking the potential squares in a line out from the currently selected piece. 
            Used to determine if the last square in the line to check contains an opposing piece that can be captured.
            If the square contains an opposing piece, that piece is then added to our list of pieces that are capturable.

            Parameters
            ----------
                x_coord: Integer
                    x-position of the board array to check
                y_coord: Integer
                    y-position of the board array to check
                pieces_to_take: Array of Piece Objects
                    Array of pieces that are capturable
                players: Player object
                    Either none or the opposing player. (None when only checking for places to move, opposing player when looking for capturable pieces)

            Returns
            -------
                False: If the square is occupied, either by the current player's piece or we aren't currently looking for capturable pieces
                True: If the square isn't occupied or is occupied by a capturable piece
        """
        if self.__pieces_board[x_coord][y_coord] and not(players != None and self.__pieces_board[x_coord][y_coord] in players.get_pieces()):
            return False
        elif players != None and self.__pieces_board[x_coord][y_coord] in players.get_pieces():
            pieces_to_take.append(self.__pieces_board[x_coord][y_coord])
        return True

    def __check_squares_in_line(self, board_pos, piece, players=None):
        """
            Checks each potential square given to make sure it's valid (no other piece is blocking it from moving)
            Apart from a couple exceptions, all the pieces move in a straight line that cannot jump over a piece, this checks the lines from the possible square to the piece to make sure it's valid
            Also, this checks for capturable pieces (opponent's pieces) in the line. pieces_to_take is appended to include these pieces, but only returns true if there is one piece (otherwise it means we're jumping over a piece)

            Parameters
            ----------
                board_pos: Integer coordinates
                    Coordinates in the board array to check whether or not it is a valid potential move.
                piece: Piece Object
                    The current selected piece to move
                players: Player object
                    Either none or the opposing player. (None when only checking for places to move, opposing player when looking for capturable pieces)

            Returns
            -------
                False: If the square is occupied, either by the current player's piece or we aren't currently looking for capturable pieces
                True: If the square isn't occupied or is occupied by a capturable piece
        """
        piece_x = piece.get_board_index()[0]
        piece_y = piece.get_board_index()[1]
        pieces_to_take = []
        if(board_pos[0] == piece_x):
            min_num = piece_y + 1 if piece_y < board_pos[1] else board_pos[1]
            diff = abs(piece_y - board_pos[1])
            for i in range(min_num, min_num + diff):
                if not self.__check_squares_in_line_helper(piece_x, i, pieces_to_take, players):
                    return False
        elif(board_pos[1] == piece_y):
            min_num = piece_x + 1 if piece_x < board_pos[0] else board_pos[0]
            diff = abs(piece_x - board_pos[0])
            for i in range(min_num, min_num + diff):
                if not self.__check_squares_in_line_helper(i, piece_y, pieces_to_take, players):
                    return False
        elif board_pos[1] < piece_y and piece_x < board_pos[0]:
            min_num = piece_x + 1 if piece_x < board_pos[0] else board_pos[0]
            diff = abs(piece_x - board_pos[0])
            j = piece_y - 1
            for i in range(min_num, min_num + diff):
                if self.__check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, pieces_to_take, players):
                    return False
                j -= 1
        elif board_pos[1] > piece_y and piece_x > board_pos[0]:
            min_num = piece_x + 1 if piece_x < board_pos[0] else board_pos[0]
            diff = abs(piece_x - board_pos[0])
            j = board_pos[1]
            for i in range(min_num, min_num + diff):
                if self.__check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, pieces_to_take, players):
                    return False
                j -= 1
        elif board_pos[1] < piece_y and piece_x > board_pos[0]:
            min_num = piece_x + 1 if piece_x < board_pos[0] else board_pos[0]
            diff = abs(piece_x - board_pos[0])
            j = board_pos[1]
            for i in range(min_num, min_num + diff):
                if self.__check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, pieces_to_take, players):
                    return False
                j += 1
        else:
            min_num = piece_x + 1 if piece_x < board_pos[0] else board_pos[0]
            diff = abs(piece_x - board_pos[0])
            j = piece_y + 1
            for i in range(min_num, min_num + diff):
                if self.__check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, pieces_to_take, players):
                    return False
                j += 1
        if len(pieces_to_take) > 1:
            return False
        return True

    def __check_out_of_range(self, board_pos):
        """
            Checks the potential square on the board to make sure it's within the board's boundaries.

            Parameters
            ----------
                board_pos: Integer coordinates
                    Coordinates in the board array to check whether or not it is a valid potential move.

            Returns
            -------
                False: If the square is outside the board.
                True: If the square is part of the board.
        """
        x_pos = board_pos[0]
        y_pos = board_pos[1]
        return x_pos > 7 or x_pos < 0 or y_pos > 7 or y_pos < 0

    def add_potential_positions(self, piece):
        """
            Once a piece is selected to move, this method loops through the potential moves that each piece has and validates which of them are legal moves given the current board's setup.
            The pieces are responsable for knowing how they move, the board validates whether those moves are out of range or if another piece is blocking the way
            All valid moves are appended to the potential_positions array, displaying them to the user as clickable choices.

            Parameters
            ----------
                piece: Piece Object
                    The current selected piece to move
        """
        for board_pos in piece.get_possible_moves():
            if self.__check_out_of_range(board_pos):
                continue
            if not self.__check_square_valid(board_pos, piece):
                continue
            pos = self.__board_pos[board_pos[0]][board_pos[1]]
            self.__potential_positions.append({
                "Index": board_pos,
                "Button": Button(pos[0], pos[1], 'Images/selected.png'),
                "Piece": None
            })
        opposite_player = self.__first_player if self.__second_player.get_colour() == piece.get_colour() else self.__second_player
        for board_pos in piece.get_possible_attack_moves():
            if self.__check_out_of_range(board_pos):
                continue
            pos = self.__board_pos[board_pos[0]][board_pos[1]]
            if(attack_piece := self.__check_square_for_player_piece(board_pos, piece, opposite_player)):
                self.__potential_positions.append({
                    "Index": board_pos,
                    "Button": Button(pos[0], pos[1], 'Images/selected.png'),
                    "Piece": attack_piece
                })
        # Calculating if castling is possible as a potential move
        if piece.get_piece_type() == "king" and not piece.has_moved():
            board_positions = []
            if piece.get_colour() == 'black':
                pos_to_add = (piece.get_board_index()[0]+3, piece.get_board_index()[1])
                if self.__pieces_board[pos_to_add[0]+1][pos_to_add[1]] is not None and not self.__pieces_board[pos_to_add[0]+1][pos_to_add[1]].has_moved():
                    board_positions.append(pos_to_add)
                pos_to_add = (piece.get_board_index()[0]-2, piece.get_board_index()[1])
                if self.__pieces_board[pos_to_add[0]-1][pos_to_add[1]] is not None and not self.__pieces_board[pos_to_add[0]-1][pos_to_add[1]].has_moved():
                    board_positions.append(pos_to_add)
            else:
                pos_to_add = (piece.get_board_index()[0]+2, piece.get_board_index()[1])
                if self.__pieces_board[pos_to_add[0]+1][pos_to_add[1]] is not None and not self.__pieces_board[pos_to_add[0]+1][pos_to_add[1]].has_moved():
                    board_positions.append(pos_to_add)
                pos_to_add = (piece.get_board_index()[0]-3, piece.get_board_index()[1])
                if self.__pieces_board[pos_to_add[0]-1][pos_to_add[1]] is not None and not self.__pieces_board[pos_to_add[0]-1][pos_to_add[1]].has_moved():
                    board_positions.append(pos_to_add)
            for board_pos in board_positions:
                if self.__check_out_of_range(board_pos):
                    continue
                if not self.__check_square_valid(board_pos, piece):
                    continue
                if board_pos[0] - piece.get_board_index()[0] < -2:
                    board_pos = (board_pos[0]+1, board_pos[1])
                elif board_pos[0] - piece.get_board_index()[0] > 2:
                    board_pos = (board_pos[0]-1, board_pos[1])
                pos = self.__board_pos[board_pos[0]][board_pos[1]]
                self.__potential_positions.append({
                    "Index": board_pos,
                    "Button": Button(pos[0], pos[1], 'Images/selected.png'),
                    "Piece": None
                })

    def get_potential_positions(self):
        """
            Returns
            -------
                Array of JSON objects: Array of potential positions which has fields for: board position, button object, and optionally the piece to capture.
        """
        return self.__potential_positions

    def clear_potential_positions(self):
        """
            Clears the potential_positions array. This stops the display on the board of potential moves so we can display a new set or move to a new turn.
        """
        self.__potential_positions = []

    def __create_board_helper(self, piece):
        """
            Helper method for putting each piece in its position on the board and then setting the pieces' buttons to their appropriate position using the board's positions' coordinates.

            Parameters
            ----------
                piece: Piece Object
                    The current spiece (being looped through in the create_board method)
        """
        piece_loc = piece.get_board_index()
        self.__pieces_board[piece_loc[0]][piece_loc[1]] = piece
        pos = self.__board_pos[piece_loc[0]][piece_loc[1]]
        piece.set_button(Button(pos[0], pos[1], piece.get_image_path()))

    def move_piece(self, piece, new_board_pos):
        """
            Updates piece selected to move on the board. Deletes old entry in the array, updates position of piece in the board array as well as the coordinates for the button (for displaying image / clicking)

            Parameters
            ----------
                piece: Piece Object
                    The current selected piece to move
                new_board_pos: Integer coordinates
                    Coordinates cooresponding to the index in the 2D board array 
        """

        if(not isinstance(piece, Piece) or not isinstance(new_board_pos, tuple) or (new_board_pos[0] < 0 or new_board_pos[0] > 8 or new_board_pos[1] < 0 or new_board_pos[1] > 8)):
            raise ValueError("Values are not correct for moving a piece. piece: {} coords: {}".format(piece, new_board_pos))
        
        old_pos = piece.get_board_index()
        self.__pieces_board[old_pos[0]][old_pos[1]] = None
        piece.move((new_board_pos))
        self.__exchange_pawn_piece(piece)
        pos = self.__board_pos[new_board_pos[0]][new_board_pos[1]]
        piece.get_button().move(pos[0], pos[1])
        self.__pieces_board[new_board_pos[0]][new_board_pos[1]] = piece

    def __create_board(self):
        """
            Loops through all the pieces in order to set them up on the board (using the helper method to separate the logic).
        """
        for piece in self.__first_player.get_pieces() + self.__second_player.get_pieces():
            self.__create_board_helper(piece)
        