# AUTOGENERATED! DO NOT EDIT! File to edit: owl.ipynb.

# %% auto 0
__all__ = ['map_stats', 'df', 'get_match_analysis_heroes_played', 'get_match_analysis_all_stats',
           'get_match_analysis_heroes_stats', 'get_team_profile', 'get_heroes_stat', 'get_players_stat',
           'get_teams_leaderboard', 'get_heroes_stat_by_player', 'get_players_stat_by_team', 'get_team_scores',
           'get_switches']

# %% owl.ipynb 0
import dateutil.parser as dparser
import pandas as pd
from streamlit_jupyter import StreamlitPatcher

# %% owl.ipynb 2
import os

project_name = 'Overgraph'
path = os.getcwd().split(project_name)[0] + project_name
owl_path = f'{path}/src/datas/owl'

# %% owl.ipynb 3
datas = {
    # https://drive.google.com/file/d/1tPx0GVfdcdJUEl57ytA_uJtArKszI4vJ/view?usp=sharing
    # Google Docs
    # match_map_stats.csv
    'match_map_stats.csv': '1tPx0GVfdcdJUEl57ytA_uJtArKszI4vJ',
    # https://drive.google.com/file/d/1Gi0mbtmjOpcGeEBYjb9iAQiodIxd9cw_/view?usp=sharing
    # Google Docs
    # phs_2018_playoffs.csv
    'phs_2018_playoffs.csv': '1Gi0mbtmjOpcGeEBYjb9iAQiodIxd9cw_',
    # https://drive.google.com/file/d/1SfBAigf9vclOCyHYP2-uyp24J5mbdLN7/view?usp=sharing
    # Google Docs
    # phs_2018_stage_1.csv
    'phs_2018_stage_1.csv': '1SfBAigf9vclOCyHYP2-uyp24J5mbdLN7',
    # https://drive.google.com/file/d/1PUQKvE37wp14NII8FXqsTigTlSOmYtg-/view?usp=sharing
    # Google Docs
    # phs_2018_stage_2.csv
    'phs_2018_stage_2.csv': '1PUQKvE37wp14NII8FXqsTigTlSOmYtg-',
    # https://drive.google.com/file/d/1HhPL5MODUIkAABjgBOkIZfSuC7g4gKaG/view?usp=sharing
    # Google Docs
    # phs_2018_stage_3.csv
    'phs_2018_stage_3.csv': '1HhPL5MODUIkAABjgBOkIZfSuC7g4gKaG',
    # https://drive.google.com/file/d/1xhUj33D7kkZsEMU6UaORBAFs3jSDrI17/view?usp=sharing
    # Google Docs
    # phs_2018_stage_4.csv
    'phs_2018_stage_4.csv': '1xhUj33D7kkZsEMU6UaORBAFs3jSDrI17',
    # https://drive.google.com/file/d/13Knx8WlSemwDNYXd1YT0mYpljjHk-R4Y/view?usp=sharing
    # Google Docs
    # phs_2019_playoffs.csv
    'phs_2019_playoffs.csv': '13Knx8WlSemwDNYXd1YT0mYpljjHk-R4Y',
    # https://drive.google.com/file/d/1dCGQsAvS9xaGIrEhHhjf9NDVTL2hk2qP/view?usp=sharing
    # Google Docs
    # phs_2019_stage_1.csv
    'phs_2019_stage_1.csv': '1dCGQsAvS9xaGIrEhHhjf9NDVTL2hk2qP',
    # https://drive.google.com/file/d/1yavjUuNO_O7fxT9PGZS8AyQpau_eZpWj/view?usp=sharing
    # Google Docs
    # phs_2019_stage_2.csv
    'phs_2019_stage_2.csv': '1yavjUuNO_O7fxT9PGZS8AyQpau_eZpWj',
    # https://drive.google.com/file/d/1WS7btQ8HC_t_t9OAp4UCQd5O1cdGsvVA/view?usp=sharing
    # Google Docs
    # phs_2019_stage_3.csv
    'phs_2019_stage_3.csv': '1WS7btQ8HC_t_t9OAp4UCQd5O1cdGsvVA',
    # https://drive.google.com/file/d/1fWNKo0HfWM2CQzi-6WbUK1duvBd0NQiN/view?usp=sharing
    # Google Docs
    # phs_2019_stage_4.csv
    'phs_2019_stage_4.csv': '1fWNKo0HfWM2CQzi-6WbUK1duvBd0NQiN',
    # https://drive.google.com/file/d/1z7_MiS63noOB26Kxtbf5mwbVzTUPv1DG/view?usp=sharing
    # Google Docs
    # phs_2020_1.csv
    'phs_2020_1.csv': '1z7_MiS63noOB26Kxtbf5mwbVzTUPv1DG',
    # https://drive.google.com/file/d/1ZWAvP5eDs2EDYiuuZLcBWRI8PgY2aiSD/view?usp=sharing
    # Google Docs
    # phs_2020_2.csv
    'phs_2020_2.csv': '1ZWAvP5eDs2EDYiuuZLcBWRI8PgY2aiSD',
    # https://drive.google.com/file/d/1SJ5T4_8YyE-fv8flntKoboXToEupP1qE/view?usp=sharing
    # Google Docs
    # phs_2021_1.csv
    'phs_2021_1.csv': '1SJ5T4_8YyE-fv8flntKoboXToEupP1qE',
    # https://drive.google.com/file/d/1QN5kH1ZwPUwcxjH_XqB2OadfL4qB6IFX/view?usp=sharing
    # Google Docs
    # phs_2022.csv
    'phs_2022.csv': '1QN5kH1ZwPUwcxjH_XqB2OadfL4qB6IFX',
    # https://drive.google.com/file/d/1fKsztKPxxDbBdmLLH0WCV_GUsFcJhBph/view?usp=sharing
    # Google Docs
    # phs_2023.csv
    'phs_2023.csv': '1fKsztKPxxDbBdmLLH0WCV_GUsFcJhBph',
    # https://drive.google.com/file/d/1TicwMNWetiVQy6doystaIp0zjL8eLfR4/view?usp=sharing
    # Google Docs
    # switch.csv
    'switch.csv': '1TicwMNWetiVQy6doystaIp0zjL8eLfR4'
}

