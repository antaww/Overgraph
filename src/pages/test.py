import streamlit as st

st.image('src/static/overgraph-removebg-preview.png', width=200, use_column_width="auto")
st.markdown("""
            ### ☝️🤓 Welcome to :red[Overgraph], a website regrouping every Overwatch League stats.
            ##### Use Overgraph to get a precise analysis of the Overwatch League data like heroes stats, players stats, teams stats and matches analysis.
            ##### Are you ready to dive into the :orange[Overwatch League] data? Let's go! 👇
            ___
            ### 📖 Pages
            ##### 🔥 <a href='Heroes_stats' target='_self' style='text-decoration: underline; color:white'>**Heroes stats**</a> : Get specific stats for every hero\n
            ##### 🏅 <a href='Heroes_stats_by_Player' target='_self' style='text-decoration: underline; color:white'>**Heroes stats by Player**</a> : Get specific stats for every hero of a player\n
            ##### ⚡ <a href='Players_stats' target='_self' style='text-decoration: underline; color:white'>**Players stats**</a> : Get specific stats for a player\n
            ##### 💡 <a href='Players_stats_by_Team' target='_self' style='text-decoration: underline; color:white'>**Players stats by Team**</a> : Get specific stats for a team\n
            ##### ⚔️ <a href='Team_VS_Teams' target='_self' style='text-decoration: underline; color:white'>**Teams VS Teams**</a> : Get team scores against other teams\n
            ##### 📈 <a href='Team_profile' target='_self' style='text-decoration: underline; color:white'>**Team profile**</a> : Get a profile for a team\n
            ##### 🤺 <a href='Match_analysis' target='_self' style='text-decoration: underline; color:white'>**Match analysis**</a> : Get specific stats for a match\n
            
            ###### *👀 Pssst, you better use the sidebar to navigate through the app, it's easier!*
            ___
            ### 📊 Data
            ##### The data used in this project is from the Overwatch League. It is a professional esports league for the video game Overwatch, produced by its developer Blizzard Entertainment.
            
            *___Overgraph___ is not affiliate with the Overwatch League or Blizzard Entertainment.*
            """, unsafe_allow_html=True)