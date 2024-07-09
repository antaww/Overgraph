import json

import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://www.overbuff.com/heroes'

# Headers for the request
headers = {'User-Agent': 'Mozilla/5.0'}

# Send a GET request to the website
response = requests.get(url, headers=headers)

# Parse the response text with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all hero divs in the parsed HTML
hero_div = soup.find_all('tr', class_='group even:bg-surface-even odd:bg-surface-odd')

# Initialize an empty dictionary to store hero data
heroes = {}

# Constants for the maximum season numbers and skill tiers
max_season_ow2 = 8
max_season_ow1 = 36
skill_tiers = ['all', 'bronze', 'silver', 'gold', 'platinum', 'diamond', 'master', 'grandmaster']


def handle_hero_name():
    """
    This function handles the hero name by converting it to lowercase and replacing certain characters.

    It uses the global variable hero_name.
    """
    global hero_name
    hero_name = hero_name.lower()
    hero_name = hero_name.replace(' ', '-')
    hero_name = hero_name.replace('.', '')
    hero_name = hero_name.replace(':', '')
    hero_name = hero_name.replace('ö', 'o')
    hero_name = hero_name.replace('ú', 'u')


# Loop through the hero divs to get hero names and roles
for i in range(0, len(hero_div), 1):
    hero_name = hero_div[i].find('a', class_='font-semibold uppercase whitespace-nowrap').text
    handle_hero_name()
    hero_role = hero_div[i].find('div', class_='leading-snug').text
    heroes[hero_name] = {}
    heroes[hero_name]['name'] = hero_name
    heroes[hero_name]['role'] = hero_role

# Loop through the heroes to get their stats
for hero_name in heroes:
    print(hero_name)
    heroes[hero_name]['stats'] = {}

    # loop through skill tiers
    for skill_tier in skill_tiers:
        heroes[hero_name]['stats'][skill_tier] = {}

        # overbuff bug :
        # ow1 : 1/2/4/7/10/16 not working
        # ow2 : 7 not working
        for game in range(1, 2 + 1, 1):
            for season_nbr in range(1, max_season_ow1 + 1, 1):
                print(f'scraping {hero_name} in ow{game}s{season_nbr} in {skill_tier}')
                if game == 2 and season_nbr > max_season_ow2:
                    print(f'Season {season_nbr} in ow{game} not available')
                    break
                if season_nbr < 10:
                    season_nbr = f'0{season_nbr}'
                season = f'ow{game}s{season_nbr}'
                delay = 0.2
                url = (f'https://www.overbuff.com/heroes/{hero_name}'
                       f'?gameMode=competitive'
                       f'&season={season}'
                       f'&skillTier={skill_tier}')
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                try:
                    seasons = {}
                    stats = {}
                    stat_value = soup.find_all('div', class_='text-sm sm:text-base leading-none')
                    stat_name = soup.find_all('div', class_='text-xs sm:text-sm text-secondary')
                    for i in range(0, len(stat_value), 1):
                        stats[stat_name[i].text] = stat_value[i].text
                        if stats[stat_name[i].text] == '—':
                            stats[stat_name[i].text] = 'Unknown'
                    heroes[hero_name]['stats'][skill_tier][season] = stats
                except AttributeError:
                    print(f'No stats for {hero_name} in {season}')

with open('../datas/heroes.json', 'w') as f:
    json.dump(heroes, f, indent=4)
