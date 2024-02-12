import os

import altair as alt
import streamlit as st
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


try:
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    map_stats = st.session_state.map_stats
    df = st.session_state.df
    get_team_profile = st.session_state.get_team_profile

    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()

    with df_tab:
        display_page_infos()
        # create a dropdown list with every unique 'stat'
        team = st.selectbox('Select a team', teams_list)
        stat = st.selectbox('Select a stat', stats_list)
        try:
            st.write(get_team_profile(team, stat))
        except KeyError:
            st.error('No data available for this team and this map type')
    with viz_tab:
        display_page_infos()
        st.subheader(
            f'todo')
        try:
            # todo: add a date picker to select the time range
            date_range = st.date_input('Select a date range', [df['Start Time'].min(), df['Start Time'].max()])
            chart_datas = get_team_profile(team, stat)
            # display a line shart sharing the x axis with y1 : the stat value and y2 : the winrate
            fig, ax1 = plt.subplots()
            ax2 = ax1.twinx()
            ax1.plot(chart_datas['Start Time'], chart_datas[stat], 'g-')
            ax2.plot(chart_datas['Start Time'], chart_datas['Winrate'], 'b-')
            ax1.set_xlabel('Date')
            ax1.set_ylabel(stat, color='g')
            ax2.set_ylabel('Winrate', color='b')
            st.pyplot(fig)

        except KeyError:
            st.error('No data available for this team and this map type')
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