url = 'https://drive.google.com/uc?export=download&id=%s'

# %% owl.ipynb 5
# map_stats = pd.read_csv(f'{owl_path}/match_map_stats.csv')
map_stats = pd.read_csv(url % datas['match_map_stats.csv'])

# %% owl.ipynb 7
# df_2018_s1 = pd.read_csv(f'{owl_path}/phs_2018_stage_1.csv')
df_2018_s1 = pd.read_csv(url % datas['phs_2018_stage_1.csv'])

# %% owl.ipynb 10
# df_2018_s2 = pd.read_csv(f'{owl_path}/phs_2018_stage_2.csv')
df_2018_s2 = pd.read_csv(url % datas['phs_2018_stage_2.csv'])

# %% owl.ipynb 13
# df_2018_s3 = pd.read_csv(f'{owl_path}/phs_2018_stage_3.csv')
df_2018_s3 = pd.read_csv(url % datas['phs_2018_stage_3.csv'])

# %% owl.ipynb 16
# df_2018_s4 = pd.read_csv(f'{owl_path}/phs_2018_stage_4.csv')
df_2018_s4 = pd.read_csv(url % datas['phs_2018_stage_4.csv'])

# %% owl.ipynb 19
# df_2018_po = pd.read_csv(f'{owl_path}/phs_2018_playoffs.csv')
df_2018_po = pd.read_csv(url % datas['phs_2018_playoffs.csv'])

# %% owl.ipynb 22
# df_2019_s1 = pd.read_csv(f'{owl_path}/phs_2019_stage_1.csv')
df_2019_s1 = pd.read_csv(url % datas['phs_2019_stage_1.csv'])

# %% owl.ipynb 25
# df_2019_s2 = pd.read_csv(f'{owl_path}/phs_2019_stage_2.csv')
df_2019_s2 = pd.read_csv(url % datas['phs_2019_stage_2.csv'])

# %% owl.ipynb 28
# df_2019_s3 = pd.read_csv(f'{owl_path}/phs_2019_stage_3.csv')
df_2019_s3 = pd.read_csv(url % datas['phs_2019_stage_3.csv'])

