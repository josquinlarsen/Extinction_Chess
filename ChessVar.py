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
        row = 0
        column = 0
        for character in position:
            letter = character.lower()
            if position[0] not in self._algebra_dict or int(position[1]) > 8:
                return False
            else:
                if letter in self._algebra_dict:
                    row += (self._algebra_dict[letter])
                    column += (int(position[1])) - 1

        return row, column

    def make_move(self, start_pos: str, end_pos: str):
        """return False if move is illegal, or game is already won"""
        if self._game_state != 'UNFINISHED':
            return False


    def make_board(self):
        """ create board for display"""
        board_size = self._board_size
        for row in range(board_size):
            board_row = []
            for column in range(board_size):
                board_row.append("_")
            self._game_board.append(board_row)

    def print_board(self):
        """print nice board"""
        for row in self._game_board:
            printed_row = "  "
            for column in row:
                printed_row += column
            print(printed_row)

    # TODO

    def move_white_pawn(self):
        # start:  a2 - h2
        # open: row +1 or +2
        # subsequent: row +1
        # capture: column +/- 1, row +1
        # TODO : check edges ?
        pass

    def move_white_knight(self):
        # start b1, g1
        # open: col +/- 1 row + 2 or col +/- 2 row + 1;
        # subsequent: col +/- 1, row +/- 2 or col +/- 2 row +/- 1
        # no special capture
        # TODO
        pass

    def move_white_bishop(self):
        # start: c1, f1
        # open: col +open space row + open space (col +1, row+1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        pass

    def move_white_rook(self):
        # start: a1, h1
        # open: col + open space OR row + open space
        # subsequent: col +/- open space OR row +/- open space
        # TODO
        pass

    def move_white_queen(self):
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
        # start: e1
        # open: col +/-1, row + 1, col +/- 1 and row - 1
        # subsequent: col +/-1, row +/- 1, col +/- 1 and row +/- 1
        #       if not on edge
        # TODO
        pass

    def move_black_pawn(self):
        # start:  a7 - h7
        # open: row - 1 or - 2
        # subsequent: row - 1
        # capture: column +/- 1, row - 1
        # TODO : check edges ?
        pass

    def move_black_knight(self):
        # start b8, g8
        # open: col +/- 1 row + 2 or col +/- 2 row + 1;
        # subsequent: col +/- 1, row +/- 2 or col +/- 2 row +/- 1
        # no special capture
        # TODO
        pass

    def move_black_bishop(self):
        # start: c8, f8
        # open: col +/- open space row - open space (col +/-1, row -1; 1:1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        pass

    def move_black_rook(self):
        # start: a8, h8
        # open: col +/- open space OR row - open space
        # subsequent: col +/- open space OR row +/- open space
        # TODO
        pass

    def move_black_queen(self):
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
        # start: e8
        # open: col +/-1; row - 1, col +/- 1 and row + 1
        # subsequent: col +/-1, row +/- 1, col +/- 1 and row +/- 1
        #       if not on edge
        # TODO
        pass

def main():
    cv = ChessVar()
    cv.make_board()
    cv.print_board()
    print(cv.convert_algebraic('b8'))


if __name__ == '__main__':
    main()