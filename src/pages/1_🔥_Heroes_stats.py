import os
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Overgraph - Heroes stats", page_icon="🔥", )


def display_page_infos():
    st.subheader('Get specific stats for every hero')
    st.markdown("""
                    The collected datas provide a comprehensive overview of **every hero performances depending on a stat in the Overwatch League**. 
                    The records indicate the full heroes list and the corresponding stat value. 
                    Analyzing the heroes stats could help to understand the overall balance of the game and the meta.
                    """)


try:
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    df = st.session_state.df
    get_heroes_stat = st.session_state.get_heroes_stat

    stats_list = df['stat'].unique()

    with df_tab:
        display_page_infos()
        # create a dropdown list with every unique 'stat'
        stat = st.selectbox('Select a stat', stats_list)
        # display the result
        st.write(get_heroes_stat(stat))
    with viz_tab:
        display_page_infos()
        max_heroes_percentage = st.slider('', 1, 100, 50, 1, format='%d %%')
        st.markdown('👀 _Use the slider to select the percentage of players to display_')
        order = st.radio('', ['Higher', 'Lower'], index=1)

        data = get_heroes_stat(stat)
        data = data[data.index != 'All Heroes']
        max_heroes = int(len(data) * max_heroes_percentage / 100)
        if max_heroes == 0:
            max_heroes = 1

        if order == 'Lower':
            order_label = 'lowest'
            data = data.sort_values(ascending=True)
        else:
            order_label = 'highest'
            data = data.sort_values(ascending=False)
        data = data.head(max_heroes)
        st.subheader(
            f'Top {max_heroes_percentage}% ({max_heroes} hero{"es" if max_heroes != 1 else ""}) {order_label} for the '
            f'stat "{stat}"')
        fig = px.pie(data, values=stat, names=data.index)
        pull_values = [0.1 if i == 0 else 0.025 for i in range(max_heroes)]
        fig.update_traces(textposition='inside', textinfo='percent+label+value', pull=pull_values, hole=0.2)
        st.plotly_chart(fig)

except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