# %% owl.ipynb 31
# df_2019_s4 = pd.read_csv(f'{owl_path}/phs_2019_stage_4.csv')
df_2019_s4 = pd.read_csv(url % datas['phs_2019_stage_4.csv'])

# %% owl.ipynb 34
# df_2019_po = pd.read_csv(f'{owl_path}/phs_2019_playoffs.csv')
df_2019_po = pd.read_csv(url % datas['phs_2019_playoffs.csv'])

# %% owl.ipynb 37
# df_2020_s1 = pd.read_csv(f'{owl_path}/phs_2020_1.csv')
df_2020_s1 = pd.read_csv(url % datas['phs_2020_1.csv'])

# %% owl.ipynb 40
# df_2020_s2 = pd.read_csv(f'{owl_path}/phs_2020_2.csv')
df_2020_s2 = pd.read_csv(url % datas['phs_2020_2.csv'])

# %% owl.ipynb 43
# df_2021 = pd.read_csv(f'{owl_path}/phs_2021_1.csv')
df_2021 = pd.read_csv(url % datas['phs_2021_1.csv'])

# %% owl.ipynb 46
# df_2022 = pd.read_csv(f'{owl_path}/phs_2022.csv')
df_2022 = pd.read_csv(url % datas['phs_2022.csv'])

# %% owl.ipynb 49
# df_2023 = pd.read_csv(f'{owl_path}/phs_2023.csv')
df_2023 = pd.read_csv(url % datas['phs_2023.csv'])

# %% owl.ipynb 52
# df_switch = pd.read_csv(f'{owl_path}/switch.csv')
df_switch = pd.read_csv(url % datas['switch.csv'])

# %% owl.ipynb 54
# merge every dataframes in one
df = pd.concat(
    [df_2018_s1, df_2018_s2, df_2018_s3, df_2018_s4, df_2018_po, df_2019_s1, df_2019_s2, df_2019_s3, df_2019_s4,
     df_2019_po, df_2020_s1, df_2020_s2, df_2021, df_2022, df_2023])

# %% owl.ipynb 57
df.replace({'hero': 'McCree'}, 'Cassidy', inplace=True)
df.replace({'hero': 'Lucio'}, 'Lúcio', inplace=True)
df.replace({'hero': 'Torbjorn'}, 'Torbjörn', inplace=True)
df = df[df['map_type'].str.lower() != 'UNKNOWN'.lower()]
df.replace({'team': 'Paris Eternal'}, 'Vegas Eternal', inplace=True)
df.replace({'team': 'Philadelphia Fusion'}, 'Seoul Infernal', inplace=True)
# todo: rework this part with 'start_time' year extraction and place it in 'stage'
stage_2018 = ['Overwatch League - Stage 1', 'Overwatch League - Stage 2', 'Overwatch League - Stage 3',
              'Overwatch League - Stage 4', 'Overwatch League - Stage 1 - Title Matches',
              'Overwatch League - Stage 2 Title Matches',
              'Overwatch League - Stage 3 Title Matches', 'Overwatch League - Stage 4 Title Matches',
              'Overwatch League Inaugural Season Championship']
stage_2019 = ['Overwatch League Stage 1', 'Overwatch League Stage 2', 'Overwatch League Stage 3',
              'Overwatch League Stage 4', 'Overwatch League Stage 1 Title Matches',
              'Overwatch League Stage 2 Title Matches', 'Overwatch League Stage 3 Title Matches',
              'Overwatch League Stage 4 Title Matches', 'Overwatch League 2019 Post-Season']
stage_2020 = ['OWL 2020 Regular Season', 'OWL APAC All-Stars', 'OWL North America All-Stars']
stage_2021 = ['OWL 2021']
stage_2022 = ['Kickoff Clash: Qualifiers', 'Kickoff Clash: Tournament', 'Midseason Madness: Qualifiers',
              'Midseason Madness: Tournament', 'Summer Showdown: Qualifiers', 'Summer Showdown: Tournament',
              'Countdown Cup: Qualifiers', 'Countdown Cup: Tournament', 'Postseason']
stage_2023 = ['Pro-Am', 'Spring Qualifiers', 'Spring Knockouts', 'Midseason Madness', 'Summer Showdown',
              'Countdown Cup', 'Postseason']

for stage in stage_2018:
    df.replace({'stage': stage}, f'2018 : {stage}', inplace=True)
for stage in stage_2019:
    df.replace({'stage': stage}, f'2019 : {stage}', inplace=True)
for stage in stage_2020:
    df.replace({'stage': stage}, f'2020 : {stage}', inplace=True)
for stage in stage_2021:
    df.replace({'stage': stage}, f'2021 : {stage}', inplace=True)
for stage in stage_2022:
    df.replace({'stage': stage}, f'2022 : {stage}', inplace=True)
for stage in stage_2023:
    df.replace({'stage': stage}, f'2023 : {stage}', inplace=True)

dps_list = ['Ashe', 'Bastion', 'Cassidy', 'Echo', 'Genji', 'Hanzo', 'Junkrat', 'Mei', 'Pharah',
            'Reaper', 'Sojourn', 'Soldier: 76', 'Sombra', 'Symmetra', 'Torbjörn', 'Tracer', 'Widowmaker']
tank_list = ['D.Va', 'Doomfist', 'Junker Queen', 'Orisa', 'Ramattra', 'Reinhardt', 'Roadhog', 'Sigma', 'Winston',
             'Wrecking Ball', 'Zarya']
support_list = ['Ana', 'Baptiste', 'Brigitte', 'Illari', 'Kiriko', 'Lifeweaver', 'Lúcio', 'Mercy', 'Moira', 'Zenyatta']

# Add a new column 'role' to the dataframe and fill it with the role of the hero
df['role'] = df['hero']
df.replace({'role': dps_list}, 'DPS', inplace=True)
df.replace({'role': tank_list}, 'Tank', inplace=True)
df.replace({'role': support_list}, 'Support', inplace=True)
df.replace({'role': 'All Heroes'}, 'All', inplace=True)


# !!!! to save execution time, match_map_stats.csv cleaned version has been saved
# !!!! if it's your first run, you must uncomment the following part: 
# for col in ['match_winner', 'map_winner', 'map_loser', 'attacker', 'defender', 'team_one_name', 'team_two_name']:
#     map_stats.replace({col: 'Paris Eternal'}, 'Vegas Eternal', inplace=True)
#     map_stats.replace({col: 'Philadelphia Fusion'}, 'Seoul Infernal', inplace=True)
# map_stats['round_start_time'] = map_stats['round_start_time'].str.replace(' UTC', '')
# map_stats['round_end_time'] = map_stats['round_end_time'].str.replace(' UTC', '')
# map_stats['round_start_time'] = map_stats['round_start_time'].apply(lambda x: dparser.parse(x, fuzzy=True))
# map_stats['round_end_time'] = map_stats['round_end_time'].apply(lambda x: dparser.parse(x, fuzzy=True))
# map_stats.to_csv(f'{owl_path}/match_map_stats.csv', index=False)

# %% owl.ipynb 63
def get_match_analysis_heroes_played(stage: str, match: int, map: str, all: bool) -> pd.DataFrame:
    # Filter the dataframe based on the stage and match_id
    match_data = df[(df['stage'] == stage) & (df['match_id'] == match) & (df['map'] == map)]

    # for each unique player, get unique 'hero' and 'stat' == 'Time Played' and 'stat_amount'
    result = pd.DataFrame(columns=['Team', 'Player', 'Hero', 'Time Played'])
    players = match_data['player'].unique()
    for player in players:
        player_data = match_data[match_data['player'] == player]
        player_data = player_data[player_data['stat'] == 'Time Played']

        # Filter the data based on the 'all' parameter
        if all:
            player_data = player_data[player_data['hero'] == 'All Heroes']
        else:
            player_data = player_data[player_data['hero'] != 'All Heroes']

        player_data = player_data[['team', 'player', 'hero', 'stat_amount']]
        player_data.columns = ['Team', 'Player', 'Hero', 'Time Played']
        result = pd.concat([result, player_data], ignore_index=True, sort=False)

    return result

