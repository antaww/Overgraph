import os

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Overgraph - Team VS Teams", page_icon="⚔️", )


def display_page_infos():
    st.subheader('Get team scores against other teams')
    st.markdown("""
                    The collected datas provide a comprehensive overview of one **team's performances against its Overwatch League opponents**. 
                    The records indicate the total number of matches / rounds played, wins, losses and win percentage for each team matchup across multiple seasons. 
                    For a high level team coach, it is important to analyze the team's performance against other teams to understand their strengths and weaknesses. 
                    It could help inform strategic decision-making going forward. 
                    """)


def double_y_lines(dataframe: pd.DataFrame, title: str, x: str, y1: str, y2: str,
                   colory1: str, colory2: str, colormean: str, second_title_condition: bool = False,
                   second_title: str = None, mode: str = 'lines+markers') -> plt.Figure:
    # Create a subplot with two y-axes
    figure = make_subplots(specs=[[{"secondary_y": True}]])

    # Add the first trace to the plot for the primary y-axis
    figure.add_trace(go.Scatter(x=dataframe[x], y=dataframe[y1], name=y1, line=dict(color=colory1), mode=mode))

    # Add the second trace to the plot for the secondary y-axis
    figure.add_trace(go.Scatter(x=dataframe[x], y=dataframe[y2], name=y2, line=dict(color=colory2), mode=mode),
                     secondary_y=True)

    # Set the title of the plot based on the condition
    if second_title_condition:
        figure.update_layout(title=second_title)
    else:
        figure.update_layout(title=title)

    # Set the title for the x-axis
    figure.update_xaxes(title_text=x)

    # Set the title for the y-axes
    figure.update_yaxes(title_text=y1, secondary_y=False)
    figure.update_yaxes(title_text=y2, secondary_y=True)

    # Set the range for the x-axis to start on the first value date
    figure.update_xaxes(range=[dataframe[x].min(), dataframe[x].max()])

    # Calculate the mean of y1
    mean_y1 = dataframe[y1].mean()

    # Add a horizontal line at the mean of y1
    figure.add_trace(go.Scatter(x=[dataframe[x].min(), dataframe[x].max()], y=[mean_y1, mean_y1],
                                mode="lines", line=dict(color=colormean, dash='dash'), name=f'Mean of {y1}'))

    return figure


try:
    map_stats = st.session_state.map_stats
    df = st.session_state.df
    get_team_profile = st.session_state.get_team_profile

    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()
    stages_list = df['stage'].unique()

    display_page_infos()

    team = st.selectbox('Select a team', teams_list)
    stat = st.selectbox('Select a stat', stats_list)
    stage = st.selectbox('Select a stage (not required)', [''] + list(stages_list))

    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        try:
            st.write(get_team_profile(team, stat, stage))
        except KeyError:
            st.error('No data available for this team and this stage')
    with viz_tab:
        st.subheader(
            f'{team}\'s {stat} and winrate over time on {stage if stage else "all stages"}')
        try:
            chart_datas = get_team_profile(team, stat, stage)
            # todo: add mean line for the stat
            fig = double_y_lines(dataframe=chart_datas, title=f'{team}\'s {stat} and winrate over time on all stages',
                                 x='Start Time', y1=stat, y2='Winrate', colory1='red', colory2='blue',
                                 colormean='green',
                                 second_title_condition=stage,
                                 second_title=f'{team}\'s {stat} and winrate over time on {stage}',
                                 mode='lines+markers')

            fig2 = double_y_lines(dataframe=chart_datas,
                                  title=f'{team}\'s Avg {stat} and winrate over time on all stages',
                                  x='Start Time', y1=f'Avg {stat}', y2='Winrate', colory1='red', colory2='blue',
                                  colormean='green', second_title_condition=stage,
                                  second_title=f'{team}\'s Avg {stat} and winrate over time on {stage}',
                                  mode='lines+markers')
            st.plotly_chart(fig)
            st.plotly_chart(fig2)
        except KeyError:
            st.error('No data available for this team and this map type')
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
