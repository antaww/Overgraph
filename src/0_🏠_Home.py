import pandas as pd
import streamlit as st
from owl_module import df, get_heroes_stat, get_heroes_stat_by_player, get_players_stat_by_team, get_team_scores, \
    map_stats, get_players_stat, get_team_profile

st.session_state.map_stats = map_stats
st.session_state.df = df
st.session_state.get_heroes_stat = get_heroes_stat
st.session_state.get_players_stat = get_players_stat
st.session_state.get_heroes_stat_by_player = get_heroes_stat_by_player
st.session_state.get_players_stat_by_team = get_players_stat_by_team
st.session_state.get_team_scores = get_team_scores
st.session_state.get_team_profile = get_team_profile

st.set_page_config(
    page_title="Overgraph",
    page_icon="./src/static/overgraph-logo.png",
)

col1, col2, col3 = st.columns(3)

with col1:
    st.write('')
with col2:
    st.image('src/static/overgraph-removebg-preview.png', use_column_width=True)
with col3:
    st.write('')
st.markdown("""
            ### ☝️🤓 Welcome to :red[Overgraph], a website regrouping every Overwatch League stats.
            ##### Use Overgraph to get a precise analysis of the Overwatch League data like heroes stats, players stats, teams stats and matches analysis.
            ##### Are you ready to dive into the :orange[Overwatch League] data? Let's go! 👇
            ___
            ### 📖 Pages
            ##### 🔥 <a href='Heroes_stats' target='_self' style='text-decoration: underline; color:white'>**Heroes stats**</a> : Get specific stats for every hero\n
            ##### 🏅 <a href='Heroes_stats_by_Player' target='_self' style='text-decoration: underline; color:white'>**Heroes stats by Player**</a> : Get specific stats for every hero of a player\n
            ##### ⚡ <a href='Players_stats' target='_self' style='text-decoration: underline; color:white'>**Players stats**</a> : Get specific stats for a player\n
            ##### 💡 <a href='Players_stats_by_Team' target='_self' style='text-decoration: underline; color:white'>**Players stats by Team**</a> : Get specific stats for a team\n
            ##### ⚔️ <a href='Team_VS_Teams' target='_self' style='text-decoration: underline; color:white'>**Teams VS Teams**</a> : Get team scores against other teams\n
            ##### 📈 <a href='Team_profile' target='_self' style='text-decoration: underline; color:white'>**Team profile**</a> : Get a profile for a team\n
            ##### 🤺 <a href='Match_analysis' target='_self' style='text-decoration: underline; color:white'>**Match analysis**</a> : Get specific stats for a match\n

            ###### *👀 Pssst, you better use the sidebar to navigate through the app, it's easier!*
            ___
            ### 📊 Data
            ##### The data used in this project is from the Overwatch League. It is a professional esports league for the video game Overwatch, produced by its developer Blizzard Entertainment.

            *___Overgraph___ is not affiliate with the Overwatch League or Blizzard Entertainment.*
            """, unsafe_allow_html=True)
