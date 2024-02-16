import os

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Overgraph - Match analysis",
    page_icon="./src/static/overgraph-logo.png"
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
    get_match_analysis_all_stats = st.session_state.get_match_analysis_all_stats
    get_match_analysis_heroes_played = st.session_state.get_match_analysis_heroes_played

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

        for i in range(len(maps)):
            with map_tabs[i]:
                st.subheader(f'Global stats for {maps[i]}')
                global_stats = get_match_analysis_all_stats(stage, int(match_id), maps[i])
                teams = global_stats['Team'].unique()
                stat_list = global_stats['Stat'].unique()

                # do the sum of each stat for each team
                global_stats_by_team = global_stats.groupby(['Team', 'Stat']).sum().reset_index()
                # drop columns that are not useful (Hero, Player, Role)
                global_stats_by_team = global_stats_by_team.drop(columns=['Hero', 'Player', 'Role'])

                # create a radar chart that compares the stats of the two teams
                team_one_stats = global_stats_by_team[global_stats_by_team['Team'] == teams[0]]
                team_two_stats = global_stats_by_team[global_stats_by_team['Team'] == teams[1]]

                team_one_color = 'rgba(0, 0, 255, 0.5)'
                team_two_color = 'rgba(255, 0, 0, 0.5)'

                # Normalize the stats to have a value between 0 and 100
                for stat in stat_list:
                    max_value = max(global_stats_by_team[global_stats_by_team['Stat'] == stat]['Stat Amount'])
                    global_stats_by_team.loc[global_stats_by_team['Stat'] == stat, 'Stat Amount'] = \
                        global_stats_by_team[global_stats_by_team['Stat'] == stat]['Stat Amount'] / max_value * 100

                fig = go.Figure()
                for team in teams:
                    team_stats = global_stats_by_team[global_stats_by_team['Team'] == team]
                    fig.add_trace(go.Scatterpolar(
                        r=team_stats['Stat Amount'],
                        theta=team_stats['Stat'],
                        fill='toself',
                        name=team,
                        line=dict(
                            color=team_one_color if team == team_one_stats['Team'].unique()[0] else team_two_color)
                    ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)

                st.write("""
                This radar chart compares the stats of the two teams. The stats are normalized to have a value between 0
                 and 100. The team with the highest value value for a stat is considered as the max value. So the other
                 team's value is calculated as a percentage of the max value.
                """)

                st.markdown("___")
                st.subheader(f'Time Played by heroes for each teams in {maps[i]}')
                heroes_played = get_match_analysis_heroes_played(stage, int(match_id), maps[i], all=False)
                teams = heroes_played['Team'].unique()
                figures = []
                players_name = []
                for team in teams:
                    players = heroes_played[heroes_played['Team'] == team]['Player'].unique()
                    for player in players:
                        player_heroes = heroes_played[
                            (heroes_played['Team'] == team) & (heroes_played['Player'] == player)]
                        trace = go.Bar(x=player_heroes['Hero'], y=player_heroes['Time Played'], name=player)
                        figures.append(trace)
                        players_name.append(player)

                total_players = len(players_name)

                team_one_subplots = make_subplots(rows=2, cols=3, subplot_titles=players_name[:total_players // 2])
                team_one_subplots.update_layout(title_text=f'Heroes played for each player of {teams[0]}', bargap=0.5)
                team_two_subplots = make_subplots(rows=2, cols=3, subplot_titles=players_name[total_players // 2:])
                team_two_subplots.update_layout(title_text=f'Heroes played for each player of {teams[1]}', bargap=0.5)

                half_players = total_players // 2

                for i in range(half_players):
                    team_one_subplots.add_trace(figures[i], row=(i // 3) + 1, col=(i % 3) + 1)

                for i in range(half_players, total_players):
                    team_two_subplots.add_trace(figures[i], row=((i - half_players) // 3) + 1,
                                                col=((i - half_players) % 3) + 1)
                st.plotly_chart(team_one_subplots, use_container_width=True)
                st.plotly_chart(team_two_subplots, use_container_width=True)

                st.markdown("___")
                st.subheader(f'Compare players stats ')


except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
