import pathlib
import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components

#style info text
st.markdown(
    """
    <style>
    .ok-text {
        background-color: #088A29;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    .attention-text {
        background-color: #FF0000;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    .won-text {
        background-color: #FFFF00;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True)


# Function to style cells based on the "cell value" column
def style_cells(val):
    if val == "#":
        return "background-color: #BCF5A9; color: black; width: 30px;"
    elif val == "0":
        return "background-color: #40FF00; color: black; width: 30px;"
    elif val == "*":
        return "background-color: #FF0000; color: black; width: 30px;"
    elif val == "1":
        return "background-color: #F3F781; color: black; width: 30px;"
    elif val == "2":
        return "background-color: #F7D358; color: black; width: 30px;"
    elif val == "3":
        return "background-color: #FAAC58; color: black; width: 30px;"
    elif val == "4":
        return "background-color: #FE642E; color: black; width: 30px;"
    else:
        return "background-color: #BCF5A9; color: black; width: 30px;"  # Default style




#function to load css file from css folder
def load_css(filepath):
    with open(filepath) as f:
        css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)

#create hidden playground
def create_hiddenplayground():
    hidden = []
    for i in range(10):
        row = [0]*10
        hidden.append(row)
    return hidden

# print hidden playground
def print_hiddenplayground(hidden):
    print_col = 0
    columns = ["0"]
    for i in range(9):
        print_col = " " + str(int(print_col) + 1)
        columns.append(print_col)

#create the playground
def create_playground():
    pgr =[]
    for i in range(10):
        row = ["#"]*10
        pgr.append(row)
    return pgr

# print playground
def print_playground(pgr):
    print_col = 0
    columns = [" 0"]
    for i in range(9):
        print_col = " " + str(int(print_col) + 1)
        columns.append(print_col)

# set bombs
def set_bombs(hidden):
    counter = 2
    for i in range(counter):
        for index, row in enumerate(hidden):
            col = random.randint(0, 9)
            hidden[index][col] = -1
            counter = counter - 1

#count how many bombs are the neighbor of a cell and set a number
def complete_hidden(hidden):
    for cp, inner_list in enumerate(hidden):
        for rp, element in enumerate(inner_list):
            if hidden[cp][rp] == -1:
                continue
            if hidden[cp][rp] == 0:
                try:
                    if hidden[cp - 1][rp] == -1 and cp > 0:
                        hidden[cp][rp] += 1
                except IndexError:
                    continue
                try:
                    if hidden[cp][rp - 1] == -1 and rp > 0:
                        hidden[cp][rp] += 1
                except IndexError:
                    continue
                try:
                    if hidden[cp + 1][rp] == -1 and cp < 10:
                       hidden[cp][rp] += 1
                except IndexError:
                    continue
                try:
                    if hidden[cp][rp + 1] == -1 and rp < 10:
                        hidden[cp][rp] += 1
                except IndexError:
                    continue
                try:
                    if hidden[cp + 1][rp + 1] == -1 and cp < 10 and rp < 10:
                        hidden[cp][rp] += 1
                except IndexError:
                    continue
                if hidden[cp - 1][rp - 1] == -1 and cp > 0 and rp > 0:
                    continue
                try:
                    if hidden[cp + 1][rp - 1] == -1 and cp < 10 and rp > 0:
                        hidden[cp][rp] += 1
                except IndexError:
                    continue
                try:
                    if hidden[cp - 1][rp + 1] == -1 and cp > 0 and rp < 10:
                        hidden[cp][rp] += 1
                except IndexError:
                    continue

#if the choosen cell equals -1 in hidden playground (=bomb) than fill * in the playground and inform about the loss
def lost(rp, cp):
    if hidden[rp][cp] == -1:
        for rp, inner_list in enumerate(pgr):
                for cp, element in enumerate(inner_list):
                    pgr[rp][cp] = str(hidden[rp][cp])
                    if pgr[rp][cp] == "-1":
                        pgr[rp][cp] = "*"
        st.write('<p class="attention-text">\n===== ** KABOOOOM ** =====</p>', unsafe_allow_html=True)
        st.write('<p class="attention-text">Sorry, you lost.</p>', unsafe_allow_html=True)
        return True

#if the choosen cell is no bomb, fill in the number from the hidden playground
def ok(rp, cp):
    if pgr[rp][cp] == "#":
        pgr[rp][cp] = str(hidden[rp][cp])
        st.write('<p class="ok-text">\n=== Well done. Go on ======</p>', unsafe_allow_html=True)
        return True

#if there is no empty field to discover fill the playground with the data from hiddenplayground and inform about the win
def won(rp, cp):
    if "#" in pgr == False:
       for rp, inner_list in enumerate(pgr):
            for cp, element in enumerate(inner_list):
                pgr[rp][cp] = str(hidden[rp][cp])
                if pgr[rp][cp] == "-1":
                    pgr[rp][cp] = "*"
       st.write('<p class="won-text">\n=====Congrats ======</p>', unsafe_allow_html=True)
       st.write('<p class="won-text">You mastered the game.</p>', unsafe_allow_html=True)
       return True




#initialize playground as html table and session states
def sesstate_playground():
    if 'df1st' not in st.session_state:
        hidden = create_hiddenplayground()
        set_bombs(hidden)
        complete_hidden(hidden)
        print_hiddenplayground(hidden)
        df1 = pd.DataFrame(hidden)
        st.session_state['df1st'] = df1
        st.session_state['hiddenst'] = hidden

    if 'df2st' not in st.session_state:
        pgr = create_playground()
        print_playground(pgr)
        df2 = pd.DataFrame(pgr)
        df2_styled = df2.style.applymap(style_cells)
        df2_styled = df2_styled.set_table_styles([{'selector': 'table', 'props': [('width', '100%')]}])
        st.session_state['df2st'] = df2_styled
        st.session_state['pgrst'] = pgr
        html_code = df2_styled.to_html()
        with col4:
            components.html(
                f"""
                    <div style="display: flex; justify-content: center; align-items: center;width: auto; height: auto; overflow: auto; text-align: center;">
                        {html_code}
                    </div>
                    """,
                height=500,
                scrolling=False
            )

def update_playground():
    with col4:
        df2 = pd.DataFrame(pgr)
        df2_styled = df2.style.applymap(style_cells)
        html_code = df2_styled.to_html()
        components.html(
            f"""
                <div style="display: flex; justify-content: center; align-items: center;width: auto; height: auto; overflow: auto; text-align: center;">
                    {html_code}
                </div>
                """,
            height=500,
            scrolling=False
        )

#initialize sesstion_state game_over
if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False

#load external css file
filepath = pathlib.Path(__file__).parent / "css" / "style_mw.css"
load_css(filepath)


#headline
st.markdown('**** Welcome to play minesweeper ****')

#form to hold the input fields and the buttons with 5 columns
(col1, colx) = st.columns([1,0.1])
with col1:
    clear = st.button('start/clear')


with st.form('form_mw'):
    (colx, colbutt1, colbutt2, colinp) = st.columns([0.3,0.8, 0.8, 2])
    (col4, colx) = st.columns([1,0.4])

    with colinp:
        st.write(" ")
        submit = st.form_submit_button('confirm input', disabled=st.session_state['game_over'])

    with colbutt1:
        rp = st.number_input(label="choose row", min_value=None, max_value=9, value="min", step=None,
                       format=None,
                       key="row_input_player", help=None, on_change=None, args=None, kwargs=None,
                       placeholder=None,
                       disabled=False, label_visibility="visible")
    with colbutt2:
        cp = st.number_input(label="choose column", min_value=None, max_value=9, value="min", step=None,
                       format=None, key="col_input_player", help=None, on_change=None, args=None, kwargs=None,
                       placeholder=None, disabled=False, label_visibility="visible")

#create initial session states
sesstate_playground()
hidden = st.session_state['hiddenst']
pgr = st.session_state['pgrst']

#onclick button check input against hidden playground and show results in playground(pgr)
if submit:
    if rp < 0 or rp > 9 or cp < 0 or cp > 9:
        st.write(f"\nYou are only allowed to set 0 - 9  for row and 0 - 9 for cp.\n")
    try:
        if st.session_state['rpinput'] == rp and st.session_state['cpinput'] == cp:
            st.write('<p class="attention-text">You had this cell already.</p>', unsafe_allow_html=True)
    except KeyError:
        pass

    st.session_state['rpinput'] = rp
    st.session_state['cpinput'] = cp

    if lost(rp, cp) == True:
        st.session_state['pgrst'] = pgr
        st.session_state['df2st'] = pd.DataFrame(pgr)
        st.session_state['game_over'] = True


    if ok(rp, cp) == True:
        st.session_state['pgrst'] = pgr
        st.session_state['df2st'] = pd.DataFrame(pgr)


    if won(rp, cp) == True:
        st.session_state['pgrst'] = pgr
        st.session_state['df2st'] = pd.DataFrame(pgr)
        st.session_state['game_over'] = True

    update_playground()

if st.session_state['game_over']:
    with colx:
        st.write("Game over. Click clear to restart.")

#onlick clear reset game by deleting session state and create new one
if clear:
    del st.session_state['df1st']
    del st.session_state['df2st']
    if st.session_state['game_over'] == True:
        del st.session_state['game_over']
    sesstate_playground()











