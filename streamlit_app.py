import streamlit as st
import random
import time

# 初期化
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# ゲームのタイトル
st.title("釣りゲーム")

# スコア表示
st.write(f"スコア: {st.session_state.score} 点")

# ゲームオーバー時の処理
if st.session_state.game_over:
    st.write("ゲームオーバー！再スタートするにはボタンを押してください")
    if st.button("再スタート"):
        st.session_state.score = 0
        st.session_state.game_over = False
else:
    # 釣りボタン
    if st.button("釣りを開始"):
        with st.spinner("釣ってます..."):
            time.sleep(2)  # 釣りのアクションをシミュレート
            fish_caught = random.choice([True, False])
            
            if fish_caught:
                st.session_state.score += 1
                st.success("おめでとう！魚がかかりました！")
            else:
                st.error("残念！魚がかかりませんでした。")
                st.session_state.game_over = True
