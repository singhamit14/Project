import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=10;id=2022%2F23;trophy=136;type=season'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

links = []
rows = soup.select('table.engineTable > tbody > tr.data1')
for row in rows:
    link = 'https://www.espncricinfo.com' + row.select('td')[6].select_one('a')['href']
    links.append(link)

print(links)
# driver = webdriver.Chrome()
# for link in links:
#     driver.get(link)
# driver.quit()
#
# soup = BeautifulSoup