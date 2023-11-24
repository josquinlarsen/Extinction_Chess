# Author: Josquin Larsen
# GitHub username: josquinlarsen
# Date: 18/nov/2023
# Description: Project 9: Portfolio Project - ChessVar.py -

class ChessVar:
    """ a class to create an object of a ChessVar game"""

    def __init__(self):
        self._game_state = 'UNFINISHED' # UNFINISHED, WHITE_WON, BLACK_WON
        self._game_board = None  # list?
        self._white_dict = {'K': 1, 'Q': 1, 'R': 2, 'B': 2, 'N': 2, 'P': 8}
        self._black_dict = {'k': 1, 'q': 1, 'r': 2, 'b': 2, 'n': 2, 'p': 8}

    def get_game_state(self):
        """return game state"""
        return self.get_game_state()

    def set_game_state(self, game_state):
        """set/update game state"""
        self._game_state = game_state

    def make_move(self, start_pos, end_pos):
        """return False if move is illegal, or game is already won"""
        pass

    # TODO


    def move_pawn(self):
        # TODO : check edges ?
        pass

    def move_knight(self):
        # TODO
        pass

    def move_bishop(self):
        # TODO
        pass

    def move_rook(self):
        # TODO
        pass

    def move_queen(self):
        # TODO
        pass

    def move_king(self):
        # TODO
        pass

