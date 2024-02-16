import math
import os
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Overgraph - Teams leaderboard",
    page_icon="./src/static/overgraph-logo.png"
)


def display_page_infos():
    st.subheader('Teams Winrate Leaderboard')
    st.markdown("""
                This page displays a leaderboard of teams based on their winrate globally or on a stage. 
                The leaderboard provides a comprehensive overview of each team's performance in the Overwatch League.
                Analyzing these stats could help to understand the ranking of the teams and their performance.
                """)


try:
    df = st.session_state.df
    get_teams_leaderboard = st.session_state.get_teams_leaderboard

    stages_list = df['stage'].unique()
    display_page_infos()
    stage = st.selectbox('Select a stage (not required)', [''] + list(stages_list))
    if not stage:
        stage = None
    data = get_teams_leaderboard(stage)

    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        if data.empty:
            st.error('No data available for this stage')
        else:
            st.write(data)
    with viz_tab:
        if data.empty:
            st.error('No data available for this stage')
        else:
            fig = px.bar(data, x='Winrate', y='Team', title='Teams Winrate Leaderboard',
                         labels={'Winrate': 'Winrate', 'Team': 'Team'},
                         color_discrete_sequence=px.colors.qualitative.Pastel)

            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig)
except AttributeError:
    st.error('You need to load the data from the Home page first !')
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
