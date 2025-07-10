import streamlit as st
import numpy as np
import random

BOARD_SIZE = 8
EMPTY = 0
BLACK = 1
WHITE = 2

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]


def init_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board


def is_on_board(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def valid_moves(board, player):
    moves = []
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == EMPTY and is_valid_move(board, player, x, y):
                moves.append((x, y))
    return moves


def is_valid_move(board, player, x_start, y_start):
    if board[x_start][y_start] != EMPTY or not is_on_board(x_start, y_start):
        return False

    other = BLACK if player == WHITE else WHITE
    for dx, dy in DIRECTIONS:
        x, y = x_start + dx, y_start + dy
        if is_on_board(x, y) and board[x][y] == other:
            x += dx
            y += dy
            while is_on_board(x, y):
                if board[x][y] == EMPTY:
                    break
                if board[x][y] == player:
                    return True
                x += dx
                y += dy
    return False


def make_move(board, player, x_start, y_start):
    board[x_start][y_start] = player
    other = BLACK if player == WHITE else WHITE
    flipped = []

    for dx, dy in DIRECTIONS:
        x, y = x_start + dx, y_start + dy
        flip_candidates = []
        while is_on_board(x, y) and board[x][y] == other:
            flip_candidates.append((x, y))
            x += dx
            y += dy
        if is_on_board(x, y) and board[x][y] == player:
            for fx, fy in flip_candidates:
                board[fx][fy] = player
                flipped.append((fx, fy))
    return board, flipped


def count_pieces(board):
    blacks = np.sum(board == BLACK)
    whites = np.sum(board == WHITE)
    return blacks, whites


def board_to_str(board):
    symbols = {EMPTY: '・', BLACK: '●', WHITE: '○'}
    rows = []
    for row in board:
        rows.append(" ".join(symbols[cell] for cell in row))
    return "\n".join(rows)


def main():
    st.title("オセロ（リバーシ）ゲーム")

    if "board" not in st.session_state:
        st.session_state.board = init_board()
        st.session_state.turn = BLACK  # 黒の先攻
        st.session_state.game_over = False
        st.session_state.message = "黒（●）の番です"

    board = st.session_state.board
    turn = st.session_state.turn
    game_over = st.session_state.game_over

    blacks, whites = count_pieces(board)
    st.write(f"● 黒: {blacks}  ○ 白: {whites}")

    def draw_board():
        for x in range(BOARD_SIZE):
            cols = st.columns(BOARD_SIZE)
            for y in range(BOARD_SIZE):
                cell = board[x][y]
                symbol = "・"
                if cell == BLACK:
                    symbol = "●"
                elif cell == WHITE:
