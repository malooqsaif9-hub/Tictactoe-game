import streamlit as st
import numpy as np
import random
import time

st.set_page_config(page_title="Tic Tac Toe 🔥", page_icon="🎮", layout="centered")

# ---------- Game state ----------
if "board" not in st.session_state:
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.winner = None
    st.session_state.score = {"X": 0, "O": 0, "DRAW": 0}
    st.session_state.move_count = 0

WIN_TAUNTS = [
    "Absolutely demolished. 💀",
    "GG, better luck next time!",
    "That was almost too easy 😎",
    "Someone call an ambulance... for the other player.",
    "Legendary play detected. 🏆",
]
DRAW_TAUNTS = [
    "A battle of equals. 🤝",
    "Nobody wins, everybody cries.",
    "Stalemate! Even the board is bored.",
]
MOVE_TAUNTS = [
    "Ooh, spicy move 🌶️",
    "Interesting strategy...",
    "Playing 4D chess I see.",
    "Bold choice, captain.",
    "The suspense is real 😬",
]

def check_winner(b):
    if 3 in np.sum(b, axis=1) or 3 in np.sum(b, axis=0):
        return "X"
    if -3 in np.sum(b, axis=1) or -3 in np.sum(b, axis=0):
        return "O"
    if np.trace(b) == 3 or np.trace(np.fliplr(b)) == 3:
        return "X"
    if np.trace(b) == -3 or np.trace(np.fliplr(b)) == -3:
        return "O"
    if 0 not in b:
        return "DRAW"
    return None

def make_move(r, c):
    if st.session_state.winner is not None:
        return
    if st.session_state.board[r, c] != 0:
        return
    st.session_state.board[r, c] = st.session_state.current
    st.session_state.move_count += 1
    result = check_winner(st.session_state.board)
    if result is not None:
        st.session_state.winner = result
        st.session_state.score[result] += 1
    else:
        st.session_state.current *= -1

def reset_game():
    st.session_state.board = np.zeros((3, 3), dtype=int)
    st.session_state.current = 1
    st.session_state.winner = None
    st.session_state.move_count = 0

def reset_all():
    reset_game()
    st.session_state.score = {"X": 0, "O": 0, "DRAW": 0}

# ---------- Styling ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e1e2f 0%, #2d1b4e 50%, #0f3460 100%);
}
h1, h2, h3, p, span, div, label {
    color: #f5f5f5 !important;
}
div.stButton > button {
    height: 100px;
    width: 100%;
    font-size: 42px;
    font-weight: 900;
    border-radius: 16px;
    border: 2px solid rgba(255,255,255,0.15);
    background: rgba(255,255,255,0.06);
    color: white;
    transition: all 0.15s ease-in-out;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}
div.stButton > button:hover {
    transform: translateY(-4px) scale(1.04);
    border: 2px solid #ff5f6d;
    background: rgba(255,255,255,0.14);
    box-shadow: 0 8px 20px rgba(255,95,109,0.35);
}
div.stButton > button:active {
    transform: scale(0.96);
}
.score-card {
    background: rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 14px 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.12);
}
.taunt {
    text-align:center;
    font-size: 18px;
    font-style: italic;
    opacity: 0.85;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1 style='text-align:center;'>🎮 Tic Tac Toe, But Make It Fancy</h1>", unsafe_allow_html=True)

# Scoreboard
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='score-card'><h3>❌ X</h3><h2>{st.session_state.score['X']}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='score-card'><h3>🤝 Draws</h3><h2>{st.session_state.score['DRAW']}</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='score-card'><h3>⭕ O</h3><h2>{st.session_state.score['O']}</h2></div>", unsafe_allow_html=True)

st.write("")

# Turn / result banner
symbols = {0: "", 1: "❌", -1: "⭕"}

if st.session_state.winner is None:
    turn_symbol = "❌" if st.session_state.current == 1 else "⭕"
    st.markdown(f"<h3 style='text-align:center;'>Turn: {turn_symbol}</h3>", unsafe_allow_html=True)
    if st.session_state.move_count > 0:
        random.seed(st.session_state.move_count)
        st.markdown(f"<p class='taunt'>{random.choice(MOVE_TAUNTS)}</p>", unsafe_allow_html=True)
else:
    if st.session_state.winner == "DRAW":
        st.markdown("<h2 style='text-align:center;'>🤝 It's a Draw!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='taunt'>{random.choice(DRAW_TAUNTS)}</p>", unsafe_allow_html=True)
    else:
        emoji = "❌" if st.session_state.winner == "X" else "⭕"
        st.markdown(f"<h2 style='text-align:center;'>🎉 {emoji} Wins! 🎉</h2>", unsafe_allow_html=True)
        st.markdown(f"<p class='taunt'>{random.choice(WIN_TAUNTS)}</p>", unsafe_allow_html=True)
        st.balloons()

st.write("")

# ---------- Board ----------
for r in range(3):
    cols = st.columns(3, gap="small")
    for c in range(3):
        label = symbols[st.session_state.board[r, c]]
        with cols[c]:
            if st.button(label if label else "·", key=f"cell_{r}_{c}"):
                make_move(r, c)
                st.rerun()

st.write("")
b1, b2 = st.columns(2)
with b1:
    if st.button("🔄 New Round", use_container_width=True):
        reset_game()
        st.rerun()
with b2:
    if st.button("🗑️ Reset Scoreboard", use_container_width=True):
        reset_all()
        st.rerun()