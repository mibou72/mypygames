import streamlit as st
import pathlib

#function to load css file from css folder
def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")

#load external css file
filepath = pathlib.Path("css/style_main.css")
load_css(filepath)



pg = st.navigation([
        st.Page("welcome_page.py", title="Home"),
        st.Page("hangman.py", title="Hangman"),
        st.Page("rockscissorspaper.py", title="Rock Scissors Paper"),
        st.Page("tictactoe.py", title="Tic Tac Toe"),
        st.Page("minesweeper.py", title="Minesweeper")
])


pg.run()










