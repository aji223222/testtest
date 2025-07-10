import streamlit as st
import random

# じゃんけんの手を定義
choices = ['グー', 'チョキ', 'パー']

# じゃんけんの結果を判定する関数
def judge(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "引き分け"
    elif (player_choice == 'グー' and computer_choice == 'チョキ') or \
         (player_choice == 'チョキ' and computer_choice == 'パー') or \
         (player_choice == 'パー' and computer_choice == 'グー'):
        return "あなたの勝ち"
    else:
        return "コンピューターの勝ち"

# StreamlitアプリのUI
st.title('じゃんけんゲーム')

# ユーザーに手を選ばせる
player_choice = st.selectbox('じゃんけんの手を選んでください:', choices)

# コンピューターが手を選ぶ
computer_choice = random.choice(choices)

# ボタンを押したときに結果を表示
if st.button('じゃんけん！'):
    result = judge(player_choice, computer_choice)
    st.write(f'あなたの手: {player_choice}')
    st.write(f'コンピューターの手: {computer_choice}')
    st.write(f'結果: {result}')
