"""Core game logic for Connect4"""

from constants import ROWS, COLS, PLAYER1_PIECE, PLAYER2_PIECE


class Connect4Game:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        """Create empty game board"""
        return [[0 for _ in range(COLS)] for _ in range(ROWS)]

    def copy_board(self):
        """Create a copy of current board"""
        return [row[:] for row in self.board]

    def reset_board(self):
        """Reset the game board"""
        self.board = self.create_board()

    def drop_piece(self, row, col, piece):
        """Drop a piece on the board"""
        self.board[row][col] = piece

    def is_valid_location(self, col):
        """Check if column is valid for dropping piece"""
        return 0 <= col < COLS and self.board[0][col] == 0

    def get_next_open_row(self, col):
        """Get the next available row in a column"""
        for r in range(ROWS-1, -1, -1):
            if self.board[r][col] == 0:
                return r
        return None

    def get_valid_locations(self, board=None):
        """Get all valid columns for dropping pieces"""
        b = board if board is not None else self.board
        return [c for c in range(COLS) if b[0][c] == 0]

    def winning_move(self, piece, board=None):
        """Check if a player has won"""
        b = board if board is not None else self.board
        
        # Horizontal
        for c in range(COLS - 3):
            for r in range(ROWS):
                if all(b[r][c+i] == piece for i in range(4)):
                    return True
        
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(b[r+i][c] == piece for i in range(4)):
                    return True
        
        # Positive Diagonal
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if all(b[r+i][c+i] == piece for i in range(4)):
                    return True
        
        # Negative Diagonal
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if all(b[r-i][c+i] == piece for i in range(4)):
                    return True
        
        return False

    def is_terminal_node(self, board=None):
        """Check if game has ended"""
        b = board if board is not None else self.board
        return (self.winning_move(PLAYER1_PIECE, b) or 
                self.winning_move(PLAYER2_PIECE, b) or 
                len(self.get_valid_locations(b)) == 0)

    @staticmethod
    def get_valid_locations_static(board):
        """Static method to get valid locations"""
        return [c for c in range(COLS) if board[0][c] == 0]

    @staticmethod
    def get_next_open_row_static(board, col):
        """Static method to get next open row"""
        for r in range(ROWS-1, -1, -1):
            if board[r][col] == 0:
                return r
        return None

    @staticmethod
    def drop_piece_static(board, row, col, piece):
        """Static method to drop piece"""
        board[row][col] = piece
        return board
