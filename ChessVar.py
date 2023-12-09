# Author: Josquin Larsen
# GitHub username: josquinlarsen
# Date: 9/dec/2023
# Description: Extinction_Chess - A variant of chess where the winning player captures all the pieces of one type
#             (e.g. all pawns (8), all knights (2), or the queen (1)). En passant, and castling are not allowed; 
#             check and checkmate are not considered; pieces move according to standard rules. White starts play by 
#             entering a start position and end position in algebraic notation (e.g. e2, e4), based on the standard 
#             chess board: 8 x 8 square grid; columns: from left to right, A - H;  rows: from bottom to top,  1 - 8.
#
#             If the player enters an invalid move (either off the grid, against a piece's standard move - (e.g. a 
#             rook moving diagonally) - another of the player's pieces is in the end square, or a piece blocks the 
#             route to the destination) the program returns False. Player state will not change until the current 
#             player enters a valid move.  If the move is valid, the program will: move the piece (updating the starting 
#             location to an empty square and the end location to the piece that moved) ; capture an opponent's piece;
#             update the tally of pieces to reflect the capture (and if the move is a winning move, update the game state
#             to the winning player) ; update the current player to the opponent ; and return True. 
#
#             Displays unicode chess piece during game play.

class ChessVar:
    """ a class to create an object of a ChessVar game"""

    def __init__(self):
        self._game_state = 'UNFINISHED'  # 'UNFINISHED', 'WHITE_WON', 'BLACK_WON'
        self._move_state = 'WHITE'  # 'BLACK'
        self._game_board = [['\u265c', '\u265e', '\u265d', '\u265b', '\u265a', '\u265d', '\u265e', '\u265c'],
                            ['\u265f', '\u265f', '\u265f', '\u265f', '\u265f', '\u265f', '\u265f', '\u265f'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['_', '_', '_', '_', '_', '_', '_', '_'],
                            ['\u2659', '\u2659', '\u2659', '\u2659', '\u2659', '\u2659', '\u2659', '\u2659'],
                            ['\u2656', '\u2658', '\u2657', '\u2655', '\u2654', '\u2657', '\u2658', '\u2656']]

        self._algebra_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self._tally_dict = {'WHITE': {'\u2654': 1, '\u2655': 1, '\u2656': 2, '\u2657': 2, '\u2658': 2, '\u2659': 8}, 
                            'BLACK': {'\u265a': 1, '\u265b': 1, '\u265c': 2, '\u265d': 2, '\u265e': 2, '\u265f': 8}}
        self._pieces = {'WHITE': {'king': '\u2654', 'queen': '\u2655', 'rook': '\u2656', 'bishop': '\u2657', 'knight': '\u2658', 'pawn': '\u2659'},
                        'BLACK': {'king': '\u265a', 'queen': '\u265b', 'rook': '\u265c', 'bishop': '\u265d', 'knight': '\u265e', 'pawn': '\u265f'}}

    def get_game_state(self) -> str:
        """ return game state """
        return self._game_state

    def set_game_state(self, game_state: str):
        """ set/update game state """
        self._game_state = game_state

    def get_move_state(self) -> str:
        """ return whose move it is """
        return self._move_state

    def set_move_state(self, player: str):
        """ update move state to 'WHITE' or 'BLACK' """
        self._move_state = player

    def play_chess(self):
        """ simulates turn-based game play """

        start_move = False
        end_move = False
        valid_move = False

        current_player = self.get_move_state()
        print(f"\n{current_player}'s move")

        while valid_move is False:
            while start_move is False:
                start_input = str(input('Please enter your starting move (e.g. a2): '))
                start_pos = self.convert_algebraic(start_input)
                if start_pos is False:
                    start_input
                    
                start_move = True

            while end_move is False:
                end_input = str(input('Please enter your end move (e.g. a4): '))
                end_pos = self.convert_algebraic(end_input)
                if end_pos is False:
                    end_input
                
                end_move = True 

            move = self.make_move(start_pos, end_pos)
            if move is True:
                valid_move = True
            else:
                print("Invalid move, try again")
                self.play_chess()

        self.print_board()
        self.print_tally()

        start_move = False
        end_move = False

        if self.get_game_state()!= 'UNFINISHED':
            valid_move = False
            print(f"{self.get_game_state()}")       

        valid_move = False
        self.play_chess()                

    def convert_algebraic(self, position: str) -> tuple[int, int] | bool:
        """
        Method that takes a parameter of a string in algebraic notation (e.g. 'a7') and converts that
        to coordinates (0, 1). To align with a chess board the first coordinate refers to the columns
        A - H converted A = 0 to H = 7. Rows are in reverse order where '_1' = (_, 7) to '_8' = (_, 0)
        if a letter or number is out of bounds, method returns False otherwise returns tuple of integer
        coordinates (0,1) for unpacking as 2d array coordinates.

        Returns (x, y) or False
        """
        letter_column = 0
        number_row = 0

        if len(position) != 2:  # out-of-bounds tests
            return False

        check_alpha = position[0].isalpha()
        if check_alpha is False:
            return False
        
        alpha_lower = position[0].lower()

        check_num = position[1].isdigit()
        if check_num is False:
            return False

        if alpha_lower not in self._algebra_dict:
            return False

        if alpha_lower in self._algebra_dict:            # valid algebraic notation for conversion
            letter_column += (self._algebra_dict[alpha_lower])
            number_row += 8 - (int(position[1]))

        if (number_row < 0) or (number_row > 7):
            return False

        return letter_column, number_row

    def make_move(self, start_pos: str, end_pos: str) -> bool:
        """
        Method that takes two string parameters, starting and end positions in algebraic notation,
        checks the current game state ('UNFINISHED', 'WHITE_WON', 'BLACK_WON'), passes the algebraic notation for
        conversion, takes the returned tuple and unpacks that into 2d array notation (array[0][1] where [0]
        represents the letter column and [1] the row). If a position is out of bounds, returns False.

        It then checks move state (either 'WHITE' or 'BLACK') and proceeds to test legal moves -
        returning False if a move is invalid. If a move is valid, the start and end coordinates are passed to the
        check_white_move or check_black_move for further testing.

        If a move is valid, it returns True otherwise it returns False and the move state is not changed until a valid
        move is chosen.

        Returns True or False
        """
       # start_coord = self.convert_algebraic(start_pos)
       # end_coord = self.convert_algebraic(end_pos)
        start_coord = start_pos
        end_coord = end_pos

        if start_coord is False:  # check out-of-bounds move (e.g. a9 or i1) before unpacking
            return False
        if end_coord is False:
            return False

        start_row, start_column = start_coord
        end_row, end_column = end_coord

        start_square = self._game_board[start_column][start_row]
        end_square = self._game_board[end_column][end_row]

        if self._game_state != 'UNFINISHED':
            return False

        if start_coord == end_coord:
            return False

        if self._move_state == 'WHITE':

            if start_square == '_':  # empty square
                return False
            
            if start_square in self._pieces['BLACK']:
                return False
            
            if end_square in self._pieces['WHITE'].values():
                return False

            valid_move_white = self.check_move(start_coord, end_coord)
            if valid_move_white is True:
                self.set_move_state('BLACK')
                return True

            return False

        if self._move_state == 'BLACK':

            if start_square == '_':  # empty square
                return False

            if start_square in self._pieces['WHITE']:
                return False

            if end_square in self._pieces['BLACK'].values():
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

    def print_tally(self):
        """ prints tally dictionary"""

        for player in self._tally_dict:
            print(f'\n{player:^1}')
            for piece in self._tally_dict[player]:
                print(f'{piece:^1} : {self._tally_dict[player][piece]:^1}')
                
    def check_move(self, start_coord: tuple, end_coord: tuple) -> bool:
        """
        Method which takes two parameters: the start and end coordinates converted in the make_move
        method. It then checks which piece is at the start location and passes the coordinates to the
        appropriate move_piece method for further move validation.

        Returns True or False depending on the return value of the move_piece method.
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord
        piece = self._game_board[start_column][start_row]
        player = self.get_move_state()
        
        if piece == self._pieces[player]['pawn']:
            return self.move_pawn(start_coord, end_coord)
        
        if piece == self._pieces[player]['knight']:
            return self.move_knight(start_coord, end_coord)
        
        if piece == self._pieces[player]['bishop']:
            return self.move_bishop(start_coord, end_coord)
        
        if piece == self._pieces[player]['rook']:
             return self.move_rook(start_coord, end_coord)
        
        if piece == self._pieces[player]['queen']:
            return self.move_queen(start_coord, end_coord)
        
        if piece == self._pieces[player]['king']:
            return self.move_king(start_coord, end_coord)
            
    def capture_piece(self, start_column: int, start_row: int, end_column: int, end_row: int) -> bool:
        """
       Method which takes four parameters, the starting and end coordinates, and 'captures' opponent's
       piece, decrements the opponent's dictionary (which holds how many of each piece remain)  based on the piece
       captured. If the piece captured results in a win, updates game state to WHITE_WON or BLACK_WON.

       Updates starting square to empty, and end square to capturing piece

       Returns True or False
        """
        if self.get_move_state() == 'WHITE':
            captured_piece = self._game_board[end_column][end_row]
            self._tally_dict['BLACK'][captured_piece] -= 1
            if self._tally_dict['BLACK'][captured_piece] == 0:
                self.set_game_state('WHITE_WON')
         
            self._game_board[end_column][end_row] = self._game_board[start_column][start_row]
            self._game_board[start_column][start_row] = '_'

            return True

        if self.get_move_state() == 'BLACK':
            captured_piece = self._game_board[end_column][end_row]
           
            self._tally_dict['WHITE'][captured_piece] -= 1
            if self._tally_dict['WHITE'][captured_piece] == 0:
                self.set_game_state('BLACK_WON')
     
            self._game_board[end_column][end_row] = self._game_board[start_column][start_row]
            self._game_board[start_column][start_row] = '_'

            return True

        return False

    def pawn_promotion(self, start_coord: tuple, end_coord: tuple):
        """ 
        Method which allows a player to promote pawn to a queen, rook, knight, or bishop, once that pawn
        reaches the final row (row 8 for white, row 1 for black); updates piece counts accordingly. 

        If player promotes their last pawn, game status is updated to a win for the opposing player. 
        """
        start_row, start_column = start_coord
        end_row, end_column = end_coord

        row_result = end_row - start_row
        column_result = end_column - start_column

        valid_input_white = False
        valid_input_black = False

        white_promotion = {'queen': '\u2655', 'rook': '\u2656', 'bishop': '\u2657', 'knight': '\u2658'}
        black_promotion = {'queen': '\u265b', 'rook': '\u265c', 'bishop': '\u265d', 'knight': '\u265e'}
        promo_list = ['queen', 'rook', 'bishop', 'knight']
        
        if (abs(column_result) == 1) and (abs(row_result) == 1):

            if self.get_move_state() == 'WHITE':
                captured_piece = self._game_board[end_column][end_row]
                self._tally_dict['BLACK'][captured_piece] -= 1
                if self._tally_dict['BLACK'][captured_piece] == 0:
                    self.set_game_state('WHITE_WON')

                print("\nPawn Promotion")                   # pawn promotion 
                for idx, piece in enumerate(promo_list):
                    print(f"{idx + 1}.{piece}")
                
                while valid_input_white is False:
                    user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    if  (user_input > 3)or (user_input < 0): 
                        user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    else: 
                        valid_input_white = True

                if user_input in range(len(promo_list)):
                    new_piece = promo_list[user_input]
                    self._game_board[end_column][end_row] = white_promotion[new_piece]
                    self._game_board[start_column][start_row] = '_'

                    self._tally_dict['WHITE'][self._game_board[end_column][end_row]] += 1
                    self._tally_dict['WHITE']['\u2659'] -= 1

                    if self._tally_dict['WHITE']['\u2659'] == 0:
                        self.set_game_state('BLACK_WON')

                    valid_input_white = False
                    return True
                
            if self.get_move_state() == 'BLACK':
                captured_piece = self._game_board[end_column][end_row]
            
                self._tally_dict['WHITE'][captured_piece] -= 1
                if self._tally_dict['WHITE'][captured_piece] == 0:
                    self.set_game_state('BLACK_WON')

                print("\nPawn Promotion")
                for idx, piece in enumerate(promo_list):
                    print(f"{idx + 1}.{piece}")
                
                while valid_input_black is False:
                    user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    if  (user_input > 3)or (user_input < 0): 
                        user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    else: 
                        valid_input_black = True

                if user_input in range(len(promo_list)):
                    new_piece = promo_list[user_input]
                    self._game_board[end_column][end_row] = black_promotion[new_piece]
                    self._game_board[start_column][start_row] = '_'

                    self._tally_dict['BLACK'][self._game_board[end_column][end_row]] += 1
                    self._tally_dict['BLACK']['\u265f'] -= 1

                    if self._tally_dict['BLACK']['\u265f'] == 0:
                        self.set_game_state('WHITE_WON')

                    valid_input_black = False
                    return True
                   
        else:
            if self.get_move_state() == 'WHITE':
        
                print("\nPawn Promotion")
                for idx, piece in enumerate(promo_list):
                    print(f"{idx + 1}.{piece}")

                while valid_input_white is False:
                    user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    if  (user_input > 3)or (user_input < 0): 
                        user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    else: 
                        valid_input_white = True

                if user_input in range(len(promo_list)):
                    new_piece = promo_list[user_input]
                    self._game_board[end_column][end_row] = white_promotion[new_piece]
                    self._game_board[start_column][start_row] = '_'

                    self._tally_dict['WHITE'][self._game_board[end_column][end_row]] += 1
                    self._tally_dict['WHITE']['\u2659'] -= 1

                    if self._tally_dict['WHITE']['\u2659'] == 0:
                        self.set_game_state('BLACK_WON')

                    valid_input_white = False
                    return True
                
            if self.get_move_state() == 'BLACK':
        
                print("\nPawn Promotion")
                for idx, piece in enumerate(promo_list):
                    print(f"{idx + 1}.{piece}")
                
                while valid_input_black is False:
                    user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    if  (user_input > 3)or (user_input < 0): 
                        user_input = int(input("Please choose the piece you want by selecting the number: ")) - 1
                    else: 
                        valid_input_black = True

                if user_input in range(len(promo_list)):
                    new_piece = promo_list[user_input]
                    self._game_board[end_column][end_row] = black_promotion[new_piece]
                    self._game_board[start_column][start_row] = '_'

                    self._tally_dict['BLACK'][self._game_board[end_column][end_row]] += 1
                    self._tally_dict['BLACK']['\u265f'] -= 1

                    if self._tally_dict['BLACK']['\u265f'] == 0:
                        self.set_game_state('WHITE_WON')

                    valid_input_black = False
                    return True

    def move_pawn(self, start_coord: tuple, end_coord: tuple) -> bool:
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

        end_square = self._game_board[end_column][end_row]

        if self.get_move_state() == 'WHITE':
            if (column_result >= 0) or (column_result < -2):
                return False

            if (row_result != 0) and (end_square == '_'):
                return False

            if start_column == 6:  # opening pawn move
                if (column_result == -2) and (row_result != 0):
                    return False

                if (column_result == -2) and (end_square == '_'):
                    if self._game_board[start_column - 1][start_row] == '_':
                        self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                            self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                        return True

                    return False

        if self.get_move_state() == 'BLACK':
            if (column_result <= 0) or (column_result > 2):
                return False

            if (row_result != 0) and (end_square == '_'):
                return False

            if start_column == 1:  # opening pawn move
                if (column_result == 2) and (row_result != 0):
                    return False

                if (column_result == 2) and (end_square == '_'):
                    if self._game_board[start_column + 1][start_row] == '_':
                        self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                            self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                        return True

                    return False

        if (end_column == 0) or (end_column == 7):
            return self.pawn_promotion(start_coord, end_coord)
            
        if (abs(column_result) == 1) and (end_square == '_'):
            self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                self._game_board[end_column][end_row], self._game_board[start_column][start_row]
            return True

        if (abs(column_result) == 1) and (abs(row_result) == 1):
            return self.capture_piece(start_column, start_row, end_column, end_row)

        return False

    def move_knight(self, start_coord: tuple, end_coord: tuple) -> bool:
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

        row_result = abs(end_row - start_row)
        column_result = abs(end_column - start_column)

        end_square = self._game_board[end_column][end_row]

        if (column_result > 2) or (row_result > 2):
            return False

        if end_square == '_':
            if (column_result == 1) and (row_result == 2):
                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            if (column_result == 2) and (row_result == 1):
                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            return False

        if end_square != '_':
            return self.capture_piece(start_column, start_row, end_column, end_row)

    def move_bishop(self, start_coord: tuple, end_coord: tuple) -> bool:
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

        end_square = self._game_board[end_column][end_row]
        pos = 1

        if (column_result == 0) or (row_result == 0):  # vertical/horizontal check
            return False

        if abs(column_result) != abs(row_result):
            return False

        if (column_result > 0) and (row_result < 0):  # moving down + left
            if end_square == '_':
                for idx in range(abs(column_result)):
                    if self._game_board[start_column + pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            if end_square != '_':
                for idx in range(abs(column_result) - 1):
                    if self._game_board[start_column + pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

        if (column_result > 0) and (row_result > 0):  # moving down + right
            if end_square == '_':
                for idx in range(abs(column_result)):
                    if self._game_board[start_column + pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            if end_square != '_':
                for idx in range(abs(column_result) - 1):
                    if self._game_board[start_column + pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

        if (column_result < 0) and (row_result < 0):  # moving up + left
            if end_square == '_':
                for idx in range(abs(column_result) - 1):
                    if self._game_board[start_column - pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            if end_square != '_':
                for idx in range(abs(column_result) - 1):
                    if self._game_board[start_column - pos][start_row - pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

        else:  # moving up and right                                       #check column
            if end_square == '_':
                for idx in range(abs(row_result)):
                    if self._game_board[start_column - pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                    self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                return True

            if end_square != '_':
                for idx in range(abs(row_result) - 1):
                    if self._game_board[start_column - pos][start_row + pos] == '_':
                        pos += 1
                    else:
                        return False

                return self.capture_piece(start_column, start_row, end_column, end_row)

    def move_rook(self, start_coord: tuple, end_coord: tuple) -> bool:
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

        end_square = self._game_board[end_column][end_row]
        pos = 1

        if (abs(column_result) > 0) and (abs(row_result) > 0):  # diagonal check
            return False

        if row_result == 0:  # check_row

            if column_result < 0:  # moving up
                if end_square == '_':
                    for idx in range(abs(column_result)):
                        if self._game_board[start_column - pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                if end_square != '_':
                    for idx in range(abs(column_result) - 1):
                        if self._game_board[start_column - pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

            else:  # moving down
                if end_square == '_':
                    for idx in range(abs(column_result) - 1):
                        if self._game_board[start_column + pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                if end_square != '_':
                    for idx in range(abs(column_result) - 1):
                        if self._game_board[start_column + pos][start_row] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

        else:  # check column
            if row_result < 0:  # moving left
                if end_square == '_':
                    for idx in range(abs(row_result)):
                        if self._game_board[start_column][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                if end_square != '_':
                    for idx in range(abs(row_result) - 1):
                        if self._game_board[start_column][start_row - pos] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

            else:  # moving right
                if end_square == '_':
                    for idx in range(abs(row_result) - 1):
                        if self._game_board[start_column][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False

                    self._game_board[start_column][start_row], self._game_board[end_column][end_row] = \
                        self._game_board[end_column][end_row], self._game_board[start_column][start_row]
                    return True

                if end_square != '_':
                    for idx in range(abs(row_result) - 1):
                        if self._game_board[start_column][start_row + pos] == '_':
                            pos += 1
                        else:
                            return False

                    return self.capture_piece(start_column, start_row, end_column, end_row)

    def move_queen(self, start_coord: tuple, end_coord: tuple) -> bool:
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

        row_result = abs(end_row - start_row)
        column_result = abs(end_column - start_column)

        bishop = self.move_bishop(start_coord, end_coord)
        rook = self.move_rook(start_coord, end_coord)
        diagonal = (column_result == row_result)

        return bishop if diagonal else rook

    def move_king(self, start_coord: tuple, end_coord: tuple) -> bool:
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

        row_result = abs(end_row - start_row)
        column_result = abs(end_column - start_column)

        bishop = self.move_bishop(start_coord, end_coord)
        rook = self.move_rook(start_coord, end_coord)
        diagonal = (column_result == row_result)

        if (column_result > 1) or (row_result > 1):
            return False

        return bishop if diagonal else rook

def main():
    
    intial_board_uni = [
        ['\u265c', '\u265e', '\u265d', '\u265b', '\u265a', '\u265d', '\u265e', '\u265c'],
        ['\u265f', '\u265f', '\u265f', '\u265f', '\u265f', '\u265f', '\u265f', '\u265f'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['\u2659', '\u2659', '\u2659', '\u2659', '\u2659', '\u2659', '\u2659', '\u2659'],
        ['\u2656', '\u2658', '\u2657', '\u2655', '\u2654', '\u2657', '\u2658', '\u2656']]

    cv = ChessVar()
    cv.print_board()
    cv.play_chess()


if __name__ == '__main__':
    main()
