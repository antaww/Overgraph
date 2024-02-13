import os

import pandas as pd
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

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
                   second_title_condition: bool = False, second_title: str = None,
                   mode: str = 'lines+markers') -> plt.Figure:
    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.add_trace(px.line(dataframe, x='Start Time', y=stat).data[0])
    figure.add_trace(px.line(dataframe, x='Start Time', y='Winrate').data[0], secondary_y=True)
    # color lines
    figure.data[0].line.color = 'red'
    figure.data[1].line.color = 'blue'
    # add title
    if stage:
        figure.update_layout(title=f'{team}\'s {stat} and winrate over time on {stage}')
    else:
        figure.update_layout(title=f'{team}\'s {stat} and winrate over time on all stages')
    # add x axis title
    figure.update_xaxes(title_text='Date')
    # add y axis title
    figure.update_yaxes(title_text=stat, secondary_y=False)
    figure.update_yaxes(title_text='Winrate', secondary_y=True)
    # add point
    figure.update_traces(mode='lines+markers')
    # make x axis start on first value date
    figure.update_xaxes(range=[dataframe['Start Time'].min(), dataframe['Start Time'].max()])
    return figure


try:
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    map_stats = st.session_state.map_stats
    df = st.session_state.df
    get_team_profile = st.session_state.get_team_profile

    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()
    stages_list = df['stage'].unique()

    with df_tab:
        display_page_infos()
        # create a dropdown list with every unique 'stat'
        team = st.selectbox('Select a team', teams_list)
        stat = st.selectbox('Select a stat', stats_list)
        stage = st.selectbox('Select a stage (not required)', [''] + list(stages_list))
        try:
            st.write(get_team_profile(team, stat, stage))
        except KeyError:
            st.error('No data available for this team and this stage')
    with viz_tab:
        display_page_infos()
        st.subheader(
            f'todo')
        try:
            chart_datas = get_team_profile(team, stat, stage)
            # todo: add mean line for the stat
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(px.line(chart_datas, x='Start Time', y=stat).data[0])
            fig.add_trace(px.line(chart_datas, x='Start Time', y='Winrate').data[0], secondary_y=True)
            # color lines
            fig.data[0].line.color = 'red'
            fig.data[1].line.color = 'blue'
            # add title
            if stage:
                fig.update_layout(title=f'{team}\'s {stat} and winrate over time on {stage}')
            else:
                fig.update_layout(title=f'{team}\'s {stat} and winrate over time on all stages')
            # add x axis title
            fig.update_xaxes(title_text='Date')
            # add y axis title
            fig.update_yaxes(title_text=stat, secondary_y=False)
            fig.update_yaxes(title_text='Winrate', secondary_y=True)
            # add point
            fig.update_traces(mode='lines+markers')
            # make x axis start on first value date
            fig.update_xaxes(range=[chart_datas['Start Time'].min(), chart_datas['Start Time'].max()])
            # todo: fig = double_y_lines()

            # same thing but replace stat with Avg+stat
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])

            fig2.add_trace(px.line(chart_datas, x='Start Time', y=f'Avg {stat}').data[0])
            fig2.add_trace(px.line(chart_datas, x='Start Time', y='Winrate').data[0], secondary_y=True)

            fig2.data[0].line.color = 'red'
            fig2.data[1].line.color = 'blue'

            if stage:
                fig2.update_layout(title=f'{team}\'s Avg {stat} and winrate over time on {stage}')
            else:
                fig2.update_layout(title=f'{team}\'s Avg {stat} and winrate over time on all stages')

            fig2.update_xaxes(title_text='Date')
            fig2.update_yaxes(title_text=f'Avg {stat}', secondary_y=False)
            fig2.update_yaxes(title_text='Winrate', secondary_y=True)
            fig2.update_traces(mode='lines+markers')
            fig2.update_xaxes(range=[chart_datas['Start Time'].min(), chart_datas['Start Time'].max()])
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
