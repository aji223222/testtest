import streamlit as st
import pygame
import random

# ゲーム設定
WIDTH, HEIGHT = 600, 400
FPS = 60

# 初期化
pygame.init()

# ゲーム画面
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('テニスゲーム')

# 色設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# パドル設定
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 60
PADDLE_SPEED = 10

# ボール設定
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# プレイヤーとコンピュータ
player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
computer_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

# スコア
player_score = 0
computer_score = 0

# フォント設定
font = pygame.font.SysFont("Arial", 30)

# ゲームのリセット
def reset_game():
    global ball_x, ball_y, ball_dx, ball_dy, player_y, computer_y
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    ball_dx = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_dy = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])
    player_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    computer_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# スコア表示
def draw_score():
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    computer_text = font.render(f"Computer: {computer_score}", True, WHITE)
    screen.blit(player_text, (50, 20))
    screen.blit(computer_text, (WIDTH - 250, 20))

# パドル描画
def draw_paddles():
    pygame.draw.rect(screen, WHITE, (10, player_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 30, computer_y, PADDLE_WIDTH, PADDLE_HEIGHT))

# ボール描画
def draw_ball():
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

# ボールの動き
def move_ball():
    global ball_x, ball_y, ball_dx, ball_dy, player_score, computer_score

    ball_x += ball_dx
    ball_y += ball_dy

    # 上下の壁で跳ね返り
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_dy = -ball_dy

    # プレイヤーとコンピュータのパドルとの衝突
    if ball_x - BALL_RADIUS <= 30 and player_y <= ball_y <= player_y + PADDLE_HEIGHT:
        ball_dx = -ball_dx
    if ball_x + BALL_RADIUS >= WIDTH - 30 and computer_y <= ball_y <= computer_y + PADDLE_HEIGHT:
        ball_dx = -ball_dx

    # 左側または右側の壁を越えた場合
    if ball_x - BALL_RADIUS <= 0:
        computer_score += 1
        reset_game()
    if ball_x + BALL_RADIUS >= WIDTH:
        player_score += 1
        reset_game()

# コンピュータのAI
def move_computer():
    global computer_y

    if computer_y + PADDLE_HEIGHT // 2 < ball_y:
        computer_y += PADDLE_SPEED
    elif computer_y + PADDLE_HEIGHT // 2 > ball_y:
        computer_y -= PADDLE_SPEED

    # パドルが画面外に行かないように制限
    if computer_y < 0:
        computer_y = 0
    if computer_y + PADDLE_HEIGHT > HEIGHT:
        computer_y = HEIGHT - PADDLE_HEIGHT

# プレイヤーの操作
def move_player():
    global player_y

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and player_y + PADDLE_HEIGHT < HEIGHT:
        player_y += PADDLE_SPEED

# ゲームのメインループ
def game_loop():
    global player_score, computer_score, ball_dx, ball_dy

    running = True
    while running:
        screen.fill(GREEN)
        draw_score()
        draw_paddles()
        draw_ball()
        move_ball()
        move_computer()
        move_player()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

# Streamlitのインターフェース
def tennis_game():
    st.title("テニスゲーム")

    if st.button("ゲームスタート"):
        game_loop()

    st.write("コントロール: ↑ 下矢印キーでパドルを動かします。")

if __name__ == "__main__":
    tennis_game()
