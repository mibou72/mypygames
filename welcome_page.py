import streamlit as st

st.markdown(
    """
    <style>
    .title {
        background-color: #BCF5A9;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 50px;
    }
    .startpagetext {
        background-color: #FFFFF;
        font-size: 15px;
        font-weight: normal;
        text-align: left;
        margin-top: 50px;
    }
    .y {
        background-color: #FFFF00;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True)

    
#overwiev site for games
st.write('<p class="title">Welcome to my games page.</p>', unsafe_allow_html=True,)
st.write('<p class="startpagetext">This is my first Streamlit Page.</p>', unsafe_allow_html=True)
st.write('<p class="startpagetext">You can play different games as seen in the navigation.</p>', unsafe_allow_html=True)
st.write('<p class="startpagetext">Please be cautius at the games with text input. Unfortunately it is not possible to delete your input after '
         'submission. You have to delete it yourself befor you can submit your next input.</p>', unsafe_allow_html=True)