from Classes.player import *
from Classes.button import Button
from Classes.board import Board
from Classes.piece_factory import PieceFactory

import os
import pygame
import sys

class Game():
    """
        Class for controlling much of the game logic.
        Game logic is split between higher level control which belongs here and
        lower level management of the board which is contained in board.py.
    """
    def __init__(self):
        """
            Initialize the game logic
        """
        self.__factory = PieceFactory()
        
        self.__white_pieces = self.__create_pieces('white')
        self.__black_pieces = self.__create_pieces('black')

        self.__first_player = Player('white', self.__white_pieces)
        self.__second_player = Player('black', self.__black_pieces)

        self.__board = self.__create_board(self.__first_player, self.__second_player)
 
        self.__game_turn = 'p1'
        self.__possible_moves = []
        self.__current_piece = None

    def __create_board(self, first_player, second_player):
        """
            This creates the array object which represents the board and is used to initialize the Board object. The array object is initialized with positions that follow the squares on the board image.
            The reason for creating the array here as opposed to in the board.py class is separation of logic from initialization.
            The GameLogic class handles most of the initializations and the top level game logic whereas the Board class is focused on the logic of managing the board's squares.
        """
        board = [ [0]*8 for i in range(8)]
        x_coord = 60
        y_coord = 55
        for y in range(0, 8):
            for x in range(0, 8):
                board[x][y] = (x_coord, y_coord)
                x_coord += 75
            y_coord += 75
            x_coord = 60
        return Board(board, first_player, second_player)

    def __create_pieces_helper(self, colour, p_type, amount, y_pos, piece_counter):
        """
            A helper method for creating pieces. Handles the creation of duplicate pieces which lets the create_pieces method remain clean and easy to read.
            
            Paramters
            ---------
                colour: string
                    The pieces' colour, white or black, for choosing the correct image to distinguish pieces on the board.
                p_type: string
                    The piece type, to tell the piece factory which piece to create.
                amount: integer
                    Number of pieces to be created
                y_pos: integer
                    Sets y coordinate in the board array.
                piece_counter: integer
                    Creates the x coordinate in the board array.
        """
        pieces = []
        for i in range(amount):
            piece = self.__factory.create_piece(p_type, colour, piece_counter, y_pos)
            piece_counter += 1
            pieces.append(piece)
    
        return pieces

    def __create_pieces(self, colour):
        """
            Creates all the different chess pieces (the actual creation is done in the helper method, but the logic of distinguishing the pieces is here)
            
            Paramters
            ---------
                colour: string
                    The pieces' colour, white or black, for choosing the correct image to distinguish pieces on the board.

            Returns
            -------
            Object Array
                Array of all pieces for the specified colour (player).
        """
        pieces = []
        y_pos = 0 if colour == 'black' else 7
        pieces += self.__create_pieces_helper(colour, 'rook', 1, y_pos, 0)
        pieces += self.__create_pieces_helper(colour, 'knight', 1, y_pos, 1)
        pieces += self.__create_pieces_helper(colour, 'bishop', 1, y_pos, 2)
        if colour == 'black':
            pieces += self.__create_pieces_helper(colour, 'king', 1, y_pos, 3)
            pieces += self.__create_pieces_helper(colour, 'queen', 1, y_pos, 4)
        else:
            pieces += self.__create_pieces_helper(colour, 'queen', 1, y_pos, 3)
            pieces += self.__create_pieces_helper(colour, 'king', 1, y_pos, 4)
        pieces += self.__create_pieces_helper(colour, 'bishop', 1, y_pos, 5)
        pieces += self.__create_pieces_helper(colour, 'knight', 1, y_pos, 6)
        pieces += self.__create_pieces_helper(colour, 'rook', 1, y_pos, 7)
        
        y_pos = y_pos + 1 if colour == 'black' else y_pos - 1
        pieces += self.__create_pieces_helper(colour, 'pawn', 8, y_pos, 0)

        return pieces

    def __draw_helper(self, pieces, screen):
        """
            Helper method that loops through the array of pieces passed in, calling their respective draw methods to load the image to the appropriate place.
            
            Paramters
            ---------
                pieces: object array
                    Array of all pieces to be drawn
                screen: Pygame Display obj
                    The object for rendering all images in the game, passed into the draw method to load the images.
        """
        for piece in pieces:
            piece.draw(screen)

    def draw_pieces(self, screen):
        """
            Generic method for drawing all dynamic objects (both players' pieces and selectable squares' images)
            
            Paramters
            ---------
                screen: Pygame Display obj
                    The object for rendering all images in the game, passed into the draw method to load the images.
        """
        self.__draw_helper(self.__white_pieces, screen)
        self.__draw_helper(self.__black_pieces, screen)
        for position in self.__board.get_potential_positions():
            position['Button'].draw(screen)

    def __change_turn(self):
        """
            Handles turn changes (Separated as method in order to increase readability)
        """
        self.__game_turn = 'p2' if 'p1' == self.__game_turn else 'p1'

    def __game_over(self):
        """
            Sets game state to game over (Separated as method in order to increase readability and for future add ons)
            Currently this method only modifies the game state, which sends the users back to the menu screen, in the future this should display a final screen announcing the winner.
        """
        self.game_state_manager(self.game_state, 'gameOver')

    def __remove_piece(self, piece):
        """
            Handles removing a 'taken' piece. Takes in the piece in the occupied game board square and removes it from the non current player. (If  the piece is a king, the game is ended)
            
            Paramters
            ---------
                piece: Piece object
                    The piece to be removed from the board after being taken by the opposing player.
        """
        player = self.__first_player if 'p1' != self.__game_turn else self.__second_player
        player.get_pieces().remove(piece)
        if piece.get_piece_type() == 'king':
            self.__game_over()
        piece = None

    def __select_move(self):
        """
            This method is called as part of the regular game loop. The for loop will be empty until a piece is selected and then the board objects potential positions' array will be populated.
            The potential positions' array is a list of every move that a piece can make. This loop will cycle through all these possibilities to register a click on one of them.
            
            This loop can be broken down into two sections within the first if statement (checking for a click).
            The main section is what will always occur and it shifts the selected piece to the newly selected square. The piece is added to the new square in the board array and old square removes its reference to the piece, the potential positions' array is cleared and the turn is changed.

            The second section is contained in the if statement for the condition that the piece selected is the king and it hasn't moved yet. This logic is to handle castling (swapping the rook and king) which requires a bit more involved logic than the other moves since two pieces move.
        """
        for move in self.__board.get_potential_positions():
            if move['Button'].click():
                if self.__current_piece.get_piece_type() == 'king' and not self.__current_piece.has_moved():
                    pos_diff = move['Index'][0] - self.__current_piece.get_board_index()[0]
                    board_layout = self.__board.get_pieces_board()
                    if(pos_diff > 1):
                        rook = board_layout[move['Index'][0]+1][move['Index'][1]] if board_layout[move['Index'][0]+1][move['Index'][1]] != None else board_layout[move['Index'][0]+2][move['Index'][1]]
                        self.__board.move_piece(rook, (move['Index'][0]-1, move['Index'][1]))
                    elif(pos_diff < -1):
                        rook = board_layout[move['Index'][0]-1][move['Index'][1]] if board_layout[move['Index'][0]-1][move['Index'][1]] != None else board_layout[move['Index'][0]-2][move['Index'][1]]
                        self.__board.move_piece(rook, (move['Index'][0]+1, move['Index'][1]))
                self.__board.move_piece(self.__current_piece, move['Index'])
                if(piece := move['Piece']):
                    self.__remove_piece(piece)
                self.__board.clear_potential_positions()
                self.__change_turn() 

    def __turn(self, player):
        """
            This method is called as part of the regular game loop and cycles through the current player's pieces.
            The pieces are cycled through waiting for a click which then updates the board with the potential moves for the selected piece.

            Paramters
            ---------
                player: player object
                    The current player whose turn it is.
        """
        for piece in player.get_pieces():
            if piece.piece_clicked():
                self.__board.clear_potential_positions()
                self.__board.add_potential_positions(piece)
                self.__current_piece = piece

    def menu_display(self, game_state, start_button, exit_button):
        """
            Game menu logic. Displays the menu screen with start and exit buttons, loading the chess board upon start being clicked.

            Paramters
            ---------
                game_state: array
                    Takes in the array object holdingthe current game state: 'menu', 'game', or 'gameOver'
                start_button: button object
                    The button object for the start button (to begin the game)
                exit_button: button object
                    The button object for the quit button (to exit)
            
            Returns
            -------
                background: pygame image
                    The background image loaded through pygame.
        """
        self.game_state = game_state
        background = pygame.image.load(os.path.join('./', 'Images/Menu.png'))
        if start_button.click():
            background = pygame.image.load(os.path.join('./', 'Images/chess_board.jpg'))
            self.game_state_manager(game_state, 'game')
        if exit_button.click():
            sys.exit()
        return background

    def game_state_manager(self, game_state, new_state):
        """
            Swaps the "game state" shifting the game from menu to current game to game over.
            Done as an array to persist the state as it goes between gamelogic.py and run.py (strings in python are pass by value)

            Paramters
            ---------
                game_state: array
                    Takes in the array object holdingthe current game state: 'menu', 'game', or 'gameOver'
                new_state: string
                    The new state to set the game to
        """
        game_state.clear()
        game_state.append(new_state)

    def game(self):
        """
            Central game loop called from run.py, this handles passing in the current player to the turn method (handles piece selection) and then the select_move method (handles moving the selected piece).
        """
        self.__turn(self.__first_player) if 'p1' == self.__game_turn else self.__turn(self.__second_player)
        self.__select_move()