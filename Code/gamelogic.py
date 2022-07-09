from Classes.player import *
from Classes.abstract_piece import *
from Classes.button import Button
from Classes.board import Board

class Game():
    def __init__(self, screen):
        board_pos = self.create_board()
        
        self.white_pieces = self.create_pieces('white', screen, board_pos)
        self.black_pieces = self.create_pieces('black', screen, board_pos)

        self.first_player = Player('white', self.white_pieces)
        self.second_player = Player('black', self.black_pieces)

        self.board = Board(board_pos, self.first_player, self.second_player)
 
        self.game_turn = ['p1'] 
        self.possible_moves = []
        self.current_piece = None

    def create_board(self):
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

    def __create_pieces_helper(self, colour, screen, p_type, amount, y_pos, piece_counter):
        pieces = []
        for i in range(amount):
            piece = None
            if p_type == "pawn":
                piece = Pawn(colour, (piece_counter, y_pos))
            elif p_type == "rook":
                piece = Rook(colour, (piece_counter, y_pos))
            elif p_type == "bishop":
                piece = Bishop(colour, (piece_counter, y_pos))
            elif p_type == "knight":
                piece = Knight(colour, (piece_counter, y_pos))
            elif p_type == "king":
                piece = King(colour, (piece_counter, y_pos))
            elif p_type == "queen":
                piece = Queen(colour, (piece_counter, y_pos))
            piece.initButton()
            piece_counter += 1
            pieces.append(piece)
    
        return pieces

    def create_pieces(self, colour, screen, board):
        pieces = []
        y_pos = 0 if colour == 'black' else 7
        piece_counter = 0
        pieces += self.__create_pieces_helper(colour, screen, 'rook', 1, y_pos, 0)
        pieces += self.__create_pieces_helper(colour, screen, 'knight', 1, y_pos, 1)
        pieces += self.__create_pieces_helper(colour, screen, 'bishop', 1, y_pos, 2)
        if colour == 'black':
            pieces += self.__create_pieces_helper(colour, screen, 'king', 1, y_pos, 3)
            pieces += self.__create_pieces_helper(colour, screen, 'queen', 1, y_pos, 4)
        else:
            pieces += self.__create_pieces_helper(colour, screen, 'queen', 1, y_pos, 3)
            pieces += self.__create_pieces_helper(colour, screen, 'king', 1, y_pos, 4)
        pieces += self.__create_pieces_helper(colour, screen, 'bishop', 1, y_pos, 5)
        pieces += self.__create_pieces_helper(colour, screen, 'knight', 1, y_pos, 6)
        pieces += self.__create_pieces_helper(colour, screen, 'rook', 1, y_pos, 7)
        
        y_pos = y_pos + 1 if colour == 'black' else y_pos - 1
        pieces += self.__create_pieces_helper(colour, screen, 'pawn', 8, y_pos, piece_counter)

        return pieces

    def __draw_helper(self, pieces, screen):
        for piece in pieces:
            piece.draw(screen)

    def draw_pieces(self, screen):
        self.__draw_helper(self.white_pieces, screen)
        self.__draw_helper(self.black_pieces, screen)
        for position in self.board.get_potentional_positions():
            position['Button'].draw(screen)

    def change_turn(self):
        next_turn = 'p2' if 'p1' in self.game_turn else 'p1'
        self.game_turn.clear()
        self.game_turn.append(next_turn)

    def remove_piece(self, piece):
        player = self.first_player if 'p1' not in self.game_turn else self.second_player
        player.getPieces().remove(piece)
        piece = None

    def select_move(self):
        for move in self.board.get_potentional_positions():
            if move['Button'].click():
                self.board.move_piece(self.current_piece, move['Index'])
                if(piece := move['Piece']):
                    self.remove_piece(piece)
                self.board.clear_potential_positions()
                self.change_turn()

    def highlight_possible_moves(self, piece):
        self.board.add_potential_positions(piece)

    def turn(self, player, screen):
        for piece in player.getPieces():
            if piece.piece_clicked():
                self.board.clear_potential_positions()
                self.highlight_possible_moves(piece)
                self.current_piece = piece

    def game(self, screen):
        self.turn(self.first_player, screen) if 'p1' in self.game_turn else self.turn(self.second_player, screen)
        self.select_move()