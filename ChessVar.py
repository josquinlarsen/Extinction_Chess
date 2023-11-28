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
        self._game_board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
                            ['_', 'P', 'p', '_', '_', '_', 'p', 'N'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', 'Q', '_', '_', '_', '_'],
                            ['_', 'R', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', 'P', '_', 'K', '_', 'P', 'P'],
                            ['r', 'N', 'B', 'q', '_', '_', '_', 'R']]  

        self._white_dict = {'K': 1, 'Q': 1, 'R': 2, 'B': 2, 'N': 2, 'P': 8}
        self._black_dict = {'k': 1, 'q': 1, 'r': 2, 'b': 2, 'n': 2, 'p': 8}
        self._algebra_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def get_game_state(self):
        """return game state"""
        return self._game_state

    def set_game_state(self, game_state: str):
        """set/update game state"""
        self._game_state = game_state

    def get_move_state(self):
        """ return whose move it is"""
        return self._move_state

    def set_move_state(self, player:str):
        """update move state to 'WHITE' or 'BLACK' """
        self._move_state = player

    def convert_algebraic(self, position: str):
        """
        Method that takes a parameter of a string in algebraic notation (e.g. 'a7') and converts that 
        to coordinates (0, 1). To align with a chess board the first coordinate refers to the columns 
        A - H converted A = 0 to H = 7. Rows are in reverse order where '_1' = (_, 7) to '_8' = (_, 0)
        if a letter or number is out of bounds method returns -1 otherwise  returns coordinates (0,1)
        tuple for unpacking as 2d array coordinates
        """
        letter_column = 0
        number_row = 0

        if len(position) != 2:                  # out-of-bounds tests
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

        else:                                   # valid algebraic notation for conversion
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
        """
        start_coord = self.convert_algebraic(start_pos)
        end_coord = self.convert_algebraic(end_pos)
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        square = self._game_board[start_column][start_row]

        if self._game_state != 'UNFINISHED':
            return False

        if -1 in start_coord or -1 in end_coord:  # check out-of-bounds move (e.g. a9 or i1)
            return False

        if self._move_state == 'WHITE':
            if square == '_':  # empty square
                return False
            if square.islower() is True:  # trying to move black piece
                return False

            valid_move_white = self.check_white_move(start_coord, end_coord)
            if valid_move_white is False:
                return False
            
            self.set_move_state('BLACK')
           
            return True

        if self._move_state == 'BLACK':
            if square == '_': # empty square
                return False
            if square.isupper() is True: # trying to move white piece
                return False
            
            valid_move_black = self.check_black_move(start_coord, end_coord) 
            if valid_move_black is False:
                return False
            
            self.set_move_state('WHITE')

            return True

    def print_board(self):
        """prints board in a 8x8 configuration"""
        for row in self._game_board:
            printed_row = ""
            for column in row:
                printed_row += column
            print(printed_row)

    def check_white_move(self, start_coord, end_coord):
        """
        Method which takes two parameters: the start and end coordinates converted in the make_move
        method. It then checks which piece is at the start location and passes the coordinates to the
        appropriate move_white_'PIECE' for further move validation. 

        Returns True or False depending on the return value of the move_white_'PIECE' method.
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        piece = self._game_board[start_column][start_row]

        if piece == 'P':
            return self.move_white_pawn(start_coord, end_coord)

        if self._game_board[start_column][start_row] == 'N':
            return self.move_white_knight(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'B':
            return self.move_white_bishop(start_coord, end_coord)

        if self._game_board[start_column][start_row] == 'R':
            return self.move_white_rook(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'Q':
            return self.move_white_queen(start_coord, end_coord)

        if piece == 'K':
            return self.move_white_king(start_coord, end_coord)

    def check_black_move(self, start_coord, end_coord):
        """        
        Method which takes two parameters: the start and end coordinates converted in the make_move
        method. It then checks which piece is at the start location and passes the coordinates to the
        appropriate move_black_'PIECE' for further move validation. 

        Returns True or False depending on the return value of the move_black_'PIECE' method.
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        piece = self._game_board[start_column][start_row]

        if piece == 'p':
            return self.move_black_pawn(start_coord, end_coord)

        if piece == 'n':
            return self.move_black_knight(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'b':
            return self.move_black_bishop(start_coord, end_coord)

        if self._game_board[start_column][start_row] == 'r':
            return self.move_black_rook(start_coord, end_coord)
        
        if self._game_board[start_column][start_row] == 'q':
            return self.move_black_queen(start_coord, end_coord)

        if piece == 'k':
            return self.move_black_king(start_coord, end_coord)

    def move_black_pawn(self, start_coord, end_coord):
        """
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid 
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position to 'p'
        for black pawn. If a piece is captured, the opponents' dictionary is decremented by 1 for the corresponding piece
        If the piece captured is the only piece or only remaining piece, the game state is updated to 'BLACK_WON'
        
        Valid moves: - Destination square is empty '_'
                     - From starting square, can move forward one or two squares if no piece is blocking the path 
                     - Subsequent moves after first sqaure: can only move forward one square
                     - Cannot move diagonally, unless capturing opponent piece
                     - Cannot move backwards

        Capture:     - Can only capture on the forward left or right diagonal from the starting square

        If move is vaild, returns True otherwise returns False                     
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if column_result <= 0:
            return False
        
        if column_result > 2:
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
            else:
                return False

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

    def move_black_bishop(self, start_coord, end_coord):
        # 'B'
        # start: c1, f1
        # open: col +open space row + open space (col +1, row+1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) == 0 and abs(row_result) != 0: #vert/horz check
            return False
        if abs(column_result) != 0 and abs(row_result) == 0:
            return False
        
        if abs(column_result) != abs(row_result):
            return False

        #if column_result > 0:                             
        check_black = self._game_board[end_column][end_row].islower()  
        if check_black is True:
            return False
        else:
            if column_result > 0 and row_result < 0:   #moving down + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'
                    return True
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'

                    return True
                
            if column_result > 0 and row_result > 0:   #moving down + right
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'
                    return True
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'

                    return True
            if column_result < 0 and row_result < 0 : #moving up + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'
                    return True
                    
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'

                    return True

            else:                        # moving up and right                                       #check column
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(row_result)):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'
                    return True
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(row_result)-1):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'b'

                    return True

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

        if abs(column_result) > 0 and abs(row_result) > 0: #diagonal check
            return False
            
        if row_result == 0:                             # check_row
            check_black = self._game_board[end_column][end_row].islower()  
            if check_black is True:
                return False
            else:
                if column_result < 0:   #moving up
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'r'
                        return True
                    check_opponent = self._game_board[end_column][end_row].isupper()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column - pos][start_row] == '_':
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
                else: #moving down
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'r'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].isupper()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
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

    def move_black_queen(self, start_coord, end_coord):
        # 'q' bishop + rook 
        # start: d8
        # open:
        #   bishop - col + open space row + open space (col +1, row+1)
        #   rook - col + open space OR row + open space
        # subsequent:
        #   bishop - col +/-1 open space, row +/- open space
        #   rook - col +/- open space OR row +/- open space
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        check_black = self._game_board[end_column][end_row].islower()  
        if check_black is True:
            return False
        
        if abs(column_result) == abs(row_result): #bishop functionality 
            if column_result > 0 and row_result < 0:   #moving down + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'
                    return True
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'

                    return True
                
            if column_result > 0 and row_result > 0:   #moving down + right
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'
                    return True
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'

                    return True
            if column_result < 0 and row_result < 0 : #moving up + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'
                    return True
                    
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'

                    return True

            else:                        # moving up and right                                       #check column
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(row_result)):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'
                    return True
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(row_result)-1):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._white_dict[captured_piece] -= 1
                    if self._white_dict[captured_piece] == 0:
                        self.set_game_state('BLACK_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'q'

                    return True
                
        # rook functionality   
        if (row_result == 0 and abs(column_result) > 0) or (abs(row_result) > 0 and column_result == 0): 
            if row_result == 0:                             # check_row
                if column_result < 0:   #moving up
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'q'
                        return True
                    check_opponent = self._game_board[end_column][end_row].isupper()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._white_dict[captured_piece] -= 1
                        if self._white_dict[captured_piece] == 0:
                            self.set_game_state('BLACK_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'q'

                        return True
                else: #moving down
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'q'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].isupper()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._white_dict[captured_piece] -= 1
                        if self._white_dict[captured_piece] == 0:
                            self.set_game_state('BLACK_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'q'

                        return True
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
                        self._game_board[end_column][end_row] = 'q'
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
                        self._game_board[end_column][end_row] = 'q'

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
                        self._game_board[end_column][end_row] = 'q'
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
                        self._game_board[end_column][end_row] = 'q'

                        return True
        else:
            return False
        
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
        White Pawn: 'P'
        Method which takes two parameters, the converted start and end coordinates, and tests if a move is valid 
        or invalid. If a move is valid it changes the start position to an empy square '_' and the end position to 'P'
        for white pawn. If a piece is captured, the opponent's dictionary is decremented by 1 for the corresponding piece.
        If the piece captured is the only piece or only remaining piece, the game state is updated to 'WHITE_WON'
        
        Valid moves: - Destination square is empty '_'
                     - From starting square, can move forward one or two squares if no piece is blocking the path 
                     - Subsequent moves after first square: can only move forward one square
                     - Cannot move diagonally, unless capturing opponent piece
                     - Cannot move backwards

        Capture:     - Can only capture on the forward left or right diagonal from the starting square

        If move is vaild, returns True otherwise returns False
        """
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
        
    def move_white_bishop(self, start_coord, end_coord):
        # 'b'
        # start: c8, f8
        # open: col +/- open space row - open space (col +/-1, row -1; 1:1)
        # subsequent: col +/-1 open space, row +/- open space
        # have to check for blocks
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) == 0 and abs(row_result) != 0: #vert/horz check
            return False
        if abs(column_result) != 0 and abs(row_result) == 0:
            return False
        
        if abs(column_result) != abs(row_result):
            return False

        #if column_result > 0:                             
        check_white = self._game_board[end_column][end_row].isupper()  
        if check_white is True:
            return False
        else:
            if column_result > 0 and row_result < 0:   #moving down + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'
                    return True
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'

                    return True
                
            if column_result > 0 and row_result > 0:   #moving down + right
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'
                    return True
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'

                    return True
            if column_result < 0 and row_result < 0 : #moving up + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'
                    return True
                    
                check_opponent = self._game_board[end_column][end_row].isupper()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'

                    return True

            else:                        # moving up and right                                       #check column
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(row_result)):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'
                    return True
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(row_result)-1):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'B'

                    return True

    def move_white_rook(self, start_coord, end_coord):
        # 'R'
        # start: a1, h1
        # open: col +/- open space OR row - open space
        # subsequent: col +/- open space OR row +/- open space
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        if abs(column_result) > 0 and abs(row_result) > 0: #diagonal check
            return False
            
        if row_result == 0:                             # check_row
            check_white = self._game_board[end_column][end_row].isupper()  
            if check_white is True:
                return False
            else:
                if column_result < 0:   #moving up
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'R'
                        return True
                    
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'R'

                        return True
                else: #moving down
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'R'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'R'

                        return True
    
        else:                                                               #check column
            check_white = self._game_board[end_column][end_row].isupper()  
            if check_white is True:
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
                        self._game_board[end_column][end_row] = 'R'
                        return True
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row - pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'R'

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
                        self._game_board[end_column][end_row] = 'R'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row + pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'R'

                        return True

    def move_white_queen(self, start_coord, end_coord):
        # 'Q'
        # start: d1
        # open:
        #   bishop - col +/- open space row - open space (col +/- 1, row+1)
        #   rook - col +/- open space OR row - open space
        # subsequent:
        #   bishop - col +/-1 open space, row +/- open space
        #   rook - col +/- open space OR row +/- open space
        # TODO
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        check_white = self._game_board[end_column][end_row].isupper()  
        if check_white is True:
            return False
        
        if abs(column_result) == abs(row_result): #bishop functionality 
            if column_result > 0 and row_result < 0:   #moving down + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'
                    return True
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'

                    return True
                
            if column_result > 0 and row_result > 0:   #moving down + right
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'
                    return True
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column + pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'

                    return True
            if column_result < 0 and row_result < 0 : #moving up + left
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'
                    return True
                    
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(column_result)-1):
                        if self._game_board[start_column - pos][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'

                    return True

            else:                        # moving up and right                                       #check column
                if self._game_board[end_column][end_row] == '_':
                    pos = 1
                    for _ in range(abs(row_result)):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'
                    return True
                check_opponent = self._game_board[end_column][end_row].islower()
                if check_opponent is True:
                    pos = 1
                    for _ in range(abs(row_result)-1):
                        if self._game_board[start_column - pos][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False
                
                    captured_piece = self._game_board[end_column][end_row]
                    self._black_dict[captured_piece] -= 1
                    if self._black_dict[captured_piece] == 0:
                        self.set_game_state('WHITE_WON')

                    self._game_board[start_column][start_row] = '_'
                    self._game_board[end_column][end_row] = 'Q'

                    return True
                
        # rook functionality   
        if (row_result == 0 and abs(column_result) > 0) or (abs(row_result) > 0 and column_result == 0): 
            if row_result == 0:                             # check_row
                if column_result < 0:   #moving up
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'Q'
                        return True
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column - pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'Q'

                        return True
                else: #moving down
                    if self._game_board[end_column][end_row] == '_':
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'Q'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(column_result)-1):
                            if self._game_board[start_column + pos][start_row] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'Q'

                        return True
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
                        self._game_board[end_column][end_row] = 'Q'
                        return True
                    
                    check_opponent = self._game_board[end_column][end_row].lower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row - pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'Q'

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
                        self._game_board[end_column][end_row] = 'Q'
                        return True
                        
                    check_opponent = self._game_board[end_column][end_row].islower()
                    if check_opponent is True:
                        pos = 1
                        for _ in range(abs(row_result)-1):
                            if self._game_board[start_column][start_row + pos] == '_':
                                pos += 1
                            else:
                                return False
                    
                        captured_piece = self._game_board[end_column][end_row]
                        self._black_dict[captured_piece] -= 1
                        if self._black_dict[captured_piece] == 0:
                            self.set_game_state('WHITE_WON')

                        self._game_board[start_column][start_row] = '_'
                        self._game_board[end_column][end_row] = 'Q'

                        return True
        else:
            return False

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


def main():

    initial_board =[
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
    print(cv.make_move('g2', 'g4'))
    print(cv.get_game_state())

    #print(cv.make_move('d5', 'd5'))

    #print(cv.make_move('a1', 'a3'))

    #print(cv.make_move('g2', 'g3'))

    #print(cv.make_move('b5', 'b4'))

    #print(cv.make_move('g3', 'h4'))

   # print(cv.make_move('b4', 'b3'))  
   # print(cv.make_move('b8', 'c6'))

   # print(cv.make_move('e5', 'f6'))

   # print(cv.make_move('c6', 'b8'))
    cv.print_board()

    print(cv._black_dict, cv._white_dict)


if __name__ == '__main__':
    main()