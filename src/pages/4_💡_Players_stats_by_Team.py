import os
import streamlit as st

st.set_page_config(
    page_title="Overgraph - Players stats by Team",
    page_icon="💡",
)
try:
    df = st.session_state.df
    get_players_stat_by_team = st.session_state.get_players_stat_by_team

    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()

    st.subheader('Get specific stats for a team')
    # create a dropdown list with every unique 'stat'
    team = st.selectbox('Select a team', teams_list)
    stat = st.selectbox('Select a stat', stats_list)
    # display the result
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    with df_tab:
        st.write(get_players_stat_by_team(stat, team))
    with viz_tab:
        st.subheader(f'{team}\'s {stat} stats')
        data = get_players_stat_by_team(stat, team)
        st.bar_chart(data)
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
