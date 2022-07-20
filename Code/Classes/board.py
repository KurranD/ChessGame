from Classes.button import Button
import json
from Classes.abstract_piece import *

class Board():
    def __init__(self, board_pos, firstPlayer, secondPlayer):
        self.board_pos = board_pos
        self.firstPlayer = firstPlayer
        self.secondPlayer = secondPlayer
        self.piecesBoard = [ [None]*8 for i in range(8)]
        self.create_board()
        self.potentialPositions = []

    def return_board_pos(self):
        return self.board_pos

    def exchange_pawn_piece(self, piece):
        y_coord = piece.get_board_index()[1]
        if piece.pieceType() == 'pawn' and (y_coord == 0 or y_coord == 7):
            tempButton = piece.get_button()
            tempColour = piece.get_colour()
            tempIndex = piece.get_board_index()
            player = self.firstPlayer if tempColour == self.firstPlayer.getColour() else self.secondPlayer
            player.getPieces().remove(piece)
            piece = Queen(tempColour, tempIndex)
            piece.set_button(tempButton)
            piece.initButton()
            piece.get_button().update_image(piece.get_image())
            player.getPieces().append(piece)

    def check_square_for_player_piece(self, boardPos, piece, oppositePlayer):
        if piece.pieceType() != 'pawn' and piece.pieceType() != 'knight':
            if not self.check_squares_in_line(boardPos, piece, oppositePlayer):
                return None
        return self.piecesBoard[boardPos[0]][boardPos[1]] if self.piecesBoard[boardPos[0]][boardPos[1]] in oppositePlayer.getPieces() else None

    def check_square_valid(self, boardPos, piece):
        if piece.pieceType() != 'knight':
            return self.check_squares_in_line(boardPos, piece)
        else:
            return self.piecesBoard[boardPos[0]][boardPos[1]] == None

    def __check_squares_in_line_helper(self, x_coord, y_coord, piecesToTake, players):
        if self.piecesBoard[x_coord][y_coord] and not(players != None and self.piecesBoard[x_coord][y_coord] in players.getPieces()):
            return False
        elif players != None and self.piecesBoard[x_coord][y_coord] in players.getPieces():
            piecesToTake.append(self.piecesBoard[x_coord][y_coord])
        return True

    def check_squares_in_line(self, boardPos, piece, players=None):
        piece_x = piece.get_board_index()[0]
        piece_y = piece.get_board_index()[1]
        piecesToTake = []
        if(boardPos[0] == piece_x):
            minNum = piece_y + 1 if piece_y < boardPos[1] else boardPos[1]
            diff = abs(piece_y - boardPos[1])
            for i in range(minNum, minNum + diff):
                if not self.__check_squares_in_line_helper(piece_x, i, piecesToTake, players):
                    return False
        elif(boardPos[1] == piece_y):
            minNum = piece_x + 1 if piece_x < boardPos[0] else boardPos[0]
            diff = abs(piece_x - boardPos[0])
            for i in range(minNum, minNum + diff):
                if not self.__check_squares_in_line_helper(i, piece_y, piecesToTake, players):
                    return False
        elif boardPos[1] < piece_y and piece_x < boardPos[0]:
            minNum = piece_x + 1 if piece_x < boardPos[0] else boardPos[0]
            diff = abs(piece_x - boardPos[0])
            j = piece_y - 1
            for i in range(minNum, minNum + diff):
                if self.check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, piecesToTake, players):
                    return False
                j -= 1
        elif boardPos[1] > piece_y and piece_x > boardPos[0]:
            minNum = piece_x + 1 if piece_x < boardPos[0] else boardPos[0]
            diff = abs(piece_x - boardPos[0])
            j = boardPos[1]
            for i in range(minNum, minNum + diff):
                if self.check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, piecesToTake, players):
                    return False
                j -= 1
        elif boardPos[1] < piece_y and piece_x > boardPos[0]:
            minNum = piece_x + 1 if piece_x < boardPos[0] else boardPos[0]
            diff = abs(piece_x - boardPos[0])
            j = boardPos[1]
            for i in range(minNum, minNum + diff):
                if self.check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, piecesToTake, players):
                    return False
                j += 1
        else:
            minNum = piece_x + 1 if piece_x < boardPos[0] else boardPos[0]
            diff = abs(piece_x - boardPos[0])
            j = piece_y + 1
            for i in range(minNum, minNum + diff):
                if self.check_out_of_range((i, j)):
                    continue
                if not self.__check_squares_in_line_helper(i, j, piecesToTake, players):
                    return False
                j += 1
        if len(piecesToTake) > 1:
            return False
        return True

    def check_out_of_range(self, boardPos):
        x = boardPos[0]
        y = boardPos[1]
        return x > 7 or x < 0 or y > 7 or y < 0

    def add_potential_positions(self, piece):
        for boardPos in piece.possible_moves():
            if self.check_out_of_range(boardPos):
                continue
            if not self.check_square_valid(boardPos, piece):
                continue
            pos = self.board_pos[boardPos[0]][boardPos[1]]
            self.potentialPositions.append({
                "Index": boardPos,
                "Button": Button(pos[0], pos[1], 'Images/selected.png'),
                "Piece": None
            })
        oppositePlayer = self.firstPlayer if self.secondPlayer.getColour() == piece.get_colour() else self.secondPlayer
        for boardPos in piece.possible_attack_moves():
            if self.check_out_of_range(boardPos):
                continue
            pos = self.board_pos[boardPos[0]][boardPos[1]]
            if(attack_piece := self.check_square_for_player_piece(boardPos, piece, oppositePlayer)):
                self.potentialPositions.append({
                    "Index": boardPos,
                    "Button": Button(pos[0], pos[1], 'Images/selected.png'),
                    "Piece": attack_piece
                })
        if piece.pieceType() == "king" and not piece.has_moved():
            boardPositions = []
            if piece.get_colour() == 'black':
                posToAdd = (piece.get_board_index()[0]+3, piece.get_board_index()[1])
                if self.piecesBoard[posToAdd[0]+1][posToAdd[1]] is not None and not self.piecesBoard[posToAdd[0]+1][posToAdd[1]].has_moved():
                    boardPositions.append(posToAdd)
                posToAdd = (piece.get_board_index()[0]-2, piece.get_board_index()[1])
                if self.piecesBoard[posToAdd[0]-1][posToAdd[1]] is not None and not self.piecesBoard[posToAdd[0]-1][posToAdd[1]].has_moved():
                    boardPositions.append(posToAdd)
            else:
                posToAdd = (piece.get_board_index()[0]+2, piece.get_board_index()[1])
                if self.piecesBoard[posToAdd[0]+1][posToAdd[1]] is not None and not self.piecesBoard[posToAdd[0]+1][posToAdd[1]].has_moved():
                    boardPositions.append(posToAdd)
                posToAdd = (piece.get_board_index()[0]-3, piece.get_board_index()[1])
                if self.piecesBoard[posToAdd[0]-1][posToAdd[1]] is not None and not self.piecesBoard[posToAdd[0]-1][posToAdd[1]].has_moved():
                    boardPositions.append(posToAdd)
            for boardPos in boardPositions:
                if self.check_out_of_range(boardPos):
                    continue
                if not self.check_square_valid(boardPos, piece):
                    continue
                if boardPos[0] - piece.get_board_index()[0] < -2:
                    boardPos = (boardPos[0]+1, boardPos[1])
                elif boardPos[0] - piece.get_board_index()[0] > 2:
                    boardPos = (boardPos[0]-1, boardPos[1])
                pos = self.board_pos[boardPos[0]][boardPos[1]]
                self.potentialPositions.append({
                    "Index": boardPos,
                    "Button": Button(pos[0], pos[1], 'Images/selected.png'),
                    "Piece": None
                })

    def get_potentional_positions(self):
        return self.potentialPositions

    def clear_potential_positions(self):
        self.potentialPositions = []

    def __create_board_helper(self, piece):
        pieceLoc = piece.get_board_index()
        self.piecesBoard[pieceLoc[0]][pieceLoc[1]] = piece
        pos = self.board_pos[pieceLoc[0]][pieceLoc[1]]
        piece.set_button(Button(pos[0], pos[1], piece.get_image()))

    def move_piece(self, piece, newBoardPos):
        oldPos = piece.get_board_index()
        self.piecesBoard[oldPos[0]][oldPos[1]] = None
        piece.move((newBoardPos))
        self.exchange_pawn_piece(piece)
        pos = self.board_pos[newBoardPos[0]][newBoardPos[1]]
        piece.get_button().move(pos[0], pos[1])
        self.piecesBoard[newBoardPos[0]][newBoardPos[1]] = piece

    def create_board(self):
        for piece in self.firstPlayer.getPieces() + self.secondPlayer.getPieces():
            self.__create_board_helper(piece)
        