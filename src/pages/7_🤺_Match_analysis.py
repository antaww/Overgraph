import os

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set the page configuration
st.set_page_config(
    page_title="Overgraph - Match analysis",  # The title of the page
    page_icon="./src/static/overgraph-logo.png"  # The icon of the page
)


def display_page_infos():
    """
    This function displays the information of the page.

    It uses the Streamlit library to display a subheader and a markdown text.
    """
    st.subheader('Analyse a match')
    st.markdown("""
                    The collected datas provide a comprehensive overview of one **team's performances on different maps**.
                    The records indicate the team's composition and the corresponding winrate.
                    For a high level team coach, it is important to analyze the team's performance on different maps to understand their strengths and weaknesses.
                    It could help inform strategic decision-making going forward.
                    """)


try:
    # Get the dataframe and the function to get player stats from the session state
    map_stats = st.session_state.map_stats
    df = st.session_state.df
    get_match_analysis_all_stats = st.session_state.get_match_analysis_all_stats
    get_match_analysis_heroes_played = st.session_state.get_match_analysis_heroes_played
    get_match_analysis_heroes_stats = st.session_state.get_match_analysis_heroes_stats

    # Get the list of unique teams and stats from the dataframe
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

    maps = map_stats[map_stats['match_id'] == float(match_id)]['map_name'].unique()

    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        st.write('Map stats :')
        st.write(map_stats[map_stats['match_id'] == float(match_id)])
        st.write('Match stats :')
        st.write(df[df['match_id'] == float(match_id)])
    with viz_tab:
        match_winner = map_stats[map_stats['match_id'] == float(match_id)]['match_winner'].unique()[0]
        team_one = map_stats[map_stats['match_id'] == float(match_id)]['team_one_name'].unique()[0]
        team_two = map_stats[map_stats['match_id'] == float(match_id)]['team_two_name'].unique()[0]
        start_time = map_stats[map_stats['match_id'] == float(match_id)]['round_start_time'].unique()[0]
        st.title(f'{team_one} vs {team_two} ({start_time}) - Winner : {match_winner}')
        map_tabs = st.tabs([map_name for map_name in maps])

        for i in range(len(maps)):
            with map_tabs[i]:
                map_winner = map_stats[(map_stats['match_id'] == float(match_id)) & (map_stats['map_name'] == maps[i])][ \
                    'map_winner'].unique()[0]
                st.subheader(f'Overall stats for {maps[i]} - Winner : {map_winner}')
                global_stats = get_match_analysis_all_stats(stage, float(match_id), maps[i])
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

                st.write(
                    'These bar charts show the time played by each hero for each player of each team (in seconds).')
                heroes_played = get_match_analysis_heroes_played(stage, float(match_id), maps[i], all=False)
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

                for h in range(half_players):
                    team_one_subplots.add_trace(figures[h], row=(h // 3) + 1, col=(h % 3) + 1)

                for m in range(half_players, total_players):
                    team_two_subplots.add_trace(figures[m], row=((m - half_players) // 3) + 1,
                                                col=((m - half_players) % 3) + 1)
                st.plotly_chart(team_one_subplots, use_container_width=True)
                st.plotly_chart(team_two_subplots, use_container_width=True)

                st.markdown("___")
                st.subheader(f'Compare players stats ')

                st.write("""
                This part allows you to compare the stats of two players from each team. You can choose 
                to compare the stats of all heroes or the stats of a specific hero.
                \n
                By using these charts, you can compare the stats of two players to see who is the best in a specific
                stat or for a specific hero. With these informations, you can make strategic decisions for the next
                match, and you can know the strengths and weaknesses of each player.
                \n
                We used the same way to normalize the stats as the radar chart before.
                \n\n\n
                """)

                team_one_players = heroes_played[heroes_played['Team'] == teams[0]]['Player'].unique()
                team_two_players = heroes_played[heroes_played['Team'] == teams[1]]['Player'].unique()

                st.subheader('Configure the comparison :')

                # create 2 columns to display the selectbox for each team
                col1, col2 = st.columns(2)
                with col1:
                    team_one_player = st.selectbox(f'Choose a player from {teams[0]}', team_one_players,
                                                   key=f'team_one_player_select_{maps[i]}')
                with col2:
                    team_two_player = st.selectbox(f'Choose a player from {teams[1]}', team_two_players,
                                                   key=f'team_two_player_select_{maps[i]}')

                radio = st.radio('Compare to :', ['All heroes', 'Specific hero'], key=f'radio_{maps[i]}')
                if radio == 'Specific hero':
                    team_one_player_heroes = heroes_played[heroes_played['Player'] == team_one_player]['Hero'].unique()
                    team_two_player_heroes = heroes_played[heroes_played['Player'] == team_two_player]['Hero'].unique()

                    # add 'All heroes' to the list of heroes to make it possible to compare if a player many heroes
                    team_one_player_heroes = list(team_one_player_heroes)
                    if len(team_one_player_heroes) > 1:
                        team_one_player_heroes.append('All heroes')
                    team_two_player_heroes = list(team_two_player_heroes)
                    if len(team_two_player_heroes) > 1:
                        team_two_player_heroes.append('All heroes')

                    col1, col2 = st.columns(2)
                    with col1:
                        team_one_player_hero = st.selectbox(f'Choose a hero for {team_one_player}',
                                                            team_one_player_heroes,
                                                            key=f'team_one_player_hero_select_{maps[i]}')
                    with col2:
                        team_two_player_hero = st.selectbox(f'Choose a hero for {team_two_player}',
                                                            team_two_player_heroes,
                                                            key=f'team_two_player_hero_select_{maps[i]}')

                    if team_one_player_hero != 'All heroes':
                        all_heroes = False
                        team_one_player_stats = get_match_analysis_heroes_stats(stage, float(match_id), maps[i],
                                                                                team_one_player, all_heroes,
                                                                                team_one_player_hero)
                    else:
                        team_one_player_hero = 'All heroes'
                        all_heroes = True
                        team_one_player_stats = get_match_analysis_heroes_stats(stage, float(match_id), maps[i],
                                                                                team_one_player, all_heroes)

                    if team_two_player_hero != 'All heroes':
                        all_heroes = False
                        team_two_player_stats = get_match_analysis_heroes_stats(stage, float(match_id), maps[i],
                                                                                team_two_player, all_heroes,
                                                                                team_two_player_hero)
                    else:
                        team_two_player_hero = 'All heroes'
                        all_heroes = True
                        team_two_player_stats = get_match_analysis_heroes_stats(stage, float(match_id), maps[i],
                                                                                team_two_player, all_heroes)
                else:
                    team_one_player_hero = 'All heroes'
                    team_two_player_hero = 'All heroes'
                    all_heroes = True
                    team_one_player_stats = get_match_analysis_heroes_stats(stage, float(match_id), maps[i],
                                                                            team_one_player, all_heroes)
                    team_two_player_stats = get_match_analysis_heroes_stats(stage, float(match_id), maps[i],
                                                                            team_two_player, all_heroes)

                # remove lines with stat that are not in common
                common_stats = list(set(team_one_player_stats['Stat']).intersection(team_two_player_stats['Stat']))
                team_one_player_stats = team_one_player_stats[team_one_player_stats['Stat'].isin(common_stats)]
                team_two_player_stats = team_two_player_stats[team_two_player_stats['Stat'].isin(common_stats)]

                # Normalize the stats to have a value between 0 and 100
                for stat in common_stats:
                    max_value = max(team_one_player_stats[team_one_player_stats['Stat'] == stat]['Stat Amount'].max(),
                                    team_two_player_stats[team_two_player_stats['Stat'] == stat]['Stat Amount'].max())
                    team_one_player_stats.loc[team_one_player_stats['Stat'] == stat, 'Stat Amount'] = \
                        team_one_player_stats[team_one_player_stats['Stat'] == stat]['Stat Amount'] / max_value * 100
                    team_two_player_stats.loc[team_two_player_stats['Stat'] == stat, 'Stat Amount'] = \
                        team_two_player_stats[team_two_player_stats['Stat'] == stat]['Stat Amount'] / max_value * 100

                # use a radar chart to compare the stats of the two players
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=team_one_player_stats['Stat Amount'],
                    theta=team_one_player_stats['Stat'],
                    fill='toself',
                    name=team_one_player,
                    line=dict(color=team_one_color)
                ))
                fig.add_trace(go.Scatterpolar(
                    r=team_two_player_stats['Stat Amount'],
                    theta=team_two_player_stats['Stat'],
                    fill='toself',
                    name=team_two_player,
                    line=dict(color=team_two_color)
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

except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