# %% owl.ipynb 65
def get_match_analysis_all_stats(stage: str, match: int, map: str) -> pd.DataFrame:
    # Filter the dataframe based on the stage and match_id
    match_data = df[(df['stage'] == stage) & (df['match_id'] == match) & (df['map'] == map)]

    # List of common stats to calculate
    stats_list = [
        'All Damage Done', 'Assists', 'Eliminations', 'Eliminations per Life', 'Deaths', 'Final Blows',
        'Hero Damage Done', 'Time Played', 'Ultimates Used', 'Objective Kills', 'Weapon Accuracy',
        'Average Time Alive', 'Damage Blocked', 'Healing Done', 'Players Saved']

    # get all these stat for the player : 'Team', 'Player', 'Hero', 'Role', 'Stat', 'Stat Amount'
    result = pd.DataFrame(columns=['Team', 'Player', 'Hero', 'Role', 'Stat', 'Stat Amount'])

    for stat in stats_list:
        player_data = match_data[match_data['stat'] == stat]
        # Filter the data based on the 'all' parameter
        player_data = player_data[player_data['hero'] == 'All Heroes']
        player_data = player_data[['team', 'player', 'hero', 'role', 'stat', 'stat_amount']]
        player_data.columns = ['Team', 'Player', 'Hero', 'Role', 'Stat', 'Stat Amount']
        result = pd.concat([result, player_data], ignore_index=True, sort=False)

    return result

# %% owl.ipynb 67
def get_match_analysis_heroes_stats(stage: str, match: int, map: str, player: str, all: bool,
                                    hero: str = None) -> pd.DataFrame:
    # Filter the dataframe based on the stage and match_id
    match_data = df[(df['stage'] == stage) & (df['match_id'] == match) & (df['map'] == map)]

    # List of common stats to calculate
    stats_list = ['All Damage Done', 'Assists', 'Eliminations', 'Eliminations per Life', 'Deaths', 'Final Blows',
                  'Hero Damage Done', 'Time Played', 'Ultimates Used', 'Objective Kills', 'Weapon Accuracy',
                  'Average Time Alive', 'Damage Blocked', 'Healing Done', 'Players Saved']

    tank_stats = ['Damage Blocked']
    support_stats = ['Healing Done', 'Players Saved']

    # get all these stat for the player : 'Team', 'Player', 'Hero', 'Role', 'Stat', 'Stat Amount' 
    result = pd.DataFrame(columns=['Team', 'Player', 'Hero', 'Role', 'Stat', 'Stat Amount'])

    for stat in stats_list:
        player_data = match_data[(match_data['player'] == player) & (match_data['stat'] == stat)]
        # Filter the data based on the 'all' parameter
        if all:
            player_data = player_data[player_data['hero'] == 'All Heroes']
        else:
            player_data = player_data[player_data['hero'] != 'All Heroes']

        # Filter the data based on the 'hero' parameter
        if hero is not None:
            player_data = player_data[player_data['hero'] == hero]

        player_data = player_data[['team', 'player', 'hero', 'role', 'stat', 'stat_amount']]

        player_data.columns = ['Team', 'Player', 'Hero', 'Role', 'Stat', 'Stat Amount']
        result = pd.concat([result, player_data], ignore_index=True, sort=False)

    return result

