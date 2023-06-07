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


data = []
driver = webdriver.Chrome()
for link in links:
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup)
#     # Find the match details
    match_details = soup.find('div', text='Match Details')
    teams = [team.text.replace(' Innings', '') for team in match_details.find_all('span')]

    # Find the tables containing the bowling data
    tables = soup.find_all('table', class_='ds-table')

    # Extract the bowling data from the first innings
    first_inning_rows = [row for row in tables[1].find_all('tr') if len(row.find_all('td')) >= 11]
    bowling_summary = []
    for row in first_inning_rows :
        tds = row.find_all('td')
        bowling_summary.append({
            'match' : ' Vs '.join(teams),
            'bowlingTeam' : teams[1],
            'bowlerName' : tds[0].find('a').text.replace(' ', ''),
            'overs' : tds[1].text,
            'maiden' : tds[2].text,
            'runs' : tds[3].text,
            'wickets' : tds[4].text,
            'economy' : tds[5].text,
            '0s' : tds[6].text,
            '4s' : tds[7].text,
            '6s' : tds[8].text,
            'wides' : tds[9].text,
            'noBalls' : tds[10].text,
        })

    # Extract the bowling data from the second innings
    second_inning_rows = [row for row in tables[3].find_all('tr') if len(row.find_all('td')) >= 11]
    for row in second_inning_rows :
        tds = row.find_all('td')
        bowling_summary.append({
            'match' : ' Vs '.join(teams),
            'bowlingTeam' : teams[0],
            'bowlerName' : tds[0].find('a').text.replace(' ', ''),
            'overs' : tds[1].text,
            'maiden' : tds[2].text,
            'runs' : tds[3].text,
            'wickets' : tds[4].text,
            'economy' : tds[5].text,
            '0s' : tds[6].text,
            '4s' : tds[7].text,
            '6s' : tds[8].text,
            'wides' : tds[9].text,
            'noBalls' : tds[10].text,
        })
data = {
    'bowlingSummary' : bowling_summary
}
print(data)

with open('bowlling_results.json', 'w') as json_file:
    json.dump(data, json_file)


#return {'bowlingSummary' : bowling_summary}


