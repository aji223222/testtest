import streamlit as st
import numpy as np
import random

# ゲームの設定
GRID_SIZE = 10  # グリッドのサイズ（10x10）
NUM_MINES = 15  # 爆弾の数

# 初期化
if 'game_board' not in st.session_state:
    st.session_state.game_board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # ボードの初期化（0: 非爆弾、1: 爆弾）
    st.session_state.revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)  # セルの開かれている状態
    st.session_state.mines = set()  # 爆弾の位置
    st.session_state.game_over = False  # ゲームオーバー状態
    st.session_state.win = False  # 勝利状態
    st.session_state.flags = set()  # フラグを立てた位置

# 爆弾をランダムに配置する関数
def place_mines():
    while len(st.session_state.mines) < NUM_MINES:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        st.session_state.mines.add((x, y))
        st.session_state.game_board[x, y] = -1  # -1を爆弾の位置に設定
    
    # 各セルに隣接する爆弾の数をカウントする
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if st.session_state.game_board[x, y] == -1:
                continue  # 爆弾があるセルはスキップ
            # 8方向をチェック
            mine_count = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    nx, ny = x + i, y + j
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if st.session_state.game_board[nx, ny] == -1:
                            mine_count += 1
            st.session_state.game_board[x, y] = mine_count

# セルを開ける関数
def reveal_cell(x, y):
    if (x, y) in st.session_state.flags:
        return  # フラグが立てられている場合は何もしない
    if st.session_state.game_board[x, y] == -1:  # 爆弾を踏んだ
        st.session_state.game_over = True
        return
    st.session_state.revealed[x, y] = True
    # 0のセルの場合、周囲のセルを再帰的に開ける
    if st.session_state.game_board[x, y] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                nx, ny = x + i, y + j
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and not st.session_state.revealed[nx, ny]:
                    reveal_cell(nx, ny)

# フラグを置く
def toggle_flag(x, y):
    if st.session_state.revealed[x, y]:  # 既に開かれているセルにはフラグを立てられない
        return
    if (x, y) in st.session_state.flags:
        st.session_state.flags.remove((x, y))
    else:
        st.session_state.flags.add((x, y))

# 勝利判定
def check_win():
    # 開かれたセルが非爆弾セルのみの場合、勝利
    unrevealed_non_mine = 0
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if not st.session_state.revealed[x, y] and (x, y) not in st.session_state.mines:
                unrevealed_non_mine += 1
    if unrevealed_non_mine == 0:
        st.session_state.win = True
        st.session_state.game_over = True

# ゲームの描画
def draw_game():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if st.session_state.revealed[x, y]:
                if st.session_state.game_board[x, y] == -1:
                    st.write(f"💣", end=" ")
                else:
                    st.write(f"{st.session_state.game_board[x, y]}", end=" ")
            else:
                if (x, y) in st.session_state.flags:
                    st.write(f"🚩", end=" ")  # フラグを立てた場所
                else:
                    st.write(f"■", end=" ")  # 隠されたセル
        st.write()

# ゲームの進行
def play_game():
    st.title("マインスイーパ")

    if not st.session_state.mines:
        place_mines()

    if st.session_state.game_over:
        if st.session_state.win:
            st.write("おめでとうございます！あなたの勝ちです！")
        else:
            st.write("ゲームオーバー！爆弾を踏みました。")
        return

    # ゲームボードの表示
    draw_game()

    # ユーザーの操作
    action = st.radio("アクションを選択", ["セルを開く", "フラグを置く"])
    x = st.number_input("x座標（0〜9）", min_value=0, max_value=GRID_SIZE-1)
    y = st.number_input("y座標（0〜9）", min_value=0, max_value=GRID_SIZE-1)
あimport streamlit as st
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
あ
    if action == "セルを開く":
        reveal_cell(x, y)
    elif action == "フラグを置く":
        toggle_flag(x, y)

    check_win()

# ゲーム開始
if __name__ == "__main__":
    play_game()