# %% owl.ipynb 69
def get_team_profile(team: str, stat: str, stage: str = None) -> pd.DataFrame:
    """
    This function generates a profile for a given team, based on a specific statistic and optionally for a specific stage.
    
    Parameters:
    team (str): The name of the team.
    stat (str): The statistic to consider.
    stage (str, optional): The stage to consider. If None, all stages are considered.
    
    Returns:
    pd.DataFrame: A DataFrame containing the team profile.
    """

    # Filter the DataFrame based on the team, stat, and hero
    result = df[df['team'] == team]
    result = result[result['stat'] == stat]
    result = result[result['hero'] == 'All Heroes']

    # If a stage is specified, filter the DataFrame based on the stage
    if stage:
        print('stage filter')
        result = result[result['stage'] == stage]

    # Calculate the total stat amount for each match
    stat_result = result.groupby(['match_id'])['stat_amount'].sum()

    # Calculate the total stat amount for each match and start time
    total_stat_amount = result.groupby(['match_id', 'start_time'])['stat_amount'].sum()

    # Calculate the number of start times for each match
    number_of_start_time_per_match = total_stat_amount.groupby(['match_id']).count()

    # Calculate the average stat amount
    avg_stat = total_stat_amount.groupby(['match_id']).sum() / number_of_start_time_per_match

    # Add the total and average stat amounts to the DataFrame
    result['stat_match_total'] = result['match_id'].apply(lambda x: stat_result[x])
    result['avg_stat'] = result['match_id'].apply(lambda x: avg_stat[x])

    # Replace the stat amount with the total stat amount
    result['stat_amount'] = result['stat_match_total']
    result = result.drop(columns=['stat_match_total'])

    # Merge the DataFrame with the map stats DataFrame
    result = result.reset_index().merge(
        map_stats[['match_id', 'match_winner', 'team_one_name', 'team_two_name']], on='match_id')

    # Add the opponent team to the DataFrame
    result['opponent'] = result['team_one_name']
    result['opponent'] = result['opponent'].where(result['team_one_name'] != team, result['team_two_name'])
    result = result.drop(columns=['team_one_name', 'team_two_name'])

    # Remove duplicate matches
    result = result.drop_duplicates(subset='match_id')
    result = result.set_index('match_id')

    # Convert the start time to a datetime object and sort the DataFrame by start time
    result['start_time'] = result['start_time'].str.replace(' UTC', '')
    result['start_time'] = result['start_time'].apply(lambda x: dparser.parse(x, fuzzy=True))
    result = result.sort_values(by='start_time')

    # Calculate the win rate for each match
    result['winrate'] = 0
    win = 0
    loss = 0
    for match in result.index:
        if result.loc[match, 'match_winner'] == team:
            win += 1
        else:
            loss += 1
        result.loc[match, 'winrate'] = win / (win + loss) * 100

    # Remove unnecessary columns
    result = result.drop(columns=['index', 'stat', 'map_type', 'map', 'player', 'hero', 'team'])

    # Rename the columns
    result.rename(
        columns={'start_time': 'Start Time', 'stat_amount': stat, 'match_winner': 'Match Winner', 'winrate': 'Winrate',
                 'opponent': 'Opponent', 'stage': 'Stage', 'avg_stat': f'Avg {stat}'},
        inplace=True)

    result.index.name = 'Match ID'

    return result

# %% owl.ipynb 71
def get_heroes_stat(stat: str) -> pd.DataFrame:
    """
    This function calculates the total amount of a specific statistic for each hero in the dataset.

    Parameters:
    stat (str): The statistic to consider.

    Returns:
    pd.DataFrame: A DataFrame containing the total amount of the statistic for each hero, sorted in descending order.
    """
    # Filter the DataFrame based on the statistic
    result = df[df['stat'] == stat]

    # # Group by hero and sum the statistic amounts
    # result = result.groupby('hero')['stat_amount'].sum().sort_values(ascending=False)
    # 
    # # Set the name of the Series and its index
    # result.name = stat
    # result.index.name = 'Hero'
    # 
    # # Convert the Series to a DataFrame
    # result = result.to_frame()

    # get the sum of the stat for each hero : 'Hero', 'Role', 'Stat', 'Stat Amount'
    result = result.groupby(['hero', 'role', 'stat'])['stat_amount'].sum().reset_index()
    result = result[result['hero'] != 'All Heroes']
    result = result.sort_values(by='stat_amount', ascending=False)
    result = result.set_index('hero')

    # Rename the columns
    result.rename(columns={'role': 'Role', 'stat': 'Stat', 'stat_amount': stat}, inplace=True)
    result.index.name = 'Hero'

    return result


# %% owl.ipynb 73
def get_players_stat(stat: str) -> pd.DataFrame:
    """
    This function calculates the total amount of a specific statistic for each player in the dataset.

    Parameters:
    stat (str): The statistic to consider.

    Returns:
    pd.DataFrame: A DataFrame containing the total amount of the statistic for each player, sorted in descending order.
    """
    # Filter the DataFrame based on the statistic
    result = df[df['stat'] == stat]

    # Group by player and sum the statistic amounts
    result = result.groupby('player')['stat_amount'].sum().sort_values(ascending=False)

    # Set the name of the Series and its index
    result.name = stat
    result.index.name = 'Player'

    # Convert the Series to a DataFrame
    result = result.to_frame()

    return result

