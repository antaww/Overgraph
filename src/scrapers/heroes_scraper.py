import requests
from bs4 import BeautifulSoup

url = 'https://www.overbuff.com/heroes'

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

meta = {}

heroe_div = soup.find_all('tr', class_='group even:bg-surface-even odd:bg-surface-odd')
heroes = {}

for i in range(0, len(heroe_div), 1):
    heroe_name = heroe_div[i].find('a', class_='font-semibold uppercase whitespace-nowrap').text
    heroe_role = heroe_div[i].find('div', class_='leading-snug').text
    meta[heroe_name] = heroe_role
    heroes[heroe_name] = {}
    heroes[heroe_name]['role'] = heroe_role

print(heroes)