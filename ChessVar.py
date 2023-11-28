# Author: Josquin Larsen
# GitHub username: josquinlarsen
# Date: 18/nov/2023
# Description: Project 9: Portfolio Project - ChessVar.py -

class ChessVar:
    """ a class to create an object of a ChessVar game"""

    def __init__(self):
        self._game_state = 'UNFINISHED'  # 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'
        self._move_state = 'WHITE'  # 'BLACK'
        self._board_size = 8
        self._game_board = [['_', 'n', 'b', 'q', '_', 'b', 'n', '_'],
                            ['_', 'p', 'p', '_', '_', '_', 'p', 'p'],
                            ['_', '_', '_', '_', 'k', '_', '_', '_'],
                            ['r', '_', '_', 'p', '_', '_', '_', 'N'],
                            ['P', '_', '_', 'p', '_', '_', '_', 'r'],
                            ['_', '_', '_', 'p', '_', '_', '_', '_'],
                            ['_', 'P', 'P', '_', 'K', '_', 'P', 'P'],
                            ['R', 'N', 'B', 'Q', '_', '_', '_', 'R']]  # list?

        self._white_dict = {'K': 1, 'Q': 1, 'R': 2, 'B': 2, 'N': 2, 'P': 8}
        self._black_dict = {'k': 1, 'q': 1, 'r': 2, 'b': 2, 'n': 2, 'p': 8}
        self._algebra_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self._white_counter = 1
        self._black_counter = 1
        self._capture = 'NO'  # 'YES'

    def get_game_state(self):
        """return game state"""
        return self._game_state

    def set_game_state(self, game_state):
        """set/update game state"""
        self._game_state = game_state

    def get_move_state(self):
        """ return whose move it is"""
        return self._move_state

    def set_move_state(self, player:str):
        """update move state 'WHITE' or 'BLACK' """
        self._move_state = player

    def update_game_board(self, new_board):
        """update game board for next move"""
        self._game_board = new_board

    def get_white_counter(self):
        """return number of white moves"""
        return self._white_counter

    def inc_white_counter(self):
        """increment white counter"""
        return self._white_counter + 1

    def get_black_counter(self):
        """ return black move counter"""
        return self._black_counter

    def inc_black_counter(self):
        """ increment black counter"""
        return self._black_counter + 1

    def convert_algebraic(self, position: str):
        """
        converts algebraic notation to 2d array coordinates,
        returns tuple for unpacking
        """
        # decorator?
        letter_column = 0
        number_row = 0
        if len(position) != 2:
            letter_column = -1
        check_alpha = position[0].isalpha()
        if check_alpha is not True:
            letter_column = -1
        check_num = position[1].isdigit()
        if check_num is not True:
            letter_column = -1
        if position[0] not in self._algebra_dict:
            letter_column = -1
        if letter_column < 0 or letter_column >= 8:
            letter_column = -1
        else:
            if position[0] in self._algebra_dict:
                letter_column += (self._algebra_dict[position[0]])
                number_row += 8 - (int(position[1]))

        return letter_column, number_row

    def make_move(self, start_pos: str, end_pos: str):
        """return False if move is illegal, or game is already won"""
        if self._game_state != 'UNFINISHED':
            return False
        start_coord = self.convert_algebraic(start_pos)
        end_coord = self.convert_algebraic(end_pos)
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        if -1 in start_coord or -1 in end_coord:  # check out-of-bounds move (e.g. a9 or i1)
            return False

        square = self._game_board[start_column][start_row]

        if self._move_state == 'WHITE':
            if square == '_':  # empty square
                return False
            if square.islower() is True:  # trying to move black piece
                return False

            valid_move_white = self.check_white_move(start_coord, end_coord)
            if valid_move_white is False:
                return False
            self.set_move_state('BLACK')
            self._white_counter += 1

            return True

        if self._move_state == 'BLACK':
            if square == '_':
                return False
            if square.isupper() is True: # trying to move white piece
                return False
            valid_move_black = self.check_black_move(start_coord, end_coord) # returning None need to return True or False ?
            if valid_move_black is False:
                return False
            self.set_move_state('WHITE')
            self._black_counter += 1

            return True


    def print_board(self):
        """print nice board"""
        for row in self._game_board:
            printed_row = ""
            for column in row:
                printed_row += column
            print(printed_row)

    def check_white_move(self, start_coord, end_coord):
        """check if white move is valid"""
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        piece = self._game_board[start_column][start_row]

        if piece == 'P':
            return self.move_white_pawn(start_coord, end_coord)

        if self._game_board[start_column][start_row] == 'N':
            return self.move_white_knight(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'B':
            pass
        if self._game_board[start_column][start_row] == 'R':
            pass
        if self._game_board[start_column][start_row] == 'Q':
            pass

        if piece == 'K':
            return self.move_white_king(start_coord, end_coord)


    def check_black_move(self, start_coord, end_coord):
        """check if black move is valid"""
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        piece = self._game_board[start_column][start_row]

        if piece == 'p':
            return self.move_black_pawn(start_coord, end_coord)

        if piece == 'n':
            return self.move_black_knight(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'b':
            pass

        if self._game_board[start_column][start_row] == 'r':
            return self.move_black_rook(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'q':
            pass

        if piece == 'k':
            return self.move_black_king(start_coord, end_coord)


    #USE THESE INSTEAD OF MOVE?

    def move_black_pawn(self, start_coord, end_coord): # not returning True or False
        """
        checks if black pawn move is valid if so moves the pawn and returns True, if not returns False
        """
        # 'p'
        # start:  a7 - h7
        # open: row +1 or +2
        # subsequent: row +1
        # capture: column +/- 1, row +1
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if 0 <= column_result > 2:
            return False

        if start_column == 1:  # opening pawn move
            if column_result == 2 and row_result != 0:
                return False
            else:
                if self._game_board[start_column + 1][start_row] == '_':
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'p'
                    return True

            if column_result == 1 and self._game_board[end_column][end_row] == '_':
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'p'
                return True

        if abs(row_result) == 1 and column_result == 1:
            check_opponent = self._game_board[end_column][end_row].isupper()  # capture
            if check_opponent is True:
                captured_piece = self._game_board[end_column][end_row]
                self._white_dict[captured_piece] -= 1
                if self._white_dict[captured_piece] == 0:
                    self.set_game_state('BLACK_WON')

                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'p'

                return True

        if column_result == 1 and self._game_board[end_row][end_column] == '_':
            self._game_board[start_column][start_row] = '_'
            self._game_board[end_column][end_row] = 'p'
            return True
        else:
            return False

    def move_black_knight(self, start_coord, end_coord):
        # 'n'
        # start b8, g8
        # open: col +/- 1 row + 2 or col +/- 2 row + 1;
        # subsequent: col +/- 1, row +/- 2 or col +/- 2 row +/- 1
        # no special capture
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if 0 > end_column > 7 or 0 > end_row > 7:  # already check?
            return False
        
        if abs(column_result) > 2 or abs(row_result) > 2:
            return False
        
        if self._game_board[end_column][end_row] == '_':
            if abs(column_result) == 1 and abs(row_result) == 2:
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'n'
                return True
            if abs(column_result) == 2 and abs(row_result) == 1:
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'n'
                return True
            else:
                return False
        
        check_opponent = self._game_board[end_column][end_row].isupper()
        if check_opponent is True:
            captured_piece = self._game_board[end_column][end_row]
            self._white_dict[captured_piece] -= 1
            if self._white_dict[captured_piece] == 0:
                self.set_game_state('BLACK_WON')

            self._game_board[start_column][start_row] = '_'
            self._game_board[end_column][end_row] = 'n'

            return True
        else:
            return False

    def move_white_bishop(self):
        # 'B'
        # start: c1, f1
        # open: col +open space row + open space (col +1, row+1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        pass

    def move_black_rook(self, start_coord, end_coord):
        # 'r'
        # start: a8, h8
        # open: col + open space OR row + open space
        # subsequent: col +/- open space OR row +/- open space
        # TODO
        
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if row_result == 0:                             # check_column
            check_black = self._game_board[end_column][end_row].islower()  
            if check_black is True:
                return False
            else:
                if self._game_board[end_column][end_row] == '_':
                    for square in range(abs(column_result)):
                        if self._game_board[start_column][start_row + square] != '_':
                            return False
                        else:
                            self._game_board[start_column][start_row] = '_'
                            self._game_board[end_column][end_row] = 'r'
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    for square in range(abs(column_result)):
                        if self._game_board[start_column][start_row + square] != '_':
                            return False
                        else:
                            captured_piece = self._game_board[end_column][end_row]
                            self._white_dict[captured_piece] -= 1
                            if self._white_dict[captured_piece] == 0:
                                self.set_game_state('BLACK_WON')

                            self._game_board[start_column][start_row] = '_'
                            self._game_board[end_column][end_row] = 'r'

                            return True
        else:                                                               #check column
            check_black = self._game_board[end_column][end_row].islower()  
            if check_black is True:
                return False
            else:
                if row_result < 0:   #moving left 
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(row_result)):
                            if self._game_board[start_column][start_row - pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'r'
                        return True
                    check_opponent = self._game_board[end_column][end_row].isupper()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row - pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._white_dict[captured_piece] -= 1
                        if self._white_dict[captured_piece] == 0:
                            self.set_game_state('BLACK_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'r'

                        return True
                else: #moving right
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row + pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'r'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].isupper()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row + pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._white_dict[captured_piece] -= 1
                        if self._white_dict[captured_piece] == 0:
                            self.set_game_state('BLACK_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'r'

                        return True

    def move_white_queen(self):
        # 'Q'
        # start: d1
        # open:
        #   bishop - col + open space row + open space (col +1, row+1)
        #   rook - col + open space OR row + open space
        # subsequent:
        #   bishop - col +/-1 open space, row +/- open space
        #   rook - col +/- open space OR row +/- open space
        # TODO
        pass

    def move_black_king(self, start_coord, end_coord):   # king not working
        # 'K'
        # start: e7
        # open: col +/-1, row + 1, col +/- 1 and row - 1
        # subsequent: col +/-1, row +/- 1, col +/- 1 and row +/- 1
        #       if not on edge
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if 0 >= end_column > 7 or 0 >= end_row > 7:
            return False
        
        if 1 > column_result > 2:
            return False
        
        if 1 > row_result > 2:
            return False
        
        if self._game_board[end_column][end_row] == '_':            # up, down
            if abs(column_result) == 1 and row_result == 0:
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'k'
                return True
            if column_result == 0 and abs(row_result) == 1:         # left, right
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'k'
                return True
            if abs(column_result) == 1 and abs(row_result) == 1:         # diagonal 
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'k'
                return True
            
        check_opponent = self._game_board[end_column][end_row].isupper()
        if check_opponent is True:
            captured_piece = self._game_board[end_column][end_row]
            self._white_dict[captured_piece] -= 1
            if self._white_dict[captured_piece] == 0:
                self.set_game_state('BLACK_WON')

            self._game_board[start_column][start_row] = '_'
            self._game_board[end_column][end_row] = 'k'

            return True
        else:
            return False


    def move_white_pawn(self, start_coord, end_coord):
        """
        checks if white pawn move is valid, if so moves the pawn and returns True, if not, returns False
        """
        # 'p'
        # start:  a7 - h7
        # open: row - 1 or - 2
        # subsequent: row - 1
        # capture: column +/- 1, row - 1
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if 1 >= column_result < -2:
            return False

        if start_column == 6:  # opening pawn move
            if column_result == -2 and row_result != 0:
                return False
            else:
                if self._game_board[start_column - 1][start_row] == '_':
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'P'
                    return True

            if column_result == -1 and self._game_board[end_column][end_row] == '_':
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'P'
                return True

        if column_result == -1 and abs(row_result) == 1:
            check_opponent = self._game_board[end_column][end_row].islower()  # capture
            if check_opponent is True:

                captured_piece = self._game_board[end_column][end_row]
                self._black_dict[captured_piece] -= 1
                if self._black_dict[captured_piece] == 0:
                    self.set_game_state('WHITE_WON')

                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'P'

                return True

        if column_result == -1 and self._game_board[end_row][end_column] == '_':
            self._game_board[start_column][start_row] = '_'
            self._game_board[end_column][end_row] = 'P'
            return True
        else:
            return False

    def move_white_knight(self, start_coord, end_coord):
        # 'n'
        # start b8, g8
        # open: col +/- 1 row + 2 or col +/- 2 row + 1;
        # subsequent: col +/- 1, row +/- 2 or col +/- 2 row +/- 1
        # no special capture
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if 0 >= column_result > 7 or 0 >= row_result > 7:
            return False
        
        if self._game_board[end_column][end_row] == '_':
            if abs(column_result) == 1 and abs(row_result) == 2:
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'N'
                return True
            if abs(column_result) == 2 and abs(row_result) == 1:
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'N'
                return True
        else:
            return False
        
        check_opponent = self._game_board[end_column][end_row].islower()
        if check_opponent is True:
                captured_piece = self._game_board[end_column][end_row]
                self._black_dict[captured_piece] -= 1
                if self._black_dict[captured_piece] == 0:
                    self.set_game_state('WHITE_WON')

                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'N'
        else: 
            return False
        
    def move_black_bishop(self):
        # 'b'
        # start: c8, f8
        # open: col +/- open space row - open space (col +/-1, row -1; 1:1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        pass

    def move_white_rook(self):
        # 'r'
        # start: a8, h8
        # open: col +/- open space OR row - open space
        # subsequent: col +/- open space OR row +/- open space
        # TODO
        pass

    def move_black_queen(self):
        # 'q'
        # start: d8
        # open:
        #   bishop - col +/- open space row - open space (col +/- 1, row+1)
        #   rook - col +/- open space OR row - open space
        # subsequent:
        #   bishop - col +/-1 open space, row +/- open space
        #   rook - col +/- open space OR row +/- open space
        # TODO
        pass

    def move_white_king(self, start_coord, end_coord):
        # 'K'
        # start: e1
        # open: col +/-1; row - 1, col +/- 1 and row + 1
        # subsequent: col +/-1, row +/- 1, col +/- 1 and row +/- 1
        #       if not on edge
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if 0 >= end_column > 7 or 0 >= end_row > 7: # already check this?
            return False
        
        if 1 > column_result > 2:
            return False
        
        if 1 > row_result > 2:
            return False
        
        if self._game_board[end_column][end_row] == '_':            # up, down
            if abs(column_result) == 1 and row_result == 0:
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'K'
                return True
            if column_result == 0 and abs(row_result) == 1:         # left, right
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'K'
                return True
            if abs(column_result) == 1 and abs(row_result) == 1:         # diagonal 
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'K'
                return True
            
        check_opponent = self._game_board[end_column][end_row].islower()
        if check_opponent is True:
            captured_piece = self._game_board[end_column][end_row]
            self._black_dict[captured_piece] -= 1
            if self._black_dict[captured_piece] == 0:
                self.set_game_state('WHITE_WON')

            self._game_board[start_column][start_row] = '_'
            self._game_board[end_column][end_row] = 'K'

            return True
        
        else:
            return False

    def make_board(self): # probably won't use
        """ create board for display"""
        board_size = self._board_size
        for row in range(board_size):
            board_row = []
            for column in range(board_size):
                board_row.append("_")
            self._game_board.append(board_row)
        self.set_white_pieces()
        self.set_black_pieces()
        return self._game_board
    def set_white_pieces(self): #probably won't use
        """ sets white pieces to proper locations """
        back_row = 0
        back_column = 0
        for number in range(self._board_size):
            if self._game_board[back_row][back_column] == '_':
                self._game_board[back_row][0] = 'R'
                self._game_board[back_row][1] = 'N'
                self._game_board[back_row][2] = 'B'
                self._game_board[back_row][3] = 'Q'
                self._game_board[back_row][4] = 'K'
                self._game_board[back_row][5] = 'B'
                self._game_board[back_row][7] = 'R'
                self._game_board[back_row][6] = 'N'

        # pawn
        front_row = 1
        front_column = 0
        for number in range(self._board_size):
            if self._game_board[front_row][front_column] == '_':
                self._game_board[front_row][front_column] = 'P'
                front_column += 1

    def set_black_pieces(self): # probably won't use
        """sets black pieces to proper locations"""
        back_row = 7
        back_column = 0
        for number in range(self._board_size):
            if self._game_board[back_row][back_column] == '_':
                self._game_board[back_row][0] = 'r'
                self._game_board[back_row][1] = 'n'
                self._game_board[back_row][2] = 'b'
                self._game_board[back_row][3] = 'q'
                self._game_board[back_row][4] = 'k'
                self._game_board[back_row][5] = 'b'
                self._game_board[back_row][7] = 'r'
                self._game_board[back_row][6] = 'n'

        # pawn
        front_row = 6
        front_column = 0
        for number in range(self._board_size):
            if self._game_board[front_row][front_column] == '_':
                self._game_board[front_row][front_column] = 'p'
                front_column += 1
def main():

    intial_board =[
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
    
    cv = ChessVar()
    #print(cv.convert_algebraic('b8'))
    print(cv.make_move('e2', 'f1'))

    #print(cv.make_move('a5', 'h5'))

    print(cv.make_move('h4', 'a4'))

   # print(cv.make_move('g7', 'g6'))

    #print(cv.make_move('e2', 'e4'))

   # print(cv.make_move('g8', 'f6'))

   # print(cv.make_move('e4', 'e5'))  # same black pawn not working

   # print(cv.make_move('b8', 'c6'))

   # print(cv.make_move('e5', 'f6'))

   # print(cv.make_move('c6', 'b8'))
    cv.print_board()

    print(cv._black_dict, cv._white_dict)


if __name__ == '__main__':
    main()