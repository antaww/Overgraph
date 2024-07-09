<img src="https://overgraph.streamlit.app:443/~/+/media/4e13515ded64dc92409a16d07da67c67ffd8a1ab08534c303300e87b.png" alt="Overgraph" width="300"/>


## 🫸 Welcome to Overgraph, a website regrouping every Overwatch League stats to help you make the best analysis of the game.
### ☝️🤓 Note that this project is available on streamlit [here](https://overgraph.streamlit.app/).
### If you want to run the project locally, you can follow the steps below: 
- `pip install -r requirements.txt`
- `streamlit run src/0_🏠_Home.py`

## 📖 Website pages
#### 🔥 Heroes stats : Get specific stats for every hero
#### 🏅 Heroes stats by Player : Get specific stats for every hero of a player
#### ⚡ Players stats : Get specific stats for a player
#### 💡 Players stats by Team : Get specific stats for a team
#### ⚔️ Teams VS Teams : Get team scores against other teams
#### 📈 Team profile : Get a profile for a team
#### 🤺 Match analysis : Get specific stats for a match
#### 🏆 Teams leaderboard : Get the leaderboard of the teams

## 📝 Project structure
- `src/` : Contains the scripts to run the website
  - `datas/` : Contains the datas used in the project
    - `chara_img/` : Contains the images of the heroes
  - `pages/` : Contains the pages of the website
  - `scrapers/` : Contains the scripts to scrap the datas
    - `detection/` : Contains the scripts to improve default datasets (switches, timing..)
      - `imgs/` : Contains the extracted images from the extractor script
  - `static/` : Contains the css style of the website