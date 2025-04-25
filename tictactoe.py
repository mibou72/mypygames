"""
Tick Tack Toe Spiel
- Spielfeld erstellen
- Spielbrett ausgeben
- Zeile auswählen
- Spalte auswählen
- Marker setzten
  - check: Feld leer?
- Sieg? Unentschieden?
- Spielbrett nochmals anzeigen
"""
import random
import pathlib
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


#function to load css file from css folder
def load_css(filepath):
    with open(filepath) as f:
        css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

#style cells based on value
def style_cells(val):
    if val == st.session_state['human_player']:
        return "background-color: #FFFF00; color: black; width: 90px; height: 90px; border: 1px solid;"
    elif val == "Computer":
        return "background-color: #00BFFF; color: black; width: 90px; height: 90px; border: 1px solid;"
    else:
        return "background-color: #FFFFFF; color: black; width: 90px; height: 90px; border: 1px solid;" # Default style


# 1. Spielbrett erstellen
def erstelle_brett():
    brett = []
    for i in range(3):
        zeile = [" ", " ", " "]
        brett.append(zeile)
    return brett


# 2.Spielbrett ausgeben
def drucke_brett(brett):
    for zeile in brett:
        print("|".join(zeile))
        print("-", "-", "-")


# zug machen computer
def zug_computer(brett):
    while True:
        compzeile = random.randint(0, 2)
        compspalte = random.randint(0, 2)
        if brett[compzeile][compspalte] == " ":
            brett[compzeile][compspalte] = "Computer"
            break


# 3.Zug machen
def mache_zug(brett, aktueller_spieler, zeile, spalte):
    if brett[zeile][spalte] == " ":
        brett[zeile][spalte] = aktueller_spieler
        return True
    else:
        with colc:
            st.write("you had already this cell.")
            return False


# 4.Gewinn überprüfen
def pruefe_gewonnen(brett, test, computer_player="Computer"):
    # Check rows
    for zeile in range(3):
        if brett[zeile][0] == brett[zeile][1] == brett[zeile][2] and brett[zeile][0] != " ":
            return brett[zeile][0]  # Return the winner (either test or computer_player)

    # Check columns
    for spalte in range(3):
        if brett[0][spalte] == brett[1][spalte] == brett[2][spalte] and brett[0][spalte] != " ":
            return brett[0][spalte]  # Return the winner (either test or computer_player)

    # Check diagonals
    if brett[0][0] == brett[1][1] == brett[2][2] and brett[0][0] != " ":
        return brett[0][0]  # Return the winner (either test or computer_player)
    if brett[0][2] == brett[1][1] == brett[2][0] and brett[0][2] != " ":
        return brett[0][2]  # Return the winner (either test or computer_player)

    return None  # No winner yet


# 5.prüfe unentschieden
def pruefe_unentschieden(brett):
    for zeile in brett:
        if " " in zeile:
            return False
    return True



#initialize playground as html table and session_states
def sesstate_playground():
    if 'dfst' not in st.session_state:
        brett = erstelle_brett()
        drucke_brett(brett)
        df = pd.DataFrame(brett)
        df_styled = df.style.applymap(style_cells)
        df_styled = df_styled.set_table_styles([{'selector': 'table', 'props': [('width', '100%')]}])
        st.session_state['dfst'] = df_styled
        st.session_state['brett'] = brett
        html_code = df_styled.to_html()

#update playground(session state)
def update_sessionstate():
    with colplay:
        st.session_state['brett'] = brett
        df = pd.DataFrame(brett)
        df_styled = df.style.applymap(style_cells)
        html_code = df_styled.to_html()
        components.html(
            f"""
                                         <div style="display: flex; justify-content: center; align-items: center;width: auto; height: auto; overflow: auto; text-align: center;">
                                             {html_code}
                                         </div>
                                         """,
            height=350,
            scrolling=False
        )

#load external css file
filepath = pathlib.Path(__file__).parent.parent / "css" / "style_ttt.css"
load_css(filepath)

