import os
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Overgraph - Players stats", page_icon="🏅", )


def display_page_infos():
    st.subheader('Get specific stats for every player')
    st.markdown("""
                        The collected datas provide a comprehensive overview of **every player performances depending on a stat in the Overwatch League**. 
                        The records indicate the full players list and the corresponding stat value. 
                        Analyzing the players stats could help to understand the overall balance of the game and the meta.
                        """)


try:
    df = st.session_state.df
    get_players_stat = st.session_state.get_players_stat

    stats_list = df['stat'].unique()
    display_page_infos()
    stat = st.selectbox('Select a stat', stats_list)
    data = get_players_stat(stat)

    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])

    # todo: sort the list
    with df_tab:
        st.write(data)
    with viz_tab:

        page_size = 10
        total_players = len(data)

        max_pages = total_players // page_size + (1 if total_players % page_size > 0 else 0)
        page_number = st.slider('Select a page', 1, max_pages, 1)
        st.markdown('👀 _Use the slider to navigate through player pages_')

        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        data = data.iloc[start_index:end_index]

        st.subheader(f'Page {page_number}/{max_pages} for the stat "{stat} (from {start_index + 1} to {end_index})"')
        # Round the 'stat' column to 2 decimal places
        data[stat] = data[stat].round(2)
        formatted_stat = data[stat].apply(lambda x: "{:,}".format(x))

        fig = px.bar(data, x=stat, y=data.index, labels={'x': stat, 'y': 'Player'}, color=stat,
                     color_continuous_scale='reds')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig.update_traces(textposition='inside', text=formatted_stat, textfont_size=100, textfont_color='Black')
        st.plotly_chart(fig)
except AttributeError:
    st.error('You need to load the data from the Home page first !')
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
