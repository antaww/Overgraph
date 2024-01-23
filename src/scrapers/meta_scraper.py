import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.overbuff.com/meta?platform=pc&gameMode=competitive'

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

meta = {}

heroes = soup.find_all('div', class_='text-sm sm:text-base font-medium')
titles = soup.find_all('h1', class_='flex-1 self-end text-lg font-sans font-medium pl-2')
percentages = soup.find_all('td', class_='px-3 py-4 text-sm font-medium whitespace-nowrap space-y-1')

for i in range(0, len(titles), 1):
    title = titles[i].get_text(strip=True)
    meta[title] = {}

    for j in range(i, i + 5):
        hero = heroes[j].find('a').text
        percentage = percentages[j].find('span').get_text(strip=True)
        meta[title][hero] = percentage

print(meta)
with open('../results/meta.json', 'w') as f:
    json.dump(meta, f, indent=4)

