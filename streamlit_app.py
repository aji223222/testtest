import streamlit as st
import numpy as np
import time
from PIL import Image, ImageDraw
import random

# ゲームの設定
CAR_WIDTH = 20  # 車の幅
CAR_HEIGHT = 40  # 車の高さ
TRACK_WIDTH = 200  # トラックの幅
TRACK_HEIGHT = 600  # トラックの高さ
OBSTACLE_WIDTH = 30  # 障害物の幅
OBSTACLE_HEIGHT = 30  # 障害物の高さ

# 初期化
if 'car_pos' not in st.session_state:
    st.session_state.car_pos = [TRACK_WIDTH // 2 - CAR_WIDTH // 2, TRACK_HEIGHT - CAR_HEIGHT - 10]  # 車の初期位置
if 'score' not in st.session_state:
    st.session_state.score = 0  # スコア
if 'obstacles' not in st.session_state:
    st.session_state.obstacles = []  # 障害物のリスト
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# 車の描画
def draw_car(draw, car_pos):
    draw.rectangle([car_pos[0], car_pos[1], car_pos[0] + CAR_WIDTH, car_pos[1] + CAR_HEIGHT], fill="blue")

# 障害物の描画
def draw_obstacles(draw, obstacles):
    for obs in obstacles:
        draw.rectangle([obs[0], obs[1], obs[0] + OBSTACLE_WIDTH, obs[1] + OBSTACLE_HEIGHT], fill="red")

# 障害物の移動
def move_obstacles():
    # 障害物を移動させる
    new_obstacles = []
    for obs in st.session_state.obstacles:
        if obs[1] < TRACK_HEIGHT:
            new_obstacles.append([obs[0], obs[1] + 5])
    
    # 新しい障害物を追加
    if random.random() < 0.05:
        new_x = random.randint(0, TRACK_WIDTH - OBSTACLE_WIDTH)
        new_obstacles.append([new_x, 0])
    
    st.session_state.obstacles = new_obstacles

# 衝突判定
def check_collision():
    car_pos = st.session_state.car_pos
    for obs in st.session_state.obstacles:
        if (car_pos[0] < obs[0] + OBSTACLE_WIDTH and
            car_pos[0] + CAR_WIDTH > obs[0] and
            car_pos[1] < obs[1] + OBSTACLE_HEIGHT and
            car_pos[1] + CAR_HEIGHT > obs[1]):
            return True
    return False

# 車の移動
def move_car(direction):
    if direction == 'left':
        st.session_state.car_pos[0] = max(0, st.session_state.car_pos[0] - 10)
    elif direction == 'right':
        st.session_state.car_pos[0] = min(TRACK_WIDTH - CAR_WIDTH, st.session_state.car_pos[0] + 10)

# ゲーム画面の描画
def draw_game():
    # 画面の作成
    image = Image.new('RGB', (TRACK_WIDTH, TRACK_HEIGHT), (0, 0, 0))  # 黒い背景
    draw = ImageDraw.Draw(image)
    
    # トラックの中央線
    draw.line([TRACK_WIDTH // 2, 0, TRACK_WIDTH // 2, TRACK_HEIGHT], fill="white", width=2)
    
    # 車を描画
    draw_car(draw, st.session_state.car_pos)
    
    # 障害物を描画
    draw_obstacles(draw, st.session_state.obstacles)
    
    return image

# ゲームの進行
def game_loop():
    if st.session_state.game_over:
        st.write("ゲームオーバー！")
        st.write(f"スコア: {st.session_state.score}")
        if st.button("再スタート"):
            st.session_state.car_pos = [TRACK_WIDTH // 2 - CAR_WIDTH // 2, TRACK_HEIGHT - CAR_HEIGHT - 10]
            st.session_state.score = 0
            st.session_state.obstacles = []
            st.session_state.game_over = False
        return
    
    # ゲームの描画
    image = draw_game()
    st.image(image, caption="レースゲーム", use_column_width=True)
    
    # 車の移動処理
    direction = None
    if st.button("左"):
        direction = 'left'
    elif st.button("右"):
        direction = 'right'
    
    if direction:
        move_car(direction)
    
    # 障害物の移動
    move_obstacles()
    
    # 衝突チェック
    if check_collision():
        st.session_state.game_over = True
        return
    
    # スコア更新
    st.session_state.score += 1
    st.write(f"スコア: {st.session_state.score}")
    
    # ゲームの進行
    time.sleep(0.1)

# ゲームの開始
def start_game():
    st.title("レースゲーム")
    game_loop()

# 実行
if __name__ == "__main__":
    start_game()
