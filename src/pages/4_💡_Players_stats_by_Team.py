import os

import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Overgraph - Players stats by Team",
    page_icon="./src/img/overgraph-logo.png"
)


def display_page_infos():
    st.subheader('Get specific stats for a team')
    st.markdown("""
                    This page provides a comprehensive overview of **each team's performance based on a specific stat in the Overwatch League**.
                    The records indicate the full list of players in the team and the corresponding stat value for each player.
                    These insights could be pivotal in enhancing the team's strategies and performance.
                """)


try:
    df = st.session_state.df
    get_players_stat_by_team = st.session_state.get_players_stat_by_team

    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()

    display_page_infos()
    # create a dropdown list with every unique 'stat'
    team = st.selectbox('Select a team', teams_list)
    stat = st.selectbox('Select a stat', stats_list)
    # display the result
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    data = get_players_stat_by_team(stat, team)
    with df_tab:
        if data.empty:
            st.error('No data available for this team and this stat')
        else:
            st.write(data)
    with viz_tab:
        if data.empty:
            st.error('No data available for this team and this stat')
        else:
            st.subheader(f'{team}\'s {stat} stats')
            data[stat] = data[stat].round(2)

            formatted_stat = data[stat].apply(lambda x: "{:,}".format(x))
            fig = px.bar(data, x=stat, y=data.index, labels={'x': stat, 'y': 'Player'}, color=stat,
                         color_continuous_scale='reds')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            fig.update_traces(textposition='inside', text=formatted_stat, textfont_size=100, textfont_color='Black',
                              textangle=0)

            st.plotly_chart(fig)
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
