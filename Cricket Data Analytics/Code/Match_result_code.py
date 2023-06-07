import requests
import json
from bs4 import BeautifulSoup

# Navigate to the URL and fetch the HTML content
response = requests.get('https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?class=10;id=2022%2F23;trophy=136;type=season')
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
all_rows = soup.select('table.engineTable > tbody > tr.data1')


match_summary = []
for row in all_rows:             # Looping through each rows and get the data from the cells(td)
    tds = row.find_all('td')
    match_summary.append({
        'team1': tds[0].get_text(),
        'team2': tds[1].get_text(),
        'winner': tds[2].get_text(),
        'margin': tds[3].get_text(),
        'ground': tds[4].get_text(),
        'matchDate': tds[5].get_text(),
        'scorecard': tds[6].get_text()
    })

data = {
    "matchSummary": match_summary
}
print(data)

with open('match_results.json', 'w') as json_file:
    json.dump(data, json_file)