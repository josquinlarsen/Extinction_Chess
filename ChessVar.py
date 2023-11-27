# Author: Josquin Larsen
# GitHub username: josquinlarsen
# Date: 18/nov/2023
# Description: Project 9: Portfolio Project - ChessVar.py -

class ChessVar:
    """ a class to create an object of a ChessVar game"""

    def __init__(self):
        self._game_state = 'UNFINISHED'  # 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'
        self._board_size = 8
        self._game_board = []  # list?
        self._white_dict = {'K': 1, 'Q': 1, 'R': 2, 'B': 2, 'N': 2, 'P': 8}
        self._black_dict = {'k': 1, 'q': 1, 'r': 2, 'b': 2, 'n': 2, 'p': 8}
        self._algebra_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self._move_state = 'WHITE'  # 'BLACK'
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
        for character in position:
            letter = character.lower()
            if position[0] not in self._algebra_dict or letter_column < 0 or letter_column >= 8:
                return False
            else:
                if letter in self._algebra_dict:
                    letter_column += (self._algebra_dict[letter])
                    number_row += (int(position[1])) - 1

        return letter_column, number_row

    def make_move(self, start_pos: str, end_pos: str):
        """return False if move is illegal, or game is already won"""
        #self.make_board()
        if self._game_state != 'UNFINISHED':
            return False

        start_coord = self.convert_algebraic(start_pos)
        end_coord = self.convert_algebraic(end_pos)
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        if start_coord is False or end_coord is False:  # check out-of-bounds move (e.g. a9 or i1)
            return False

        if self._move_state == 'WHITE':
            if self._game_board[start_column][start_row] == '_':  # empty square
                return False
            if self._game_board[start_column][start_row].islower() is True:  # trying to move black piece
                return False
            valid_move = (self.check_white_move(start_coord, end_coord))
            if valid_move is True:
                self.set_move_state('BLACK')
                self.inc_white_counter()
                return self._game_board
            else:
                return False

        if self._move_state == 'BLACK':
            if self._game_board[start_column][start_row] == '_': # empty square
                return False
            if self._game_board[start_column][start_row].isupper() is True: # trying to move white piece
                return False
            if self._game_board[end_column][end_row] != '_':
                return False
            if self._game_board[end_column][end_row].islower() is True:
                return False

    def make_board(self):
        """ create board for display"""
        board_size = self._board_size
        for row in range(board_size):
            board_row = []
            for column in range(board_size):
                board_row.append("_")
            self._game_board.append(board_row)
        self.set_white_pieces()
        self.set_black_pieces()

    def print_board(self):
        """print nice board"""
        for row in self._game_board:
            printed_row = ""
            for column in row:
                printed_row += column
            print(printed_row)

    def set_white_pieces(self):
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

    def set_black_pieces(self):
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

    def check_white_move(self, start_coord, end_coord):
        """check if white move is valid"""
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        if self._game_board[start_column][start_row] == 'P':
            row_result = end_row - start_row
            column_result = end_column - start_column
            if self._white_counter == 1: # opening pawn move
                if column_result == 2 and row_result != 0:
                    return False
                else:
                    if self._game_board[start_column + 1][start_row + 1] == '_':
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'P'
                        return True

                if column_result == 1 and self._game_board[end_column][end_row] == '_':
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'P'
                    return True

            if column_result == 1 and row_result >= abs(1) and self._game_board[end_column][end_row].islower(): # capture

                captured_piece = self._game_board[end_column][end_row]
                self._black_dict[captured_piece] -= 1
                if self._black_dict[captured_piece] == 0:
                    self.set_game_state('WHITE_WON')

                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'P'

                return True

            if column_result == 1 and self._game_board[end_row][end_column] == '_':
                self._game_board[start_column][start_row] = '_'
                self._game_board[end_column][end_row] = 'P'
                return True
            else:
                return False
        if self._game_board[start_column][start_row] == 'N':
            pass
        if self._game_board[start_column][start_row] == 'B':
            pass
        if self._game_board[start_column][start_row] == 'R':
            pass
        if self._game_board[start_column][start_row] == 'Q':
            pass
        if self._game_board[start_column][start_row] == 'K':
            pass


    def check_black_move(self, start_coord, end_coord):
        """check if black move is valid"""
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        if self._game_board[start_column][start_row] == 'p':
            pass
        if self._game_board[start_column][start_row] == 'n':
            pass
        if self._game_board[start_column][start_row] == 'b':
            pass
        if self._game_board[start_column][start_row] == 'r':
            pass
        if self._game_board[start_column][start_row] == 'q':
            pass
        if self._game_board[start_column][start_row] == 'k':
            pass


    #USE THESE INSTEAD OF MOVE?


    def move_white_pawn(self):
        # 'P'
        # start:  a2 - h2
        # open: row +1 or +2
        # subsequent: row +1
        # capture: column +/- 1, row +1
        # TODO
        pass

    def move_white_knight(self):
        # 'N'
        # start b1, g1
        # open: col +/- 1 row + 2 or col +/- 2 row + 1;
        # subsequent: col +/- 1, row +/- 2 or col +/- 2 row +/- 1
        # no special capture
        # TODO
        pass

    def move_white_bishop(self):
        # 'B'
        # start: c1, f1
        # open: col +open space row + open space (col +1, row+1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        pass

    def move_white_rook(self):
        # 'R'
        # start: a1, h1
        # open: col + open space OR row + open space
        # subsequent: col +/- open space OR row +/- open space
        # TODO
        pass

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

    def move_white_king(self):
        # 'K'
        # start: e1
        # open: col +/-1, row + 1, col +/- 1 and row - 1
        # subsequent: col +/-1, row +/- 1, col +/- 1 and row +/- 1
        #       if not on edge
        # TODO
        pass

    def move_black_pawn(self):
        # 'p'
        # start:  a7 - h7
        # open: row - 1 or - 2
        # subsequent: row - 1
        # capture: column +/- 1, row - 1
        # TODO
        pass

    def move_black_knight(self):
        # 'n'
        # start b8, g8
        # open: col +/- 1 row + 2 or col +/- 2 row + 1;
        # subsequent: col +/- 1, row +/- 2 or col +/- 2 row +/- 1
        # no special capture
        # TODO
        pass

    def move_black_bishop(self):
        # 'b'
        # start: c8, f8
        # open: col +/- open space row - open space (col +/-1, row -1; 1:1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        pass

    def move_black_rook(self):
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

    def move_black_king(self):
        # 'k'
        # start: e8
        # open: col +/-1; row - 1, col +/- 1 and row + 1
        # subsequent: col +/-1, row +/- 1, col +/- 1 and row +/- 1
        #       if not on edge
        # TODO
        pass

def main():
    cv = ChessVar()
    cv.make_board()

    #print(cv.convert_algebraic('b8'))
    print(cv.make_move('e2', 'e3'))
    cv.print_board()


if __name__ == '__main__':
    main()