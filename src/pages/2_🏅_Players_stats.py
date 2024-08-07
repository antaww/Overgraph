import os
import plotly.express as px
import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="Overgraph - Players stats",  # The title of the page
    page_icon="./src/static/overgraph-logo.png"  # The icon of the page
)


def display_page_infos():
    """
    This function displays the information of the page.

    It uses the Streamlit library to display a subheader and a markdown text.
    """
    st.subheader('Get specific stats for every player')
    st.markdown("""
                        The collected datas provide a comprehensive overview of **every player performances depending on a stat in the Overwatch League**. 
                        The records indicate the full players list and the corresponding stat value. 
                        Analyzing the players stats could help to understand the overall balance of the game and the meta.
                        """)


try:
    # Get the dataframe and the function to get player stats from the session state
    df = st.session_state.df
    get_players_stat = st.session_state.get_players_stat
    # Get the list of unique stats from the dataframe
    stats_list = df['stat'].unique()
    # Display the page information
    display_page_infos()
    # Select a stat from the stats list
    stat = st.selectbox('Select a stat', stats_list)
    # Get the data for the selected stat
    data = get_players_stat(stat)
    # Create tabs for the dataframe and the visualization
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    with df_tab:
        if data.empty:
            st.error('No data available for this stat')
        else:
            st.write(data)
    with viz_tab:
        if data.empty:
            st.error('No data available for this stat')
        else:
            # Set the page size and calculate the total number of players and the maximum number of pages
            page_size = 10
            total_players = len(data)
            max_pages = total_players // page_size + (1 if total_players % page_size > 0 else 0)

            # Create a slider to select a page
            page_number = st.slider('Select a page', 1, max_pages, 1)
            st.markdown('👀 _Use the slider to navigate through player pages_')

            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size

            # Get the data for the selected page
            data = data.iloc[start_index:end_index]

            st.subheader(
                f'Page {page_number}/{max_pages} for the stat "{stat} (from {start_index + 1} to {end_index})"')
            data[stat] = data[stat].round(2)
            formatted_stat = data[stat].apply(lambda x: "{:,}".format(x))

            fig = px.bar(data, x=stat, y=data.index, labels={'x': stat, 'y': 'Player'}, color=stat,
                         color_continuous_scale='reds')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            fig.update_traces(textposition='inside', text=formatted_stat, textfont_size=100, textfont_color='Black',
                              textangle=0)
            st.plotly_chart(fig)
except AttributeError:
    st.error('You need to load the data from the Home page first !')
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
