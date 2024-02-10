import os
import streamlit as st

st.set_page_config(
    page_title="Overgraph - Players stats",
    page_icon="🏅",
)


def display_page_infos():
    st.subheader('Get specific stats for every player')
    st.markdown("""
                        The collected datas provide a comprehensive overview of **every player performances depending on a stat in the Overwatch League**. 
                        The records indicate the full players list and the corresponding stat value. 
                        Analyzing the players stats could help to understand the overall balance of the game and the meta.
                        """)


try:
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    df = st.session_state.df
    get_players_stat = st.session_state.get_players_stat

    stats_list = df['stat'].unique()
    # todo: sort the list
    with df_tab:
        display_page_infos()
        stat = st.selectbox('Select a stat', stats_list)
        st.write(get_players_stat(stat))

    with viz_tab:
        display_page_infos()
        max_players_percentage = st.slider('', 1, 100, 50, 1, format='%d %%')
        st.markdown('👀 _Use the slider to select the percentage of players to display_')
        order = st.radio('', ['Higher', 'Lower'], index=1)
        import plotly.express as px
        data = get_players_stat(stat)
        max_players = int(len(data) * max_players_percentage / 100)

        if order == 'Lower':
            order_label = 'lowest'
            data = data.sort_values(ascending=True)
        else:
            order_label = 'highest'
            data = data.sort_values(ascending=False)
        data = data.head(max_players)
        st.subheader(
            f'Top {max_players_percentage}% ({max_players} player{"s" if max_players != 1 else ""}) {order_label} for the stat "{stat}"')
        fig = px.pie(data, values=stat, names=data.index)
        pull_values = [0.1 if i == 0 else 0.025 for i in range(max_players)]
        fig.update_traces(textposition='inside', textinfo='percent+label+value', pull=pull_values, hole=0.2)
        st.plotly_chart(fig)
except AttributeError:
    st.error('You need to load the data from the Home page first !')
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
