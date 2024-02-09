import os
import altair as alt
import streamlit as st

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
    get_team_scores = st.session_state.get_team_scores

    teams_list = df['team'].unique()
    map_types_list = df['map_type'].str.title().unique()

    with df_tab:
        display_page_infos()
        # create a dropdown list with every unique 'stat'
        team = st.selectbox('Select a team', teams_list)
        map_type = st.selectbox('Select a map (not required)', [''] + list(map_types_list))
        st.markdown('_**Only Matches** column means : if the score is based on the whole match or only the map_')
        # display the result
        try:
            st.write(get_team_scores(team, map_type))
        except KeyError:
            st.error('No data available for this team and this map type')
    with viz_tab:
        display_page_infos()
        st.subheader(
            f'Winrate of {team} against other teams on {map_type + ' maps' if map_type else "all types of matches"}')
        try:
            chart_datas = get_team_scores(team, map_type).set_index('Opponent')[['Winrate', 'Total Matches']]
            chart = alt.Chart(chart_datas.reset_index()).mark_bar().encode(
                x='Opponent',
                y=alt.Y('Winrate', scale=alt.Scale(domain=(0, 100))),
                color=alt.Color('Total Matches', scale=alt.Scale(scheme='orangered')),  # https://vega.github.io/vega/docs/schemes/#reference
                tooltip=['Opponent', 'Winrate', 'Total Matches'],
            ).properties(
                height=500
            ).interactive()
            st.altair_chart(chart, use_container_width=True)

        except KeyError:
            st.error('No data available for this team and this map type')
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