# %% owl.ipynb 75
def avg_stats_per_game(stat: str, player: str) -> pd.DataFrame:
    """
    This function calculates the average amount of a specific statistic per game for a specific player.

    Parameters:
    stat (str): The statistic to consider.
    player (str): The player to consider.

    Returns:
    pd.DataFrame: A DataFrame containing the average amount of the statistic per game for each hero the player has played, 
    the number of games played with each hero, sorted in descending order of the average statistic.
    """
    # Filter the DataFrame based on the statistic and player
    player_data = df[(df['stat'] == stat) & (df['player'] == player)]
    results = pd.DataFrame(columns=['Hero', 'Stat', 'Avg per game'])

    # Filter the DataFrame based on the statistic
    stat_data = player_data[player_data['stat'] == stat]

    # Calculate the average statistic amount per game for each hero
    avg_per_game = stat_data.groupby(['hero'])['stat_amount'].mean().reset_index()
    avg_per_game.columns = ['Hero', 'Avg per game']

    # Calculate the number of games played with each hero
    avg_per_game['Number of game'] = stat_data.groupby(['hero'])['stat_amount'].count().reset_index()['stat_amount']

    # Concatenate the results
    results = pd.concat([results, avg_per_game], ignore_index=True, sort=False)

    return results[['Hero', 'Avg per game', 'Number of game']]

# %% owl.ipynb 76
def get_teams_leaderboard(stage=None):
    """
    This function calculates the win rate for each team in the dataset, optionally for a specific stage.

    Parameters:
    stage (str, optional): The stage to consider. If None, all stages are considered.

    Returns:
    pd.DataFrame: A DataFrame containing the win rate for each team, sorted in descending order.
    """

    # Get a list of unique teams
    teams = df['team'].unique()

    # Initialize an empty list to store the win rates
    winrates = []

    # Calculate the win rate for each team
    for team in teams:
        # Get all matches involving the team
        team_matches = df[(df['team'] == team)]

        # If a stage is specified, filter the matches by stage
        if stage is not None:
            # Keep only rows where 'stage' is equal to the specified stage
            team_matches = team_matches[team_matches['stage'] == stage]

        # If team_matches is empty, continue to the next team
        if team_matches.empty:
            continue

        # Get match_ids for the filtered matches
        match_ids = team_matches['match_id'].unique()

        # Filter map_stats by these match_ids
        team_map_stats = map_stats[map_stats['match_id'].isin(match_ids)]

        # Count the number of matches won by the team
        wins = len(team_map_stats[team_map_stats['match_winner'] == team])

        # Calculate the total number of matches played by the team
        total_matches = len(team_map_stats)

        # Calculate the win rate
        if total_matches > 0:
            winrate = (wins / total_matches) * 100
        else:
            winrate = 0

        # Append the team and its win rate to the list
        winrates.append((team, winrate))

    # Convert the list to a DataFrame
    winrates_df = pd.DataFrame(winrates, columns=['Team', 'Winrate'])

    # Sort the DataFrame by win rate in descending order
    winrates_df = winrates_df.sort_values('Winrate', ascending=False)

    return winrates_df

# %% owl.ipynb 78
def get_heroes_stat_by_player(stat: str, player: str) -> pd.Series:
    """
    This function calculates the total amount of a specific statistic for each hero played by a specific player.

    Parameters:
    stat (str): The statistic to consider.
    player (str): The player to consider.

    Returns:
    pd.Series: A Series containing the total amount of the statistic for each hero played by the player, 
    sorted in descending order, and the average statistic per game.
    """
    # Filter the DataFrame based on the statistic and player
    result = df[(df['stat'] == stat) & (df['player'] == player)].groupby('hero')['stat_amount'].sum().sort_values(
        ascending=False)
    result.name = stat
    result.index.name = 'Hero'

    # Calculate the average statistic per game
    stat_avg = avg_stats_per_game(stat, player)

    # Merge the total and average statistics
    result = result.reset_index().merge(stat_avg, on='Hero', how='left')

    # Reset the index
    result = result.set_index('Hero')

    return result

