import math
import os
import plotly.express as px
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Overgraph - Teams leaderboard",  # The title of the page
    page_icon="./src/static/overgraph-logo.png"  # The icon of the page
)


def display_page_infos():
    """
    This function displays the information of the page.

    It uses the Streamlit library to display a subheader and a markdown text.
    """
    st.subheader('Teams Winrate Leaderboard')
    st.markdown("""
                This page displays a leaderboard of teams based on their winrate globally or on a stage. 
                The leaderboard provides a comprehensive overview of each team's performance in the Overwatch League.
                Analyzing these stats could help to understand the ranking of the teams and their performance.
                """)


try:
    # Get the dataframe and the function to get player stats from the session state
    df = st.session_state.df
    get_teams_leaderboard = st.session_state.get_teams_leaderboard

    # Get the list of unique stages from the dataframe
    stages_list = df['stage'].unique()

    # Display the page information
    display_page_infos()

    # Select a stage from the dropdown list
    stage = st.selectbox('Select a stage (not required)', [''] + list(stages_list))

    if not stage:
        stage = None
    # Get the data for the selected stage
    data = get_teams_leaderboard(stage)

    # Create tabs for the dataframe and the visualization
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        if data.empty:
            st.error('No data available for this stage')
        else:
            st.write(data)
    with viz_tab:
        if data.empty:
            st.error('No data available for this stage')
        else:
            fig = px.bar(data, x='Winrate', y='Team', title='Teams Winrate Leaderboard',
                         labels={'Winrate': 'Winrate', 'Team': 'Team'},
                         color_discrete_sequence=px.colors.qualitative.Pastel)

            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig)
except AttributeError:
    st.error('You need to load the data from the Home page first !')
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
