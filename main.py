import streamlit as st
import pathlib

#function to load css file from css folder
def load_css(filepath):
    with open(filepath) as f:
        st.html(f"<style>{f.read()}</style>")

#load external css file
filepath = pathlib.Path("css/style_main.css")
load_css(filepath)



pages = {
    "": [
        st.Page("welcome_page.py", title="Home"),
        st.Page("pages\\hangman.py", title="Hangman"),
        st.Page("pages\\rock_scissors_paper_against_computer.py", title="Rock Scissors Paper"),
        st.Page("pages\\tictactoe_against_computer.py", title="Tic Tac Toe"),
        st.Page("pages\\minesweaper.py", title="Minesweaper"),
    ],

}

pg = st.navigation(pages)
pg.run()










