import json

import requests
from bs4 import BeautifulSoup

url = 'https://www.overbuff.com/heroes'

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

meta = {}

hero_div = soup.find_all('tr', class_='group even:bg-surface-even odd:bg-surface-odd')
heroes = {}


def handle_hero_name():
    global hero_name
    hero_name = hero_name.lower()
    hero_name = hero_name.replace(' ', '-')
    hero_name = hero_name.replace('.', '')
    hero_name = hero_name.replace(':', '')
    hero_name = hero_name.replace('ö', 'o')
    hero_name = hero_name.replace('ú', 'u')


# heroes names and roles
for i in range(0, len(hero_div), 1):
    hero_name = hero_div[i].find('a', class_='font-semibold uppercase whitespace-nowrap').text
    handle_hero_name()
    hero_role = hero_div[i].find('div', class_='leading-snug').text
    meta[hero_name] = hero_role
    heroes[hero_name] = {}
    heroes[hero_name]['role'] = hero_role

# heroes stats
for hero_name in heroes:
    print(hero_name)
    url = f'https://www.overbuff.com/heroes/{hero_name}?gameMode=competitive'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        stats = {}
        stat_value = soup.find_all('div', class_='text-sm sm:text-base leading-none')
        stat_name = soup.find_all('div', class_='text-xs sm:text-sm text-secondary')
        for i in range(0, len(stat_value), 1):
            stats[stat_name[i].text] = stat_value[i].text
            if stats[stat_name[i].text] == '—':
                stats[stat_name[i].text] = 'Unknown'
        heroes[hero_name]['stats'] = stats
    except AttributeError:
        print(f'No stats for {hero_name}')

with open('../results/heroes.json', 'w') as f:
    json.dump(heroes, f, indent=4)
