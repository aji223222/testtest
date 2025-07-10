import streamlit as st
import random
from collections import Counter

# カードの定義
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# カードのデッキを作成
def create_deck():
    return [f'{rank}{suit}' for rank in ranks for suit in suits]

# カードをシャッフルして引く
def shuffle_and_deal(deck):
    random.shuffle(deck)
    return deck[:5], deck[5:10]  # プレイヤーとコンピュータの手札を5枚ずつ配る

# 手札を評価する関数
def evaluate_hand(hand):
    # ランクとスートを分ける
    ranks_in_hand = [card[:-1] for card in hand]
    suits_in_hand = [card[-1] for card in hand]

    rank_counts = Counter(ranks_in_hand)
    is_flush = len(set(suits_in_hand)) == 1
    is_straight = len(rank_counts) == 5 and (ranks_in_hand.index(max(ranks_in_hand, key=lambda x: ranks.index(x))) - ranks_in_hand.index(min(ranks_in_hand, key=lambda x: ranks.index(x))) == 4)
    
    return {
        'ranks_in_hand': ranks_in_hand,
        'is_flush': is_flush,
        'is_straight': is_straight
    }

# ゲームの状態をリセットするための関数
def reset_game():
    deck = create_deck()
    player_hand, computer_hand = shuffle_and_deal(deck)
    return player_hand, computer_hand

# ポーカーハンドを評価して勝者を決定
def determine_winner(player_hand, computer_hand):
    player_score = evaluate_hand(player_hand)
    computer_score = evaluate_hand(computer_hand)
    
    # フラッシュとストレートを判定
    player_strength = (player_score['is_flush'], player_score['is_straight'])
    computer_strength = (computer_score['is_flush'], computer_score['is_straight'])
    
    if player_strength > computer_strength:
        return 'プレイヤーの勝ち！'
    elif player_strength < computer_strength:
        return 'コンピュータの勝ち！'
    else:
        return '引き分け！'

# メインUIの作成
def poker_game():
    st.title("ポーカーゲーム")

    if 'player_hand' not in st.session_state:
        st.session_state.player_hand, st.session_state.computer_hand = reset_game()

    st.write("プレイヤーの手札: ", ', '.join(st.session_state.player_hand))
    st.write("コンピュータの手札: ", ', '.join(st.session_state.computer_hand))

    if st.button("ゲーム開始！"):
        winner = determine_winner(st.session_state.player_hand, st.session_state.computer_hand)
        st.write(winner)
        st.session_state.player_hand, st.session_state.computer_hand = reset_game()

# ゲームの起動
if __name__ == "__main__":
    poker_game()
