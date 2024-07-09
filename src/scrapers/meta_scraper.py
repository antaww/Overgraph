import requests
from bs4 import BeautifulSoup
import json

# URL of the website to scrape
url = 'https://www.overbuff.com/meta?platform=pc&gameMode=competitive'

# Headers for the request
headers = {'User-Agent': 'Mozilla/5.0'}

# Send a GET request to the website
response = requests.get(url, headers=headers)

# Parse the response text with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Initialize an empty dictionary to store meta data
meta = {}

# Find all hero divs in the parsed HTML
heroes = soup.find_all('div', class_='text-sm sm:text-base font-medium')

# Find all title divs in the parsed HTML
titles = soup.find_all('h1', class_='flex-1 self-end text-lg font-sans font-medium pl-2')

# Find all percentage divs in the parsed HTML
percentages = soup.find_all('td', class_='px-3 py-4 text-sm font-medium whitespace-nowrap space-y-1')

# Loop through the title divs to get meta data
for i in range(0, len(titles), 1):
    title = titles[i].get_text(strip=True)
    meta[title] = {}

    # Loop through the hero and percentage divs to get hero data
    for j in range(i, i + 5):
        hero = heroes[j].find('a').text
        percentage = percentages[j].find('span').get_text(strip=True)
        meta[title][hero] = percentage

# Print the meta data
print(meta)

# Write the meta data to a JSON file
with open('../datas/meta.json', 'w') as f:
    json.dump(meta, f, indent=4)