import os
import streamlit as st

try:
    df = st.session_state.df
    get_heroes_stat = st.session_state.get_heroes_stat

    stats_list = df['stat'].unique()
    # todo: sort the list
    st.subheader('Get specific stats for every hero')
    # create a dropdown list with every unique 'stat'
    stat = st.selectbox('Select a stat', stats_list)
    # display the result
    st.write(get_heroes_stat(stat))
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)



