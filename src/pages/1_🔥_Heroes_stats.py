import os
import streamlit as st
import plotly.express as px

# Set the page configuration
st.set_page_config(
    page_title="Overgraph - Heroes stats",  # The title of the page
    page_icon="./src/static/overgraph-logo.png"  # The icon of the page
)


def display_page_infos():
    """
    This function displays the information of the page.

    It uses the Streamlit library to display a subheader and a Markdown text.
    """
    st.subheader('Get specific stats for every hero')
    st.markdown("""
                    The collected datas provide a comprehensive overview of **every hero performances depending on a stat in the Overwatch League**. 
                    The records indicate the full heroes list and the corresponding stat value. 
                    Analyzing the heroes stats could help to understand the overall balance of the game and the meta.
                    """)


try:
    # Get the dataframe and the function to get hero stats from the session state
    df = st.session_state.df
    get_heroes_stat = st.session_state.get_heroes_stat
    # Get the list of unique stats from the dataframe
    stats_list = df['stat'].unique()
    # Display the page information
    display_page_infos()
    # Select a stat from the stats list
    stat = st.selectbox('Select a stat', stats_list)
    # Create tabs for the dataframe and the visualization
    df_tab, viz_tab = st.tabs(["Dataframe", "Visualization"])
    # Get the data for the selected stat
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
    # Display an error message if the data is not loaded from the Home page
    st.error('You need to load the data from the Home page first !')
    # Create a button to redirect the user to the Home page
    if st.button('Go to Home'):
        home_path = os.path.join(os.getcwd(), 'src/0_🏠_Home.py')
        st.switch_page(home_path)
