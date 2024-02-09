import os
import streamlit as st

try:
    map_stats = st.session_state.map_stats
    df = st.session_state.df
    get_team_scores = st.session_state.get_team_scores

    st.set_page_config(
        page_title="Overgraph - Team VS Teams",
        page_icon="⚔️",
    )
    teams_list = df['team'].unique()
    map_types_list = df['map_type'].str.title().unique()

    st.subheader('Get team scores against other teams')
    # create a dropdown list with every unique 'stat'
    team = st.selectbox('Select a team', teams_list)
    map_type = st.selectbox('Select a map (not required)', [''] + list(map_types_list))
    st.markdown('_**Only Matches** column means : if the score is based on the whole match or only the map_')
    # display the result
    try:
        st.write(get_team_scores(team, map_type))
    except KeyError:
        st.error('No data available for this team and this map type')
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)



