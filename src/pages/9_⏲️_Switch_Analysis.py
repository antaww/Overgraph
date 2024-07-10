import base64
import os

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Overgraph - Detailed match analysis",
    page_icon="./src/static/overgraph-logo.png"
)


def display_page_infos():
    st.subheader('Detailed match analysis')
    st.markdown("""
                    The collected datas provide a comprehensive overview of one specific match in the Overwatch League.
                    This page will sho a detailed analysis of the match, by adding the switch timings to the match statistics.
                    It will focus on the match Los Angeles Valiant vs. San Francisco Shock, played on 2018-01-11.
                    """)


try:
    display_page_infos()
    map_stats = st.session_state.map_stats
    df = st.session_state.df
    get_match_analysis_all_stats = st.session_state.get_match_analysis_all_stats
    get_match_analysis_heroes_played = st.session_state.get_match_analysis_heroes_played
    get_match_analysis_heroes_stats = st.session_state.get_match_analysis_heroes_stats
    get_switches = st.session_state.get_switches

    match_id = 10223
    stage = '2018 : Overwatch League - Stage 1'
    maps = map_stats[map_stats['match_id'] == int(match_id)]['map_name'].unique()

    match_winner = map_stats[map_stats['match_id'] == int(match_id)]['match_winner'].unique()[0]
    team_one = map_stats[map_stats['match_id'] == int(match_id)]['team_one_name'].unique()[0]
    team_two = map_stats[map_stats['match_id'] == int(match_id)]['team_two_name'].unique()[0]
    start_time = map_stats[map_stats['match_id'] == int(match_id)]['round_start_time'].unique()[0]
    st.title(f'{team_one} vs {team_two} ({start_time}) - Winner : {match_winner}')
    map_tabs = st.tabs([map_name for map_name in maps])

    switches = get_switches()

    for i in range(len(maps)):
        with map_tabs[i]:
            map_winner = map_stats[(map_stats['match_id'] == int(match_id)) & (map_stats['map_name'] == maps[i])][ \
                'map_winner'].unique()[0]
            st.subheader(f'Overall stats for {maps[i]} - Winner : {map_winner}')
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

            st.write('These bar charts show the time played by each hero for each player of each team (in seconds).')
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
                    team_one_player_stats = get_match_analysis_heroes_stats(stage, int(match_id), maps[i],
                                                                            team_one_player, all_heroes,
                                                                            team_one_player_hero)
                else:
                    team_one_player_hero = 'All heroes'
                    all_heroes = True
                    team_one_player_stats = get_match_analysis_heroes_stats(stage, int(match_id), maps[i],
                                                                            team_one_player, all_heroes)

                if team_two_player_hero != 'All heroes':
                    all_heroes = False
                    team_two_player_stats = get_match_analysis_heroes_stats(stage, int(match_id), maps[i],
                                                                            team_two_player, all_heroes,
                                                                            team_two_player_hero)
                else:
                    team_two_player_hero = 'All heroes'
                    all_heroes = True
                    team_two_player_stats = get_match_analysis_heroes_stats(stage, int(match_id), maps[i],
                                                                            team_two_player, all_heroes)
            else:
                team_one_player_hero = 'All heroes'
                team_two_player_hero = 'All heroes'
                all_heroes = True
                team_one_player_stats = get_match_analysis_heroes_stats(stage, int(match_id), maps[i],
                                                                        team_one_player, all_heroes)
                team_two_player_stats = get_match_analysis_heroes_stats(stage, int(match_id), maps[i],
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
            st.markdown("___")
            st.subheader(f'Switches for {maps[i]}')
            st.write('This part will show the switches that occured during the match on this map.')

            first_composition = switches.drop_duplicates(subset=['player', 'map'])
            first_composition = first_composition[first_composition['map'] == maps[i]]
            first_team_fc = first_composition[first_composition['team'] == 'Los Angeles Valiant']
            first_team_fc = first_team_fc[['player', 'hero']]
            first_team_fc['img'] = first_team_fc['hero'].str.lower().str.replace('.', '').str.replace('ú',
                                                                                                      'u').str.replace(
                ' ', '').str.replace(':', '')
            second_team_fc = first_composition[first_composition['team'] == 'San Francisco Shock']
            second_team_fc = second_team_fc[['player', 'hero']]
            second_team_fc['img'] = second_team_fc['hero'].str.lower().str.replace('.', '').str.replace('ú',
                                                                                                        'u').str.replace(
                ' ', '').str.replace(':', '')
            # Utilisation de HTML dans Streamlit
            html_content = """
            <div>
                <h3>Start composition for Los Angeles Valiant</h3>
                <div class="team" style="display: flex; gap: 2rem;">
            """
            for index, row in first_team_fc.iterrows():
                html_content += f"<div style='display: flex; flex-direction: column; align-items: center;'><p>{row['player']}</p>"
                with open(f'src/static/{row["img"]}.png', 'rb') as f:
                    img = base64.b64encode(f.read()).decode()
                html_content += f"<img src='data:image/png;base64,{img}' width='50' height='50'><p style='font-style: italic;'>{row['hero']}</p></div>"
            html_content += """
                </div>
                <h3>Start composition for San Francisco Shock</h3>
                <div class="team" style="display: flex; gap: 2rem;">
            """
            for index, row in second_team_fc.iterrows():
                html_content += f"<div style='display: flex; flex-direction: column; align-items: center;'><p>{row['player']}</p>"
                with open(f'src/static/{row["img"]}.png', 'rb') as f:
                    img = base64.b64encode(f.read()).decode()
                html_content += f"<img src='data:image/png;base64,{img}' width='50' height='50'><p style='font-style: italic;'>{row['hero']}</p></div>"

            switches_map = switches[switches['map'] == maps[i]]
            switches_map = switches_map[switches_map['player'].map(switches_map['player'].value_counts()) > 1]
            switches_map = switches_map[switches_map['timing'] != "0"]
            switches_map['hero_img'] = switches_map['hero'].str.lower().str.replace('.', '').str.replace('ú',
                                                                                                         'u').str.replace(
                ' ', '').str.replace(':', '')
            switches_map['from_img'] = switches_map['from'].str.lower().str.replace('.', '').str.replace('ú',
                                                                                                         'u').str.replace(
                ' ', '').str.replace(':', '')
            # order it by timing
            switches_map = switches_map.sort_values(by=['timing'])

            html_content += """
                </div>
            </div>
            <div>
                <h3>Switches</h3>
                <div class="switches" style="display: flex; gap: 1rem; flex-direction: column;">
            """
            for index, row in switches_map.iterrows():
                html_content += (f"<div style='display: flex; flex-direction: row; align-items: center; gap: 1rem;'>"
                                 f"<p style='font-style: bold;'>{row['timing']}</p>")
                with open(f'src/static/{row['from_img']}.png', 'rb') as f:
                    from_img = base64.b64encode(f.read()).decode()
                html_content += (f"<div style='display: flex; flex-direction: column; align-items: center;'>"
                                 f"<p style='margin: 0;'>{row['player']}</p>"
                                 f"<img src='data:image/png;base64,{from_img}' width='50' height='50'>"
                                 f"<p style='font-style: italic;'>{row['from']}</p>"
                                 f"</div>")
                if row['team'] == 'Los Angeles Valiant':
                    with open(f'src/static/arrowblue.png', 'rb') as f:
                        arrow = base64.b64encode(f.read()).decode()
                else:
                    with open(f'src/static/arrowred.png', 'rb') as f:
                        arrow = base64.b64encode(f.read()).decode()
                html_content += f"<img src='data:image/png;base64,{arrow}' width='50' height='50'>"

                with open(f'src/static/{row["hero_img"]}.png', 'rb') as f:
                    hero_img = base64.b64encode(f.read()).decode()
                html_content += (f"<div style='display: flex; flex-direction: column; align-items: center;'>"
                                 f"<p style='margin: 0;'>{row['player']}</p>"
                                 f"<img src='data:image/png;base64,{hero_img}' width='50' height='50'>"
                                 f"<p style='font-style: italic;'>{row['hero']}</p>"
                                 f"</div>")
                html_content += "</div>"
            html_content += """
                </div>
            </div>
            """
            st.markdown(html_content, unsafe_allow_html=True)
except AttributeError as e:
    st.error(e)
