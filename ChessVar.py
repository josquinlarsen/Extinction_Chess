# Author: Josquin Larsen
# GitHub username: josquinlarsen
# Date: 18/nov/2023
# Description: Project 9: Portfolio Project - ChessVar.py - A variant of Extinction Chess where the winning player
# captures all the pieces of one type (e.g. all pawns (8), all knights (2), or the queen (1)). Pawn promotion,
# en passant, and castling are not allowed; check and checkmate are not considered; pieces move according to standard
# rules. White starts play by entering a start position and end position in algebraic notation (e.g. e2, e4), based on
# the standard chess board:  8 x 8 square grid; columns: from left to right, A - H;  rows: from bottom to top,  1 - 8.
# If the player enters an invalid move (either off the grid, against a piece's standard move - (e.g. a rook moving
# diagonally) - another of the player's pieces is in the end square, or a piece blocks the route to the destination) the
# program returns False. Player state will not change until the current player enters a valid move.  If the move is
# valid, the program will: move the piece (updating the starting location to an empty square and the end location to
# the piece that moved) ; capture an opponent's piece ; update the tally of pieces to reflect the capture (and if the
# move is a winning move, update the game state to the winning player) ; update the current player to the opponent ; and
# return True.

class ChessVar:
    """ a class to create an object of a ChessVar game"""

    def __init__(self):
        self._game_state = 'UNFINISHED'  # 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'
        self._move_state = 'WHITE'  # 'BLACK'
        self._game_board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

        self._white_dict = {'K': 1, 'Q': 1, 'R': 2, 'B': 2, 'N': 2, 'P': 8}
        self._black_dict = {'k': 1, 'q': 1, 'r': 2, 'b': 2, 'n': 2, 'p': 8}
        self._algebra_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def get_game_state(self):
        """ return game state """
        return self._game_state

    def set_game_state(self, game_state: str):
        """ set/update game state """
        self._game_state = game_state

    def get_move_state(self):
        """ return whose move it is """
        return self._move_state

    def set_move_state(self, player: str):
        """ update move state to 'WHITE' or 'BLACK' """
        self._move_state = player

    def convert_algebraic(self, position: str):
        """
        Method that takes a parameter of a string in algebraic notation (e.g. 'a7') and converts that
        to coordinates (0, 1). To align with a chess board the first coordinate refers to the columns
        A - H converted A = 0 to H = 7. Rows are in reverse order where '_1' = (_, 7) to '_8' = (_, 0)
        if a letter or number is out of bounds method returns -1 otherwise  returns tuple of  integer
        coordinates (0,1) tuple for unpacking as 2d array coordinates

        Returns (x, y)
        """
        letter_column = 0
        number_row = 0

        if len(position) != 2:  # out-of-bounds tests
            letter_column = -1
            return False

        check_alpha = position[0].isalpha()
        if check_alpha is False:
            letter_column = -1
            
        check_num = position[1].isdigit()
        if check_num is False:
            letter_column = -1

        if position[0] not in self._algebra_dict:
            letter_column = -1

        if letter_column < 0 or letter_column >= 8:
            letter_column = -1

        else:  # valid algebraic notation for conversion
            if position[0] in self._algebra_dict:
                letter_column += (self._algebra_dict[position[0]])
                number_row += 8 - (int(position[1]))

        return letter_column, number_row

    def make_move(self, start_pos: str, end_pos: str):
        """
        Method that takes two string parameters, starting and end positions in algebraic notation,
        checks the current game state ('UNFINISHED', 'WHITE_WON', 'BLACK_WON'), passes the algebraic notation for
        conversion, takes the returned tuple and unpacks that into 2d array notation (array[0][1] where [0]
        represents the letter column and [1] the row). If a position is out of bounds (-1), it returns False.

        It then checks move state (either 'WHITE' or 'BLACK') and proceeds to test legal moves -
        returning False if a move is invalid. If a move is valid, the start and end coordinates are passed to the
        check_white_move or check_black_move for further testing.

        If a move is valid, it returns True otherwise it returns False and the move state is not changed until a valid
        move is chosen.

        Returns True or False
        """
        start_coord = self.convert_algebraic(start_pos)
        end_coord = self.convert_algebraic(end_pos)

        if start_coord is False:
            return False
        if end_coord is False:
            return False

        start_row, start_column = start_coord
        end_row, end_column = end_coord

        start_square = self._game_board[start_column][start_row]

        if self._game_state != 'UNFINISHED':
            return False

        if -1 in start_coord or -1 in end_coord:  # check out-of-bounds move (e.g. a9 or i1)
            return False

        if self._move_state == 'WHITE':

            if start_square == '_':  # empty square
                return False

            if start_square.islower() is True:  # trying to move black piece
                return False

            check_white = self._game_board[end_column][end_row].isupper()  # end square is same player
            if check_white is True:
                return False

            valid_move_white = self.check_move(start_coord, end_coord)
            if valid_move_white is True:
                self.set_move_state('BLACK')
                return True

            return False

        if self._move_state == 'BLACK':

            if start_square == '_':  # empty square
                return False

            if start_square.isupper() is True:  # trying to move white piece
                return False

            check_black = self._game_board[end_column][end_row].islower()  # end square is same player
            if check_black is True:
                return False

            valid_move_black = self.check_move(start_coord, end_coord)
            if valid_move_black is True:
                self.set_move_state('WHITE')
                return True

            return False

    def print_board(self):
        """prints board in a 8x8 configuration"""
        for row in self._game_board:
            printed_row = ""
            for column in row:
                printed_row += column
            print(printed_row)

    def check_move(self, start_coord: tuple, end_coord: tuple):
        """
        Method which takes two parameters: the start and end coordinates converted in the make_move
        method. It then checks which piece is at the start location and passes the coordinates to the
        appropriate move_piece method for further move validation.

        Returns True or False depending on the return value of the move_piece method.
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        piece = self._game_board[start_column][start_row]

        if piece == 'p' or piece == 'P':
            return self.move_pawn(start_coord, end_coord)

        if piece == 'n' or piece == 'N':
            return self.move_knight(start_coord, end_coord)

        if piece == 'b' or piece == 'B':
            return self.move_bishop(start_coord, end_coord)

        if piece == 'r' or piece == 'R':
            return self.move_rook(start_coord, end_coord)

        if piece == 'q' or piece == 'Q':
            return self.move_queen(start_coord, end_coord)

        if piece == 'k' or piece == 'K':
            return self.move_king(start_coord, end_coord)

    def capture_piece(self, start_column: int, start_row: int, end_column: int, end_row: int):
        """
       Method which takes four parameters, the starting and end coordinates, and 'captures' opponent's
       piece, decrements the opponent's dictionary (which holds how many of each piece remain)  based on the piece
       captured. If the piece captured results in a win, updates game state to WHITE_WON or BLACK_WON.

       Updates starting square to empty, and end square to capturing piece

       Returns True or False
        """
        if self.get_move_state() == 'WHITE':
            captured_piece = self._game_board[end_column][end_row]
            self._black_dict[captured_piece] -= 1
            if self._black_dict[captured_piece] == 0:
                self.set_game_state('WHITE_WON')

            self._game_board[end_column][end_row] = self._game_board[start_column][start_row]
            self._game_board[start_column][start_row] = '_'

            return True

        if self.get_move_state() == 'BLACK':
            captured_piece = self._game_board[end_column][end_row]
            self._white_dict[captured_piece] -= 1
            if self._white_dict[captured_piece] == 0:
                self.set_game_state('BLACK_WON')

            self._game_board[end_column][end_row] = self._game_board[start_column][start_row]
            self._game_board[start_column][start_row] = '_'

            return True

        else:
            return False

    def move_pawn(self, start_coord: tuple, end_coord: tuple):
        """
        White Pawn: 'P', 8 | Black Pawn: 'p' 8
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position to
        the appropriate pawn. If a piece is captured, the opponents' dictionary is decremented by 1 for the
        corresponding piece. If the piece captured is the only piece or only remaining piece, the game state is
        updated to the winning current player

        Valid moves: - Destination square is empty '_'
                     - From starting square, can move forward one or two squares if no piece is blocking the path
                     - Subsequent moves after first square: can only move forward one square
                     - Cannot move diagonally, unless capturing opponent piece
                     - Cannot move backwards

        Capture:     - Can only capture on the forward left or right diagonal from the starting square

        If move is valid, returns True otherwise returns False
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if self.get_move_state() == 'WHITE':
            if column_result >= 0:
                return False

            if column_result < -2:
                return False

            if row_result != 0 and self._game_board[end_column][end_row] == '_':
                return False

            if start_column == 6:  # opening pawn move
                if column_result == -2 and row_result != 0:
                    return False

                if column_result == -2 and self._game_board[end_column][end_row] == '_':
                    if self._game_board[start_column - 1][start_row] == '_':
                        self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                            self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                        return True
                    else:
                        return False

        if self.get_move_state() == 'BLACK':
            if column_result <= 0:
                return False

            if column_result > 2:
                return False

            if row_result != 0 and self._game_board[end_column][end_row] == '_':
                return False

            if start_column == 1:  # opening pawn move
                if column_result == 2 and row_result != 0:
                    return False

                if column_result == 2 and self._game_board[end_column][end_row] == '_':
                    if self._game_board[start_column + 1][start_row] == '_':
                        self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                            self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                        return True
                    else:
                        return False

        if abs(column_result) == 1 and self._game_board[end_column][end_row] == '_':
            self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                self._game_board[end_column][end_row], self._game_board[start_column][start_row]
            return True

        if abs(column_result) == 1 and abs(row_result) == 1:
            return self.capture_piece(start_column, start_row, end_column, end_row)

        else:
            return False

    def move_knight(self, start_coord: tuple, end_coord: tuple):
        """
        White Knight:'N', 2 | Black Knight: 'n', 2
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position to
        the appropriate knight. If a piece is captured, the opponents' dictionary is decremented by 1 for the
        corresponding piece. If the piece captured is the only piece or only remaining piece, the game state is
        updated to the winning current player

        Valid moves: - End square is empty '_' or the opponent's piece
                     - End square is on the chess board
                     - Can move (L):
                            - forward one square, left or right two squares
                            - backward one square, left or right two squares
                            - forward two squares, left or right one square
                            - backward two squares, left or right one square

        Capture:     - Opponent's piece on end square

        If move is valid, returns True otherwise returns False
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) > 2 or abs(row_result) > 2:
            return False

        if self._game_board[end_column][end_row] == '_':
            if abs(column_result) == 1 and abs(row_result) == 2:
                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            if abs(column_result) == 2 and abs(row_result) == 1:
                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True
            else:
                return False

        end_square = self._game_board[end_column][end_row]
        if end_square != '_':
            return self.capture_piece(start_column, start_row, end_column, end_row)

    def move_bishop(self, start_coord: tuple, end_coord: tuple):
        """
        White bishop: 'B', 2 | Black bishop: 'b', 2
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position
        to the appropriate bishop. If a piece is captured, the opponents' dictionary is decremented by 1 for the
        corresponding piece. If the piece captured is the only piece or only remaining piece, the game state is
        updated to the current player won.

        Valid moves: - End square is empty '_' or the opponent's piece, there are no pieces blocking route
                     - End square is on the chess board
                     - Can move diagonally forwards or backwards:

        Capture:     - Opponent's piece on end square

        If move is valid, returns True otherwise returns False
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) == 0 and abs(row_result) != 0:  # vertical/horizontal check
            return False
        if abs(column_result) != 0 and abs(row_result) == 0:
            return False

        if abs(column_result) != abs(row_result):
            return False

        if column_result > 0 and row_result < 0:  # moving down + left
            if self._game_board[end_column][end_row] == '_':
                pos = 1
                for _ in range(abs(column_result)):
                    if self._game_board[start_column + pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            end_square = self._game_board[end_column][end_row]
            if end_square != '_':
                pos = 1
                for _ in range(abs(column_result) - 1):
                    if self._game_board[start_column + pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

        if column_result > 0 and row_result > 0:  # moving down + right
            if self._game_board[end_column][end_row] == '_':
                pos = 1
                for _ in range(abs(column_result)):
                    if self._game_board[start_column + pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            end_square = self._game_board[end_column][end_row]
            if end_square != '_':
                pos = 1
                for _ in range(abs(column_result) - 1):
                    if self._game_board[start_column + pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

        if column_result < 0 and row_result < 0:  # moving up + left
            if self._game_board[end_column][end_row] == '_':
                pos = 1
                for _ in range(abs(column_result) - 1):
                    if self._game_board[start_column - pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            end_square = self._game_board[end_column][end_row]
            if end_square != '_':
                pos = 1
                for _ in range(abs(column_result) - 1):
                    if self._game_board[start_column - pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

        else:  # moving up and right                                       #check column
            if self._game_board[end_column][end_row] == '_':
                pos = 1
                for _ in range(abs(row_result)):
                    if self._game_board[start_column - pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            end_square = self._game_board[end_column][end_row]
            if end_square != '_':
                pos = 1
                for _ in range(abs(row_result) - 1):
                    if self._game_board[start_column - pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

    def move_rook(self, start_coord: tuple, end_coord: tuple):
        """
        White Rook, 'R', 2 | Black Rook: 'r', 2
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position
        to the appropriate rook. If a piece is captured, the opponents' dictionary is decremented by 1 for the
        corresponding piece. If the piece captured is the only piece or only remaining piece, the game state is
        updated to the current player won.

        Valid moves: - End square is empty '_' or the opponent's piece, there are no pieces blocking route
                     - End square is on the chess board
                     - Can move horizontally and vertically forwards and backwards:

        Capture:     - Opponent's piece on end square

        If move is valid, returns True otherwise returns False
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) > 0 and abs(row_result) > 0:  # diagonal check
            return False

        if row_result == 0:  # check_row
            if column_result < 0:  # moving up
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column - pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                end_square = self._game_board[end_column][end_row]
                if end_square != '_':
                    pos = 1
                    for _ in range(abs(column_result) - 1):
                        if self._game_board[start_column - pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

            else:  # moving down
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result) - 1):
                        if self._game_board[start_column + pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                end_square = self._game_board[end_column][end_row]
                if end_square != '_':
                    pos = 1
                    for _ in range(abs(column_result) - 1):
                        if self._game_board[start_column + pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

        else:  # check column
            if row_result < 0:  # moving left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(row_result)):
                        if self._game_board[start_column][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                end_square = self._game_board[end_column][end_row]
                if end_square != '_':
                    pos = 1
                    for _ in range(abs(row_result) - 1):
                        if self._game_board[start_column][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

            else:  # moving right
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(row_result) - 1):
                        if self._game_board[start_column][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                end_square = self._game_board[end_column][end_row]
                if end_square != '_':
                    pos = 1
                    for _ in range(abs(row_result) - 1):
                        if self._game_board[start_column][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

    def move_queen(self, start_coord: tuple, end_coord: tuple):
        """
        White Queen, 'Q', 1 | Black Queen: 'q', 1
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position to
        appropriate queen. If a piece is captured, the opponents' dictionary is decremented by 1 for the
        corresponding piece. If the piece captured is the only piece or only remaining piece, the game state is
        updated to the current player won.

        Valid moves: - End square is empty '_' or the opponent's piece, there are no pieces blocking route
                     - End square is on the chess board
                     - Can move (within the range of the board):
                                - horizontally or vertically, forwards and backwards
                                - diagonally forwards or backwards

        Capture:     - Opponent's piece on end square

        If move is valid, returns True otherwise returns False
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) == abs(row_result):  # bishop functionality
            return self.move_bishop(start_coord, end_coord)

        # rook functionality
        if (row_result == 0 and abs(column_result) > 0) or (abs(row_result) > 0 and column_result == 0):
            return self.move_rook(start_coord, end_coord)

        else:
            return False

    def move_king(self, start_coord: tuple, end_coord: tuple):
        """
        White King, 'K', 1 | Black King: 'k', 1
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position to
        the appropriate king. If a piece is captured, the opponents' dictionary is decremented by 1 for the
        corresponding piece. If the piece captured is the only piece or only remaining piece, the game state is
        updated to current player won.

        Valid moves: - End square is empty '_' or the opponent's piece, there are no pieces blocking route
                     - End square is on the chess board
                     - Can move one square:
                                - horizontally or vertically, forwards and backwards
                                - diagonally forwards or backwards

        Capture:     - Opponent's piece on end square

        If move is valid, returns True otherwise returns False
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) > 1:
            return False
        if abs(row_result) > 1:
            return False

        if abs(column_result) == abs(row_result):  # bishop functionality
            return self.move_bishop(start_coord, end_coord)

        # rook functionality
        if (row_result == 0 and abs(column_result) > 0) or (abs(row_result) > 0 and column_result == 0):
            return self.move_rook(start_coord, end_coord)

        else:
            return False

def main():
    initial_board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

    cv = ChessVar()

    cv.make_move('e2', 'e4')
    cv.make_move('d7', 'd5')
    cv.make_move('b1', 'c3')
    cv.make_move('d5', 'e4')
    cv.print_board()


if __name__ == '__main__':
    main()