# library which is required
# Openpyxl library is necessary to for this text extraction
import pandas as pd
import requests
from bs4 import BeautifulSoup

# converting input.xlsx into data frame and fetching url from data frame
df = pd.read_excel('Input.xlsx')
urls = df['URL'].tolist()

# apply for loop to getting each url
for url in urls:
    response = requests.get(url)
    # checking url is fetchable or not
    if response.status_code == 200:
        # parse the html of Url
        soup = BeautifulSoup(response.content, 'html.parser')
        #  for url title
        article_title = soup.find('h1', class_='entry-title')
        #  for url content
        article = soup.find('div', class_='td-post-content tagdiv-type')
        #  apply for loop for checking title and content having some text
        if article_title is not None and article is not None:
            article_title = article_title.get_text()
            article = article.get_text()

    # url declare as file name
    file_name = url.replace('/', '').replace(':', '') + '.txt'
    # opening file with write mode and encoding represent it will push all the word latter like latin style
    with open(file_name, 'w', encoding='utf-8') as f:
        #  url having both section or not
        if article_title and article:
            # writing the text in file
            f.write(article_title + '\n\n' + article)
