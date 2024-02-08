import pandas as pd
import streamlit as st
from owl_module import df, get_heroes_stat, get_heroes_stat_by_player, get_players_stat_by_team, get_team_scores, \
    map_stats

st.session_state.map_stats = map_stats
st.session_state.df = df
st.session_state.get_heroes_stat = get_heroes_stat
st.session_state.get_heroes_stat_by_player = get_heroes_stat_by_player
st.session_state.get_players_stat_by_team = get_players_stat_by_team
st.session_state.get_team_scores = get_team_scores

st.set_page_config(
    page_title="Overgraph",
    page_icon="👋",
)

st.title('Overgraph')
st.markdown("""
            Welcome to Overgraph, a project to analyze Overwatch League data.
            You can navigate through the sidebar to get stats about heroes, players, teams and matches.
            """)
st.sidebar.markdown("""
                    ##### *👀 Pssst, you better use the sidebar to navigate through the app, it's easier!*
                    """)
