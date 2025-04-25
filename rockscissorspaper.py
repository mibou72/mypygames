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

#style cells per value
def style_cells(val):
    if val == "Winner Player1":
        return "background-color: #819FF7; color: black; width: 90px; height: 90px; border: 1px solid;"
    elif val == "Winner Computer":
        return "background-color: #F7D358; color: black; width: 90px; height: 90px; border: 1px solid;"
    elif val == "Draw":
        return "background-color: #0B610B; color: black; width: 90px; height: 90px; border: 1px solid;"
    else:
        return "background-color: #FFFFFF; color: black; width: 90px; height: 90px; border: 1px solid;"  # Default style


#style attention text below game
st.markdown(
    """
    <style>
    .attention-text {
        background-color: #FF0000;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }

    </style>
    """,
    unsafe_allow_html=True)

#create playground
def create_playground():
    playground = []
    for i in range(3):
        row = [" "*10, " "*10, " "*10]
        playground.append(row)
    return playground

#show playground
def show_playground(playground):
    for row in playground:
        print("|".join(row))
        print("--------------"*3)

#make move human player
def makemove1(playground, player1_move, count):
    playground[count][0] = player1_move

#make move computer
def makemove2(playground, count, player2_move):
    playground[count][1] = player2_move

#check for typos when human player is writing the word
def check_spelling1(player1_move):
    if player1_move == "scissors" or player1_move == "paper" or player1_move == "rock":
        return True
    else:
        return False

#check for the winner
def check_winner_game(playground, player1_move, player2_move, count):
    if player1_move == "scissors" and player2_move == "paper" or player1_move == "rock" and player2_move == "scissors" or player1_move == "paper" and player2_move == "rock":
        playground[count][2] = "Winner Player1"

    if player2_move == "scissors" and player1_move == "paper" or player2_move == "rock" and player1_move == "scissors" or player2_move == "paper" and player1_move == "rock":
        playground[count][2] = "Winner Computer"

    if player1_move == player2_move:
        playground[count][2] = "Draw"


#initialize playground as html table and safe in session state
def sesstate_playground():
    if 'dfst' not in st.session_state:
        playground = create_playground()
        show_playground(playground)
        df = pd.DataFrame(playground)
        df_styled = df.style.applymap(style_cells)
        df_styled = df_styled.set_table_styles([{'selector': 'table', 'props': [('width', '100%')]}])
        df_styled = df_styled.hide(axis="index")
        df_styled = df_styled.hide(axis="columns")
        st.session_state['dfst'] = df_styled
        st.session_state['playground'] = playground
        html_code = df_styled.to_html()
        with colplay:
            components.html(
                f"""
                            <div style="display: flex; justify-content: center; align-items: center;width: auto; height: auto; overflow: auto; text-align: center;">
                                {html_code}
                            </div>
                            """,
                height=300,
                scrolling=False
            )
#update playground(session state)
def update_playground():
    df = pd.DataFrame(playground)
    df_styled = df.style.applymap(style_cells)
    df_styled = df_styled.set_table_styles([{'selector': 'table', 'props': [('width', '100%')]}])
    df_styled = df_styled.hide(axis="index")
    df_styled = df_styled.hide(axis="columns")
    st.session_state['dfst'] = df_styled
    st.session_state['playground'] = playground
    html_code = df_styled.to_html()
    with colplay:
        components.html(
            f"""
                                    <div style="display: flex; justify-content: center; align-items: center;width: auto; height: auto; overflow: auto; text-align: center;">
                                        {html_code}
                                    </div>
                                    """,
            height=300,
            scrolling=False
        )
#removes the input in the input field, but is not working properly therefore only used in clear button
def reset_player1move():
    st.session_state['player1_move'] = ""

#initialize needed session states
def initialize_sessionstate():
    if 'human_player' not in st.session_state:
        st.session_state['human_player'] = ""
    if 'game_over' not in st.session_state:
        st.session_state['game_over'] = False
    if 'count' not in st.session_state:
        st.session_state['count'] = 0
    if 'win_count1' not in st.session_state:
        st.session_state['win_count1'] = 0
    if 'win_count2' not in st.session_state:
        st.session_state['win_count2'] = 0
    if 'win_counte' not in st.session_state:
        st.session_state['win_counte'] = 0
    if 'playground' not in st.session_state:
        st.session_state['playground'] = ""


#load external css file
filepath = pathlib.Path(__file__).parent.parent / "css" / "style_rsp.css"
load_css(filepath)


st.markdown('**** Welcome to play Rock Paper Scissors ****')
clear = st.button("clear", on_click=reset_player1move)



#initialize form with columns
with st.form('form_ttt'):
    (cola, colc) = st.columns([1.4, 2])
    (colx, colplay) = st.columns([1, 3])
    (cold, cole) = st.columns([1.4, 2])

    # show playground
    initialize_sessionstate()
    sesstate_playground()
    playground = st.session_state['playground']


    #greetings and input field
    with colc:
        st.write(f"Welcome Player1, please make your play.")
    with colx:
        user_input = st.text_input(
            label="What is your play?",
            placeholder="scissors/paper/rock",
            disabled=False,
            label_visibility="visible",
            key="player1_move",
            value="")


    player1_move = user_input
    # if equal or won disable the submit button
    with colx:
        submit_input = st.form_submit_button("confirm your input", disabled=st.session_state['game_over'])


    if submit_input:
        count = st.session_state['count']
        #if word is spelled wrong give warning and do nothing
        if not check_spelling1(player1_move):
            with cole:
                st.write('<p class="attention-text">"Please check your spelling</p>', unsafe_allow_html=True)
                update_playground()

        # take input and check for winner
        else:
            win_count1 = 0
            win_count2 = 0
            win_counte = 0

            makemove1(st.session_state['playground'], player1_move, count)

            words = ["scissors", "paper", "rock"]
            player2_move = random.choice(words)
            makemove2(st.session_state['playground'], count, player2_move)
            check_winner_game(st.session_state['playground'], player1_move, player2_move, count)

            if st.session_state['playground'][count][2] == "Winner Player1":
                st.session_state['win_count1'] += 1
            elif st.session_state['playground'][count][2] == "Winner Computer":
                st.session_state['win_count2'] += 1
            else:
                st.session_state['win_counte'] += 1

            if st.session_state['win_count1'] >= st.session_state['win_count2'] and st.session_state['win_count1'] >= 2:
                st.session_state['game_over'] = True
                with cole:
                    st.write("Congratulations Player 1, you won the tournament.")
            elif st.session_state['win_count2'] >= st.session_state['win_count1'] and st.session_state['win_count2'] >= 2:
                st.session_state['game_over'] = True
                with cole:
                    st.write("Sorry, the computer won the tournament.")
            elif st.session_state['win_count1'] < 2 and st.session_state['win_count2'] < 2 and st.session_state[
                'win_count1'] + st.session_state['win_count2'] + st.session_state['win_counte'] >= 3:
                st.session_state['game_over'] = True
                with cole:
                    st.write("Draw - No winner in the game.")

            update_playground()
            count = st.session_state['count'] + 1
            st.session_state['count'] = count
            st.session_state['clear_input'] = True



if st.session_state['game_over']:
    with colx:
        st.write("Game over. Click clear to restart.")



# Onclick clear reset game by deleting session state and create new one
if clear:
    st.session_state.clear()
    st.rerun()

