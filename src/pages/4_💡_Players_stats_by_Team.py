import os

import plotly.express as px
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Overgraph - Players stats by Team",  # The title of the page
    page_icon="./src/static/overgraph-logo.png"  # The icon of the page
)


def display_page_infos():
    """
    This function displays the information of the page.

    It uses the Streamlit library to display a subheader and a Markdown text.
    """
    st.subheader('Get specific stats for a team')
    st.markdown("""
                    This page provides a comprehensive overview of **each team's performance based on a specific stat in the Overwatch League**.
                    The records indicate the full list of players in the team and the corresponding stat value for each player.
                    These insights could be pivotal in enhancing the team's strategies and performance.
                """)


try:
    # Get the dataframe and the function to get player stats from the session state
    df = st.session_state.df
    get_players_stat_by_team = st.session_state.get_players_stat_by_team

    # Get the list of unique teams and stats from the dataframe
    teams_list = df['team'].unique()
    stats_list = df['stat'].unique()

    # Display the page information
    display_page_infos()

    # Select a team and a stat from the dropdown lists
    team = st.selectbox('Select a team', teams_list)
    stat = st.selectbox('Select a stat', stats_list)

    # Get the data for the selected stat and team
    data = get_players_stat_by_team(stat, team)

    # Create tabs for the dataframe and the visualization
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

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
    # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
