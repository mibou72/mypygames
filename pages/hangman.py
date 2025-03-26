import pathlib
import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components

#function to load css file from css folder
def load_css(filepath):
    with open(filepath) as f:
        css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


#style cells per value
def style_cells(val):
    if val != " ":
        return "background-color: #82FA58; color: black; width: 20px; height: 20px; border_bottom: 1px solid;"
    else:
        return "background-color: #FA5858; color: black; width: 20px; height: 20px; border_bottom: 1px solid;"  # Default style

#print the hangman
def hangman(counter):
    hangman_stages = {
        14: "    |",
        13: "    |\n    |",
        12: "    |\n    |\n    |",
        11: "    |\n    |\n    |\n    |",
        10: "   ___________\n    |\n    |\n    |\n    |",
        9: "    ___________\n    |         |\n    |\n    |\n    |",
        8: "    ___________\n    |         |\n    |\n    |\n    |",
        7: "    ___________\n    |         |\n    |         O\n    |\n    |",
        6: "    ___________\n    |         |\n    |         O\n    |         |\n    |",
        5: "    ___________\n    |         |\n    |         O\n    |        /|\n    |",
        4: "    ___________\n    |         |\n    |         O\n    |        /|\\\n    |",
        3: "    ___________\n    |         |\n    |         O\n    |        /|\\\n    |        / ",
        2: "    ___________\n    |         |\n    |         O\n    |        /|\\\n    |       _/ \\",
        1: "    ___________\n    |         |\n    |         O\n    |        /|\\\n    |       _/ \\",
        0: "    ___________\n    |         |\n    |         O\n    |        /|\\\n    |       _/ \\_",
    }

    # Use st.code to preserve formatting
    if counter in hangman_stages:
        st.code(hangman_stages[counter], language="plaintext")

def create_word():
    if 'randword' not in st.session_state:
        randword = str.upper(random.choice(wordlist))  # Create a random word
        wordaslist = list(randword)  # Convert the word to a list of characters
        searchword = [" "] * len(randword)
        st.session_state['randword'] = randword
        st.session_state['wordaslist'] = wordaslist
        st.session_state['searchword'] = searchword


def sesstate_playground():
    searchword = st.session_state['searchword']  # Always get the latest searchword
    df = pd.DataFrame([searchword])
    df_styled = df.style.applymap(style_cells)
    df_styled = df_styled.set_table_styles([{'selector': 'table', 'props': [('width', '100%')]}])
    df_styled = df_styled.hide(axis="index")
    df_styled = df_styled.hide(axis="columns")
    st.session_state['dfst'] = df_styled  # Always update session state

    # Render the styled DataFrame
    html_code = df_styled.to_html()
    with colplay:
        components.html(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;width: auto; height: auto; overflow: auto; text-align: center;">
                {html_code}
            </div>
            """,
            height=30,
            scrolling=False
        )


#removes the input in the input field, but is not working properly therefore only used in clear button
def reset_player_input():
    st.session_state['player_input'] = ""

# open txt file with words, read into content, split to list and close
filepath = pathlib.Path(__file__).parent.parent / "input_files" / "words.txt"
f = open(filepath, 'r')
content = f.read()
wordlist = content.split('\n')
# print(wordlist)
f.close()

#load external css file
filepath = pathlib.Path(__file__).parent.parent / "css" / "style_hm.css"
load_css(filepath)

if 'counter' not in st.session_state:
    st.session_state['counter'] = 15
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False



#headline and clear button
st.markdown('**** Welcome to play HANGMAN ****')
clear = st.button("clear/new game", on_click=reset_player_input)
create_word()
placeholder = " "
counter = 0



with st.form('form_ttt'):
    (colplay, colb) = st.columns([1, 1])

    # Greetings and input field
    with colb:
        st.write(f"Welcome You. You wanna play?")
    with colb:
        playerinput = st.text_input(
            label="Guess the word:",
            placeholder="write letter here",
            max_chars=1,
            disabled=False,
            label_visibility="visible",
            key="player_input"
        )

    playerinput = str.upper(playerinput)

    if st.session_state['counter'] == 0:
        st.session_state['game_over'] = True
    # If equal or won disable the submit button
    with colb:
        submit_input = st.form_submit_button(
            "confirm your input",
            disabled=st.session_state['game_over'] or st.session_state['counter'] <= 1,
        )

if submit_input:

    # Get the current state
    randword = st.session_state['randword']
    wordaslist = st.session_state['wordaslist']
    searchword = st.session_state['searchword']

    # Check if the letter is in the word
    indexlist = [idx for idx, s in enumerate(wordaslist) if playerinput == s]

    if len(indexlist) == 0:  # Letter not in the word
        st.session_state['counter'] -= 1
        with colb:
            st.write(f"Dieser Buchstabe ist nicht vorhanden. Du hast noch {st.session_state['counter']} Versuche.")
        if st.session_state['counter'] == 0:
            st.session_state['game_over'] = True
    else:  # Letter is in the word
        for i in indexlist:
            searchword[i] = playerinput
            st.session_state['searchword'] = searchword  # Update session state
        if " " not in searchword:  # Check if the word is fully guessed
            st.session_state['game_over'] = True
            with colb:
                st.write("Glückwunsch, du hast das Wort erraten!")
            if st.session_state['counter'] == 0:
                st.session_state['game_over'] = True
        else:
            with colb:
                st.write("Weiter so!")



    # Update the hangman print
    with colplay:
        hangman(st.session_state['counter'])



sesstate_playground()


# Reset the input_key when clearing the game
if clear:
    st.session_state.clear()
    create_word()
    st.session_state['input_key'] = 0  # Reset the key
    st.rerun()