# %% owl.ipynb 81
def get_players_stat_by_team(stat: str, team: str) -> pd.DataFrame:
    """
    This function calculates the total amount of a specific statistic for each player in a specific team.

    Parameters:
    stat (str): The statistic to consider.
    team (str): The team to consider.

    Returns:
    pd.DataFrame: A DataFrame containing the total amount of the statistic for each player in the team, sorted in descending order.
    """
    # Filter the DataFrame based on the statistic and team
    result = df[(df['stat'] == stat) & (df['team'] == team)].groupby('player')['stat_amount'].sum().sort_values(
        ascending=False)

    # Set the name of the Series and its index
    result.name = stat
    result.index.name = 'Player'
    result = result.to_frame()

    return result

# %% owl.ipynb 83
def get_team_scores(team: str, map_type: str = None, map_name: str = None) -> pd.DataFrame:
    """
    This function generates a DataFrame containing the scores of a specific team, optionally filtered by map type and map name.

    Parameters:
    team (str): The name of the team.
    map_type (str, optional): The type of the map. If None, all map types are considered.
    map_name (str, optional): The name of the map. If None, all maps are considered.

    Returns:
    pd.DataFrame: A DataFrame containing the scores of the team, including the number of wins, losses, and the win rate.
    """
    # Stock every unique game from team (each game as a unique 'match_id'), team name is stocked in 'team_one_name' or 'team_two_name'
    team_games = map_stats[(map_stats['team_one_name'] == team) | (map_stats['team_two_name'] == team)]
    if map_type:  # only 1 row per game
        # Add column 'map_type' from dataframe 'df'
        team_games = team_games.merge(df[['match_id', 'map_type']], on='match_id')
        team_games = team_games[team_games['map_type'].str.lower() == map_type.lower()]
        if map_name:  # only 1 row per game
            team_games = team_games[team_games['map_name'].str.lower() == map_name.lower()]
        # Get one row per map
        team_games = team_games.drop_duplicates(subset='round_start_time')
        # Do not keep twice same game_number per match_id
        df_grp = team_games.groupby(['match_id', 'game_number'])
        team_games = df_grp.first().reset_index()
    else:  # only 1 row per match
        # Get one row per match
        team_games = team_games.drop_duplicates(subset='match_id')

    # Get teams list
    opponents = team_games[['team_one_name', 'team_two_name']]
    # Remove team input from opponents list
    opponents = opponents[opponents != team]
    # Regroup in one column and remove duplicates
    opponents = opponents.stack().reset_index(drop=True).drop_duplicates()

    results = pd.DataFrame(columns=['team', 'opponent', 'win', 'loss', 'winrate', 'map_type', 'only_matches'])

    for opponent in opponents:
        matches = team_games[((team_games['team_one_name'] == team) &
                              (team_games['team_two_name'] == opponent)) | (
                                     (team_games['team_one_name'] == opponent) & (team_games['team_two_name'] == team))]

        if map_type:
            wins = matches['map_winner'] == team
        else:
            wins = matches['match_winner'] == team

        total_matches = matches.shape[0]
        if total_matches == 0:
            continue
        wins = wins.sum()
        losses = len(matches) - wins
        winrate = wins / total_matches

        row = pd.DataFrame(
            {'team': team, 'opponent': opponent, 'total_matches': total_matches, 'win': wins, 'loss': losses,
             'winrate': winrate * 100, 'map_type': map_type,
             'only_matches': not map_type, 'map_name': map_name}, index=[0])
        results = pd.concat([results, row])

    # Rename columns
    results.rename(columns={'team': 'Team', 'opponent': 'Opponent', 'total_matches': 'Total Matches', 'win': 'Win',
                            'loss': 'Loss', 'winrate': 'Winrate', 'map_type': 'Map Type',
                            'only_matches': 'Only Matches', 'map_name': 'Map Name'},
                   inplace=True)

    # Reorder columns
    results = results[
        ['Team', 'Opponent', 'Total Matches', 'Win', 'Loss', 'Winrate', 'Map Type', 'Map Name', 'Only Matches']]
    if not map_type:
        results = results.drop(columns='Map Type')
    if not map_name:
        results = results.drop(columns='Map Name')

    results = results.set_index('Team')
    return results

# %% owl.ipynb 84
def get_switches() -> pd.DataFrame:
    """
    This function returns a DataFrame containing the switches made by players during matches.
    """
    result = df_switch
    return result
