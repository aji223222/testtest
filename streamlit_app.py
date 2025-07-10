import streamlit as st
import numpy as np

# ゲームボードの初期化
def initialize_board():
    return np.full((3, 3), "", dtype=str)

# 勝者判定
def check_winner(board):
    # 行、列、斜めでの勝者判定
    for i in range(3):
        # 行のチェック
        if board[i, 0] == board[i, 1] == board[i, 2] and board[i, 0] != "":
            return board[i, 0]
        # 列のチェック
        if board[0, i] == board[1, i] == board[2, i] and board[0, i] != "":
            return board[0, i]

    # 斜めのチェック
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != "":
        return board[0, 0]
    if board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != "":
        return board[0, 2]

    return None

# ゲームボードの描画
def draw_board(board):
    for i in range(3):
        for j in range(3):
            cell = board[i, j]
            st.button(cell if cell else "", key=f"{i}_{j}", on_click=make_move, args=(i, j))

# プレイヤーのターン
def make_move(i, j):
    if board[i, j] == "" and not winner:
        board[i, j] = current_player[0]
        check_game_status()

# ゲームの状態確認
def check_game_status():
    global current_player, winner, game_over
    winner = check_winner(board)
    
    if winner:
        game_over = True
        st.write(f"プレイヤー {winner} の勝利!")
    elif np.all(board != ""):  # ボードが満杯で勝者なし
        game_over = True
        st.write("引き分けです!")
    else:
        current_player = "X" if current_player == "O" else "O"

# 初期化
if 'board' not in st.session_state:
    st.session_state.board = initialize_board()
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False

board = st.session_state.board
current_player = st.session_state.current_player
winner = st.session_state.winner
game_over = st.session_state.game_over

# タイトル
st.title("〇×ゲーム")

# ゲームの状態を表示
if game_over:
    st.write("ゲームが終了しました！")
    if winner:
        st.write(f"勝者: プレイヤー {winner}")
    else:
        st.write("引き分けです！")
    if st.button("新しいゲーム"):
        st.session_state.board = initialize_board()
        st.session_state.current_player = "X"
        st.session_state.winner = None
        st.session_state.game_over = False
else:
    st.write(f"現在のプレイヤー: {current_player}")

# ゲームボードの描画
draw_board(board)