def initialize_session_state():
    if 'human_player' not in st.session_state:
        st.session_state['human_player'] = ""
    if 'game_over' not in st.session_state:
        st.session_state['game_over'] = False
    if 'brett' not in st.session_state:
        st.session_state['brett'] = ""




st.markdown('**** Welcome to play Tic Tac Toe ****')
clear = st.button("clear")
val = ""
initialize_session_state()

#initialize columns above the form for user name input
(colname, colnambutton, colnametext) = st.columns([1,1,2])

#inuput for player name
with colname:
    playerinput = st.text_input("What is your name", value=st.session_state.get('playername', ""), max_chars=30, key="playername",help=None, autocomplete=None, on_change=None, args=None, kwargs=None, placeholder="your name here", disabled=False, label_visibility="visible")

with colnambutton:
    st.write('')
    button_name = st.button("Enter")

aktueller_spieler = playerinput



# Check if playerinput is not empty
if button_name:
    if playerinput.strip():
        st.session_state['human_player'] = playerinput.strip()
    else:
        st.session_state['human_player'] = ""

#if name is not given write text
if st.session_state['human_player'] == "":
    with colname:
        st.write(f'I need your name to play!')
elif st.session_state['human_player'] != "" :
    test = st.session_state['human_player']

    #initialize form
    with st.form('form_ttt'):
        (cola, colc) = st.columns([1.7, 2])
        (colx, colplay) = st.columns([1, 3])
        (cold, cole) = st.columns([1.7, 2])

        #calculate playground
        sesstate_playground()
        brett = st.session_state.brett

        #greetings and input fields
        with colc:
            st.write(f"Nice to meet you {st.session_state['human_player']}")


        with colx:

            cplay = st.number_input(label="row number", min_value=0, max_value=2, value=st.session_state.get('zeileinput', 0), step=None,
                                    format=None, key="zeileinput", help=None, on_change=None, args=None, kwargs=None,
                                    placeholder=None, disabled=False, label_visibility="visible")
            rplay = st.number_input(label="col number", min_value=0, max_value=2, value=st.session_state.get('spalteinput', 0), step=None,
                                     format=None, key="spalteinput", help=None, on_change=None, args=None, kwargs=None,
                                     placeholder=None, disabled=False, label_visibility="visible")

            zeile = int(cplay)
            st.session_state['cplay'] = zeile
            spalte = int(rplay)
            st.session_state['rplay'] = spalte

        #if equal or won disable the submit button
        with colx:
            submit_input = st.form_submit_button("confirm your input", disabled=st.session_state['game_over'])

        #take the input and put it in the playground and check for winner
        if submit_input:
            mache_zug(brett, aktueller_spieler, zeile, spalte)
            st.session_state['brett'] = brett
            df = pd.DataFrame(brett)

            aktueller_spieler = "Computer"
            zug_computer(brett)
            st.session_state['brett'] = brett
            df = pd.DataFrame(brett)



            winner = pruefe_gewonnen(brett, test)
            if pruefe_gewonnen(brett, test):
                st.session_state['game_over'] = True
                with cole:
                    st.write(f"Congratulation {winner}. You won!")

            elif pruefe_unentschieden(brett):
                st.session_state['game_over'] = True
                with cole:
                    st.write("This is a draw!")
            else:
                with cole:
                    st.write("Go on!")

        #show playground
        brett = st.session_state.brett
        update_sessionstate()


        #hide the submit button if game is over
        if st.session_state['game_over']:
            with colx:
                st.write("Game over. Click clear to restart.")


# Onclick clear reset game by deleting session state and create new one
if clear:
    st.session_state.clear()
    if 'zeileinput' not in st.session_state or st.session_state['zeileinput'] != 0:
        st.session_state['zeileinput'] = 0
    if 'spalteinput' not in st.session_state or st.session_state['spalteinput'] != 0:
        st.session_state['spalteinput'] = 0
    if 'playername' not in st.session_state or st.session_state['playername'] != 0:
        st.session_state['playername'] = 0
    st.rerun()







