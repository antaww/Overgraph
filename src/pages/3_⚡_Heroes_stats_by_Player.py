import os

import altair as alt
import streamlit as st

st.set_page_config(
    page_title="Overgraph - Heroes stats by Player",
    page_icon="⚡",
)

try:
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    df = st.session_state.df
    get_heroes_stat_by_player = st.session_state.get_heroes_stat_by_player

    players_list = df['player'].unique()
    stats_list = df['stat'].unique()

    with df_tab:
        st.subheader('Get specific stats for a player')
        player = st.selectbox('Select a player', players_list)
        stat = st.selectbox('Select a stat', stats_list)
        st.write(get_heroes_stat_by_player(stat, player))
    with viz_tab:
        data = get_heroes_stat_by_player(stat, player)
        data = data[data.index != 'All Heroes']

        st.subheader(f'{player}\'s {stat} stats')
        total_stats = data[stat]
        st.bar_chart(total_stats)
        avg_stats = data[['Avg per game', 'Number of game']]
        chart = alt.Chart(avg_stats.reset_index()).mark_bar().encode(
            x='Hero',
            y=alt.Y('Avg per game'),
            color=alt.Color('Number of game', scale=alt.Scale(scheme='orangered')),
            # https://vega.github.io/vega/docs/schemes/#reference
            tooltip=['Hero', 'Avg per game', 'Number of game'],
        ).properties(
            height=500
        )
        st.altair_chart(chart, use_container_width=True)
        # st.bar_chart(avg_stats)
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
