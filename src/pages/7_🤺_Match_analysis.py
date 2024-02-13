import os

import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Overgraph - Match analysis",
    page_icon="./src/img/overgraph-logo.png"
)


def display_page_infos():
    st.subheader('Analyse a match')
    st.markdown("""
                    The collected datas provide a comprehensive overview of one **team's performances on different maps**.
                    The records indicate the team's composition and the corresponding winrate.
                    For a high level team coach, it is important to analyze the team's performance on different maps to understand their strengths and weaknesses.
                    It could help inform strategic decision-making going forward.
                    """)


try:
    # team_one_tab, team_two_tab = st.tabs(["Winner Team", "Looser Team"])
    map_stats = st.session_state.map_stats
    df = st.session_state.df

    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()

    display_page_infos()
    year = st.selectbox('Select a year', [2018, 2019, 2020, 2021, 2022, 2023])

    stage_list = [stage for stage in df['stage'].unique() if str(year) in stage]
    stage = st.selectbox('Select a stage', stage_list)

    stage_match = df[df['stage'] == stage]
    match_id_list: pd.DataFrame = stage_match['match_id'].unique()
    match_list = []
    for match_id in match_id_list:
        match = map_stats[map_stats['match_id'] == match_id]
        if match.empty:
            continue
        team_one = match[match['match_id'] == match_id]['team_one_name'].unique()[0]
        team_two = match[match['match_id'] == match_id]['team_two_name'].unique()[0]
        date = match[match['match_id'] == match_id]['round_start_time'].unique()[0]
        match_list.append(f"{date} - {team_one} vs {team_two} ({match_id})")

    if len(match_list) == 0:
        st.write('No match found for this stage')
        st.stop()
    match = st.selectbox('Select a match', match_list)
    match_id = match.split('(')[1].split(')')[0]


    maps = map_stats[map_stats['match_id'] == int(match_id)]['map_name'].unique()

    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        st.write('Map stats :')
        st.write(map_stats[map_stats['match_id'] == int(match_id)])
        st.write('Match stats :')
        st.write(df[df['match_id'] == int(match_id)])
    with viz_tab:
        map_tabs = st.tabs([map_name for map_name in maps])

except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
