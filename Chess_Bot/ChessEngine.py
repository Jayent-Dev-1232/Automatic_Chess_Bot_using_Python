"""
This class is responsible for storing all the information about the current state of the game. It also
will be responsible for determining valid moves at the current state of the game. It will keep the log of the moves.
"""
import numpy as np


class GameState():
    def __init__(self):
        # Board is a 2D array of size 8X8 and each element of the list has two characters.
        # The first character represents the color of the piece 'w' for white and 'b' for black.
        # The second characters represents the type of the piece 'R' for Rook, 'N' for Knight, 'B' for Bishop, 'Q' for Queen, 'K' for King and 'p' for pawn.
        # '--' denote the empty space in the 2D array of board.
        self.board = np.full((8, 8), '', dtype='<U2')
        self.board[0] = ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR']
        self.board[1] = ['bp']*8
        self.board[2:6] = ['--']*8
        self.board[6] = ['wp']*8
        self.board[7] = ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']

        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves, 'B': self.get_bishop_moves, 'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.whiteToMove = True
        self.moveLog = []

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    """
    This function undo the last move made when called.
    """
    def undo_move(self):
        # Make sure that there is any move to undo.
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            # Reverses the turn back
            self.whiteToMove = not self.whiteToMove

    """
    All moves considering checks.
    """
    def get_valid_moves(self):
        return self.get_all_possible_moves()

    """
    All moves without considering checks.
    """
    def get_all_possible_moves(self):
        moves = []
        # Number of rows
        for r in range(len(self.board)):
            # Number of columns in a particular row
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove) :
                    piece = self.board[r][c][1]
                    # Calls the appropriate move function based on piece type.
                    self.move_functions[piece](r, c, moves)

        return moves

    """
    Get all the pawn moves for the pawn located at (row, column) and these moves to the list.
    """
    def get_pawn_moves(self, r, c, moves):
        # When there is white's turn.
        if self.whiteToMove:
            # This code is for 1 square move.
            if self.board[r-1][c] == '--':
                moves.append(Move((r, c), (r-1, c), self.board))
                # This code is for 2 square move and is done for the first move only for that pawn.
                if r == 6 and self.board[r-2][c] == '--':
                    moves.append(Move((r, c), (r-2, c), self.board))

            # White pawn captures black pawn on the left side.
            if c-1 >= 0:
                # Confirms that the enemy piece is black.
                if self.board[r-1][c-1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c-1), self.board))

            # White pawn captures black pawn on the right side.
            if c+1 <=7:
                # Confirms that the enemy piece is black.
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        # When there is black's turn.
        else:
            # This code is for 1 square move.
            if self.board[r+1][c] == '--':
                moves.append(Move((r, c), (r+1, c), self.board))
                # This code is for 2 square move and is done for the first move only for that pawn.
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r, c), (r+2, c), self.board))

            # Black pawn captures white pawn on the right side.
            if c-1 >= 0:
                # Confirms that the enemy piece is white.
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))

            # Black pawn captures white pawn on the left side.
            if c+1 <= 7:
                # Confirms that the enemy piece is white.
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    """
    Get all the rook moves for the rook located at (row, column) and these moves to the list.
    """
    def get_rook_moves(self, r, c, moves):
        # When there is white's turn
        if self.whiteToMove:
            # When white rook is moving upwards.
            if r-1 >= 0:
                for i in range(r-1, -1, -1):
                    # If the upper square is empty then add it in the valid moves list.
                    if self.board[i][c] == '--':
                        moves.append(Move((r, c), (i, c), self.board))

                    # If upper square is not empty.
                    if self.board[i][c] != '--':
                        # If the piece in the upper square is black then capture that piece.
                        if self.board[i][c][0] == 'b':
                            moves.append(Move((r, c), (i, c), self.board))

                        # If the piece in the upper square is white then break out of the for loop.
                        if self.board[i][c][0] == 'w':
                            break

            # When white rook is moving leftwards.
            if c-1 >= 0:
                for i in range(c-1, -1, -1):
                    # If the left square is empty then add it in the valid moves list.
                    if self.board[r][i] == '--':
                        moves.append(Move((r, c), (r, i), self.board))

                    # If left square is not empty.
                    if self.board[r][i] != '--':
                        # If the piece in the left square is black then capture that piece.
                        if self.board[r][i][0] == 'b':
                            moves.append(Move((r, c), (r, i), self.board))

                        # If the piece in the left square is white then break out of the for loop.
                        if self.board[r][i][0] == 'w':
                            break

            # When white rook is moving rightwards.
            if c+1 <= 7:
                for i in range(c+1, 8):
                    # If the right square is empty then add it in the valid moves list.
                    if self.board[r][i] == '--':
                        moves.append(Move((r, c), (r, i), self.board))

                    # If right square is not empty.
                    if self.board[r][i] != '--':
                        # If the piece in the right square is black then capture that piece.
                        if self.board[r][i][0] == 'b':
                            moves.append(Move((r, c), (r, i), self.board))

                        # If the piece in the right square is white then break out of the for loop.
                        if self.board[r][i][0] == 'w':
                            break

            # When white rook is moving downwards.
            if r+1 <= 7:
                for i in range(r+1, 8):
                    # If the lower square is empty then add it in the valid moves list.
                    if self.board[i][c] == '--':
                        moves.append(Move((r, c), (i, c), self.board))

                    # If lower square is not empty.
                    if self.board[i][c] != '--':
                        # If the piece in the lower square is black then capture that piece.
                        if self.board[i][c][0] == 'b':
                            moves.append(Move((r, c), (i, c), self.board))

                        # If the piece in the lower square is white then break out of the for loop.
                        if self.board[i][c][0] == 'w':
                            break
        # When there is black's turn
        else:
            # When black rook is moving downwards.
            if r - 1 >= 0:
                for i in range(r - 1, -1, -1):
                    # If the lower square is empty then add it in the valid moves list.
                    if self.board[i][c] == '--':
                        moves.append(Move((r, c), (i, c), self.board))

                    # If lower square is not empty.
                    if self.board[i][c] != '--':
                        # If the piece in the lower square is white then capture that piece.
                        if self.board[i][c][0] == 'w':
                            moves.append(Move((r, c), (i, c), self.board))

                        # If the piece in the lower square is black then break out of the for loop.
                        if self.board[i][c][0] == 'b':
                            break

            # When black rook is moving rightwards.
            if c - 1 >= 0:
                for i in range(c - 1, -1, -1):
                    # If the right square is empty then add it in the valid moves list.
                    if self.board[r][i] == '--':
                        moves.append(Move((r, c), (r, i), self.board))

                    # If right square is not empty.
                    if self.board[r][i] != '--':
                        # If the piece in the right square is white then capture that piece.
                        if self.board[r][i][0] == 'w':
                            moves.append(Move((r, c), (r, i), self.board))

                        # If the piece in the right square is black then break out of the for loop.
                        if self.board[r][i][0] == 'b':
                            break

            # When black rook is moving leftwards.
            if c + 1 <= 7:
                for i in range(c + 1, 8):
                    # If the left square is empty then add it in the valid moves list.
                    if self.board[r][i] == '--':
                        moves.append(Move((r, c), (r, i), self.board))

                    # If left square is not empty.
                    if self.board[r][i] != '--':
                        # If the piece in the left square is white then capture that piece.
                        if self.board[r][i][0] == 'w':
                            moves.append(Move((r, c), (r, i), self.board))

                        # If the piece in the left square is black then break out of the for loop.
                        if self.board[r][i][0] == 'b':
                            break

            # When black rook is moving upwards.
            if r + 1 <= 7:
                for i in range(r + 1, 8):
                    # If the upper square is empty then add it in the valid moves list.
                    if self.board[i][c] == '--':
                        moves.append(Move((r, c), (i, c), self.board))

                    # If upper square is not empty.
                    if self.board[i][c] != '--':
                        # If the piece in the upper square is white then capture that piece.
                        if self.board[i][c][0] == 'w':
                            moves.append(Move((r, c), (i, c), self.board))

                        # If the piece in the upper square is black then break out of the for loop.
                        if self.board[i][c][0] == 'b':
                            break

    """
    Get all the knight moves for the knight located at (row, column) and these moves to the list.
    """
    def get_knight_moves(self, r, c, moves):
        # When there is white's turn.
        if self.whiteToMove:
            # When knight is moving on the inner left side.
            if c-1 >= 0:
                # When the knight is making move to the up on the inner left side.
                if r-2 >= 0:
                    if self.board[r-2][c-1] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r-2, c-1), self.board))

                    if self.board[r-2][c-1][0] == 'b':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r - 2, c - 1), self.board))

                # When the knight is making move to the down on the inner left side.
                if r+2 <=7:
                    if self.board[r+2][c-1] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r+2, c-1), self.board))

                    if self.board[r+2][c-1][0] == 'b':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+2, c-1), self.board))

            # When the knight is moving on the outer left side.
            if c-2 >= 0:
                # When knight is making move to the up on the outer left side.
                if r-1 >= 0:
                    if self.board[r-1][c-2] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r-1, c-2), self.board))

                    if self.board[r-1][c-2][0] == 'b':
                        # If there is an enemy piece at the square then capture that
                        moves.append(Move((r, c), (r-1, c-2), self.board))

                # When the knight is making move to the down on the outer left side.
                if r+1 <= 7:
                    if self.board[r+1][c-2] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r+1, c-2), self.board))

                    if self.board[r+1][c-2][0] == 'b':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+1, c-2), self.board))

            # When the knight is moving on the inner right side.
            if c+1 <= 7:
                # When the knight is making move to the up on the inner right side.
                if r-2 >= 0:
                    if self.board[r-2][c+1] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r-2, c+1), self.board))

                    if self.board[r-2][c+1][0] == 'b':
                        # If there is an enemy piece at the square then capture that
                        moves.append(Move((r, c), (r-2, c+1), self.board))

                # When the knight is making move to the down on the inner right side.
                if r+2 <= 7:
                    if self.board[r+2][c+1] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r+2, c+1), self.board))

                    if self.board[r+2][c+1][0] == 'b':
                        # If there is an enemy piece at the square then capture that
                        moves.append(Move((r, c), (r+2, c+1), self.board))

            # When the knight is moving on the outer right side.
            if c+2 <= 7:
                # When the knight is making move to the up on the outer right side.
                if r-1 >= 0:
                    if self.board[r-1][c+2] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r-1, c+2), self.board))

                    if self.board[r-1][c+2][0] == 'b':
                        # If there is an enemy piece at the square then capture that
                        moves.append(Move((r, c), (r-1, c+2), self.board))

                # When the knight is making move to the down on the outer right side.
                if r+1 <= 7:
                    if self.board[r+1][c+2] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r+1, c+2), self.board))

                    if self.board[r+1][c+2][0] == 'b':
                        # If there is an enemy piece at the square then capture that
                        moves.append(Move((r, c), (r+1, c+2), self.board))

        # When there is black's turn
        else:
            # When knight is moving on the inner right side.
            if c-1 >= 0:
                # When the knight is making move to the down on the inner right side.
                if r-2 >= 0:
                    if self.board[r-2][c-1] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r-2, c-1), self.board))

                    if self.board[r-2][c-1][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r - 2, c - 1), self.board))

                # When the knight is making move to the up on the inner right side.
                if r+2 <=7:
                    if self.board[r+2][c-1] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r+2, c-1), self.board))

                    if self.board[r+2][c-1][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+2, c-1), self.board))

            # When knight is moving on the outer right side.
            if c-2 >= 0:
                # When the knight is making move to the down on the outer right side.
                if r-1 >= 0:
                    if self.board[r-1][c-2] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r-1, c-2), self.board))

                    if self.board[r-1][c-2][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+2, c-1), self.board))

                # When the knight is making move to the up on the outer right side.
                if r+1 <= 7:
                    if self.board[r+1][c-2] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r+1, c-2), self.board))

                    if self.board[r+1][c-2][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+1, c-2), self.board))

            # When knight is moving on the inner left side.
            if c+1 <= 7:
                # When the knight is making move to the down on the inner left side.
                if r-2 >= 0:
                    if self.board[r-2][c+1] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r-2, c+1), self.board))

                    if self.board[r-2][c+1][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r-2, c+1), self.board))

                # When the knight is making move to the up on the outer right side.
                if r+2 <= 7:
                    if self.board[r+2][c+1] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r+2, c+1), self.board))

                    if self.board[r+2][c+1][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+2, c+1), self.board))

            # When knight is moving on the outer left side.
            if c+2 <= 7:
                # When the knight is making move to the down on the outer left side.
                if r-1 >= 0:
                    if self.board[r-1][c+2] == '--':
                        # If the square is empty then append that move in the list.
                        moves.append(Move((r, c), (r-1, c+2), self.board))

                    if self.board[r-1][c+2][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r-1, c+2), self.board))

                # When the knight is making move to the up on the outer left side.
                if r+1 <= 7:
                    if self.board[r+1][c+2] == '--':
                        # If the square in empty then append that move in the list.
                        moves.append(Move((r, c), (r+1, c+2), self.board))

                    if self.board[r+1][c+2][0] == 'w':
                        # If there is an enemy piece at the square then capture that.
                        moves.append(Move((r, c), (r+1, c+2), self.board))

    """
    Get all the bishop moves for the bishop located at (row, column) and these moves to the list.
    """
    def get_bishop_moves(self, r, c, moves):
        # Defining the directions in which it moves.
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        # Make the enemy according to the move a piece.
        enemy_color = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                end_row = r + d[0]*i
                end_col = c + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    # If the end square is empty then append that move in the list.
                    if end_piece == "--":
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # If the piece at the end square is enemy piece then capture that.
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    """
    Get all the queen moves for the queen located at (row, column) and these moves to the list.
    """
    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)

    """
    Get all the king moves for the king located at (row, column) and these moves to the list.
    """
    def get_king_moves(self, r, c, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.whiteToMove else "b"
        for i in range(8):
            end_row = r + king_moves[i][0]
            end_col = c + king_moves[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

class Move():
    # Maps key to values.
    # Key : Value
    ranks_to_rows = {"1" :7, "2" :6, "3" :5, "4" :4, "5" :3, "6" :2, "7" :1, "8" :0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a" :0, "b" :1, "c" :2, "d" :3, "e" :4, "f" :5, "g" :6, "h" :7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}


    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    """
    Overriding the equals method.
    """
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]