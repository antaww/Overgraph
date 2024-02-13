import os

import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Overgraph - Heroes stats by Player",
    page_icon="⚡",
)


def display_page_infos():
    st.subheader('Get specific stats for every hero of a player')
    st.markdown("""
                        The collected datas provide a comprehensive overview of **every player performances depending on a stat in the Overwatch League**. 
                        The records indicate the full players list and the corresponding stat value. 
                        Analyzing the players stats could help to understand the overall balance of the game and the meta.
                        """)


try:
    df = st.session_state.df
    get_heroes_stat_by_player = st.session_state.get_heroes_stat_by_player

    players_list = df['player'].unique()
    stats_list = df['stat'].unique()

    display_page_infos()
    player = st.selectbox('Select a player', players_list)
    stat = st.selectbox('Select a stat', stats_list)
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        st.write(get_heroes_stat_by_player(stat, player))
    with viz_tab:
        data = get_heroes_stat_by_player(stat, player)
        data = data[data.index != 'All Heroes']

        st.subheader(f'{player}\'s {stat} stats')

        total_stats = data[stat]
        total_stats = total_stats.round(2)
        formatted_stat = total_stats.apply(lambda x: "{:,}".format(x))
        fig = px.bar(data, x=stat, y=data.index, labels={'x': stat, 'y': 'Hero'}, color=stat,
                     color_continuous_scale='reds')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig.update_traces(textposition='inside', text=formatted_stat, textfont_size=100, textfont_color='Black', textangle=0)
        st.plotly_chart(fig)

        avg_stats = data[['Avg per game', 'Number of game']]
        avg_stats = avg_stats.sort_values(by='Avg per game', ascending=True)
        avg_stats['Avg per game'] = avg_stats['Avg per game'].round(2)
        formatted_avg_stat = avg_stats['Avg per game'].apply(lambda x: "{:,}".format(x))
        fig_avg = px.bar(avg_stats, x='Avg per game', y=avg_stats.index, labels={'y': 'Hero', 'x': 'Avg per game'},
                    color='Number of game', color_continuous_scale='reds')
        fig_avg.update_layout(xaxis={'categoryorder': 'total ascending'})
        fig_avg.update_traces(textposition='inside', text=formatted_avg_stat, textfont_size=100, textfont_color='Black', textangle=0)
        st.plotly_chart(fig_avg)
        # st.bar_chart(avg_stats)
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
