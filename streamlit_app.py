import streamlit as st
import random

# 花の選択肢と占い結果
flowers = {
    "バラ": {
        "image": "assets/flower1.jpg",
        "fortune": [
            "あなたの恋愛運は絶好調！素敵な出会いが待っています。",
            "心を開いて新しいことに挑戦してみましょう。",
            "今は少し休息が必要な時。自分を大切にして。",
        ]
    },
    "チューリップ": {
        "image": "assets/flower2.jpg",
        "fortune": [
            "友達との関係が深まる時期です。素敵な友情を築いて。",
            "これから新しい挑戦が待っています。自信を持って進んで。",
            "少し落ち着いて、自分のペースで物事を進めると良いでしょう。",
        ]
    },
    "ひまわり": {
        "image": "assets/flower3.jpg",
        "fortune": [
            "あなたの努力が報われる時です。自信を持って前に進んで。",
            "心の中で迷っていることがあるなら、今がその答えを見つける時。",
            "楽しむことを大切に。リラックスして日々を楽しんで。",
        ]
    }
}

# タイトルとインストラクション
st.title("花占いゲーム")
st.write("下記の花の中から1つ選んで、占いの結果を見てみましょう！")

# 花を選択する
flower_choice = st.selectbox("花を選んでください:", list(flowers.keys()))

# 選んだ花に基づいて占い結果を表示
if flower_choice:
    st.image(flowers[flower_choice]["image"], width=300)
    st.write(f"あなたが選んだ花は「{flower_choice}」です。")
    
    # ランダムな占い結果を表示
    fortune = random.choice(flowers[flower_choice]["fortune"])
    st.write(f"占いの結果: {fortune}")

