import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw

# ゲームの設定
GRID_SIZE = 10  # グリッドのサイズ（10x10）
PACMAN_COLOR = (255, 255, 0)  # パックマンの色（黄色）
GHOST_COLOR = (255, 0, 0)    # ゴーストの色（赤）

# 初期化
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'pacman_pos' not in st.session_state:
    st.session_state.pacman_pos = [5, 5]  # パックマンの初期位置
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# ゲームフィールドの描画
def draw_game():
    # ゲームボードのサイズ
    width, height = 400, 400
    grid = Image.new('RGB', (width, height), (0, 0, 0))  # 黒い背景
    draw = ImageDraw.Draw(grid)
    
    # グリッド線の描画
    for i in range(0, width, width // GRID_SIZE):
        draw.line([(i, 0), (i, height)], fill=(255, 255, 255))
    for i in range(0, height, height // GRID_SIZE):
        draw.line([(0, i), (width, i)], fill=(255, 255, 255))
    
    # パックマンの描画
    pacman_x = st.session_state.pacman_pos[0] * (width // GRID_SIZE) + (width // GRID_SIZE) // 2
    pacman_y = st.session_state.pacman_pos[1] * (height // GRID_SIZE) + (height // GRID_SIZE) // 2
    draw.ellipse(
        [(pacman_x - 10, pacman_y - 10), (pacman_x + 10, pacman_y + 10)],
        fill=PACMAN_COLOR
    )

    # ゴースト（簡易的に1体）の描画
    ghost_x = 3 * (width // GRID_SIZE) + (width // GRID_SIZE) // 2
    ghost_y = 3 * (height // GRID_SIZE) + (height // GRID_SIZE) // 2
    draw.ellipse(
        [(ghost_x - 10, ghost_y - 10), (ghost_x + 10, ghost_y + 10)],
        fill=GHOST_COLOR
    )
    
    return grid

# ゲームオーバー処理
def check_collision():
    pacman_pos = st.session_state.pacman_pos
    ghost_pos = [3, 3]  # ゴーストの固定位置
    if pacman_pos == ghost_pos:
        st.session_state.game_over = True
        return True
    return False

# ユーザー入力（パックマンの移動）
def move_pacman(direction):
    if st.session_state.game_over:
        return

    if direction == 'up':
        st.session_state.pacman_pos[1] = max(0, st.session_state.pacman_pos[1] - 1)
    elif direction == 'down':
        st.session_state.pacman_pos[1] = min(GRID_SIZE - 1, st.session_state.pacman_pos[1] + 1)
    elif direction == 'left':
        st.session_state.pacman_pos[0] = max(0, st.session_state.pacman_pos[0] - 1)
    elif direction == 'right':
        st.session_state.pacman_pos[0] = min(GRID_SIZE - 1, st.session_state.pacman_pos[0] + 1)

# ゲームの描画と進行
def game_loop():
    if st.session_state.game_over:
        st.write("ゲームオーバー！")
        st.write(f"スコア: {st.session_state.score}")
        if st.button("再スタート"):
            st.session_state.score = 0
            st.session_state.pacman_pos = [5, 5]
            st.session_state.game_over = False
        return

    # ゲーム画面の描画
    grid_image = draw_game()
    st.image(grid_image, caption="パックマン", use_column_width=True)
    
    # ユーザー入力を処理
    direction = None
    if st.button("上"):
        direction = 'up'
    elif st.button("下"):
        direction = 'down'
    elif st.button("左"):
        direction = 'left'
    elif st.button("右"):
        direction = 'right'
    
    if direction:
        move_pacman(direction)
    
    # 衝突チェック
    if check_collision():
        return

    # スコア表示
    st.session_state.score += 1
    st.write(f"スコア: {st.session_state.score}")
    
    # 少し待機してゲームの動きに遅延をつける
    time.sleep(0.5)

# ゲーム開始
def start_game():
    st.title("パックマン")
    game_loop()

# アプリの実行
if __name__ == "__main__":
    start_game()
