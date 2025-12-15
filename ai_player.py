import math
from connect4_game import Connect4Game
from constants import PLAYER1_PIECE, PLAYER2_PIECE, ROWS, COLS


class AIPlayer:
    def __init__(self, piece=PLAYER2_PIECE):
        self.piece = piece
        self.opp_piece = PLAYER1_PIECE if piece == PLAYER2_PIECE else PLAYER2_PIECE
        self.cache = {}  # 🧠 Transposition Table

    def board_key(self, board):
        return tuple(tuple(row) for row in board)

    def score_window(self, window):
        score = 0
        if window.count(self.piece) == 4:
            score += 100000
        elif window.count(self.piece) == 3 and window.count(0) == 1:
            score += 100
        elif window.count(self.piece) == 2 and window.count(0) == 2:
            score += 10

        if window.count(self.opp_piece) == 3 and window.count(0) == 1:
            score -= 120

        return score

    def evaluate_board(self, board):
        score = 0

        center = COLS // 2
        score += [board[r][center] for r in range(ROWS)].count(self.piece) * 6

        for r in range(ROWS):
            for c in range(COLS - 3):
                score += self.score_window([board[r][c + i] for i in range(4)])

        for c in range(COLS):
            for r in range(ROWS - 3):
                score += self.score_window([board[r + i][c] for i in range(4)])

        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                score += self.score_window([board[r + i][c + i] for i in range(4)])

        for r in range(3, ROWS):
            for c in range(COLS - 3):
                score += self.score_window([board[r - i][c + i] for i in range(4)])

        return score

    def order_moves(self, moves):
        center = COLS // 2
        return sorted(moves, key=lambda c: abs(center - c))

    def minimax(self, game, depth, alpha, beta, maximizing):
        board = game.copy_board()
        key = (self.board_key(board), depth, maximizing)

        if key in self.cache:
            return self.cache[key]

        valid_moves = self.order_moves(game.get_valid_locations(board))

        # 🔴 كسب أو خسارة فورية
        for col in valid_moves:
            row = game.get_next_open_row_static(board, col)
            temp = [r[:] for r in board]
            game.drop_piece_static(temp, row, col,
                                   self.piece if maximizing else self.opp_piece)
            if game.winning_move(self.piece if maximizing else self.opp_piece, temp):
                result = (col, 100000 if maximizing else -100000)
                self.cache[key] = result
                return result

        if depth == 0 or len(valid_moves) == 0:
            result = (None, self.evaluate_board(board))
            self.cache[key] = result
            return result

        if maximizing:
            best = (-1, -math.inf)
            for col in valid_moves:
                row = game.get_next_open_row_static(board, col)
                temp = [r[:] for r in board]
                game.drop_piece_static(temp, row, col, self.piece)

                g = Connect4Game()
                g.board = temp
                score = self.minimax(g, depth - 1, alpha, beta, False)[1]

                if score > best[1]:
                    best = (col, score)

                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        else:
            best = (-1, math.inf)
            for col in valid_moves:
                row = game.get_next_open_row_static(board, col)
                temp = [r[:] for r in board]
                game.drop_piece_static(temp, row, col, self.opp_piece)

                g = Connect4Game()
                g.board = temp
                score = self.minimax(g, depth - 1, alpha, beta, True)[1]

                if score < best[1]:
                    best = (col, score)

                beta = min(beta, score)
                if alpha >= beta:
                    break

        self.cache[key] = best
        return best
