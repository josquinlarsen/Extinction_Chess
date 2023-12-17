# Extinction_Chess
Allows two players to play Extinction Chess. Written in Python

Portfolio Project for CS162 (Intro to Computer Science II) Fall 2023

A variant of chess where the winning player must capture all the pieces of one type
(e.g. all pawns (8), all knights (2), or the queen (1)). En passant, and castling are not allowed; 
check and checkmate are not considered; pieces move according to standard rules. White starts play by 
entering a start position and end position in algebraic notation (e.g. e2, e4) based on the standard 
chess board: 8 x 8 square grid; columns: from left to right, A - H;  rows: from bottom to top,  1 - 8.

If the player enters an invalid move (either off the grid, against a piece's standard move - (e.g. a 
rook moving diagonally) - another of the player's pieces is in the end square, or a piece blocks the 
route to the destination) the program returns False. Player state does not change until the current 
player enters a valid move.  If the move is valid, the program will: move the piece (updating the starting 
location to an empty square and the end location to the piece that moved) ; capture an opponent's piece (if necessary);
update the tally of pieces to reflect the capture (and if the move is a winning move, update the game state
to the winning player) ; update the current player to the opponent ; and return True.

If pawn promotion causes the player to no longer have any pawns, game state is updated to a win for the opponent. 

**Added Pawn Promotion, real-time play ability, unicode piece representation beyond original specifications
