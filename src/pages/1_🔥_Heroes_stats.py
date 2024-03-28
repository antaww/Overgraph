import os
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Overgraph - Heroes stats",
    page_icon="./src/static/overgraph-logo.png"
)


def display_page_infos():
    st.subheader('Get specific stats for every hero')
    st.markdown("""
                    The collected datas provide a comprehensive overview of **every hero performances depending on a stat in the Overwatch League**. 
                    The records indicate the full heroes list and the corresponding stat value. 
                    Analyzing the heroes stats could help to understand the overall balance of the game and the meta.
                    """)


try:
    df = st.session_state.df
    get_heroes_stat = st.session_state.get_heroes_stat

    stats_list = df['stat'].unique()

    display_page_infos()
    stat = st.selectbox('Select a stat', stats_list)
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    data = get_heroes_stat(stat)

    with df_tab:
        if data.empty:
            st.error('No data available for this stat')
        else:
            st.write(data)
    with viz_tab:
        if data.empty:
            st.error('No data available for this stat')
        else:
            max_heroes_percentage = st.slider('', 1, 100, 50, 1, format='%d %%')
            st.markdown('👀 _Use the slider to select the percentage of players to display_')
            order = st.radio('', ['Higher', 'Lower'], index=0)

            data = data[data.index != 'All Heroes']

            for role in data['Role'].unique():
                data_role = data[data['Role'] == role]
                max_heroes = int(len(data_role) * max_heroes_percentage / 100)
                if max_heroes == 0:
                    max_heroes = 1

                if order == 'Lower':
                    order_label = 'lowest'
                    data_role = data_role.sort_values(ascending=True, by=stat)
                else:
                    order_label = 'highest'
                    data_role = data_role.sort_values(ascending=False, by=stat)
                data_role = data_role.head(max_heroes)

                st.subheader(
                    f'Top {max_heroes_percentage}% ({max_heroes} hero{"es" if max_heroes != 1 else ""}) {order_label} for the '
                    f'stat "{stat}" in the role "{role}"')
                fig = px.treemap(data_role, path=[data_role.index], values=stat)
                fig.update_traces(hovertemplate='<b>%{label}</b><br>%{value}<extra></extra>')
                st.plotly_chart(fig)
except AttributeError:
    # explain that the user goes to the page Heroes without having loaded the data from the Home page
    st.error('You need to load the data from the Home page first !')
    # # create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
