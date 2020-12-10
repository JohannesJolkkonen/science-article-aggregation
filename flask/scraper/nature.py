import requests
from bs4 import BeautifulSoup
import boto3

url = ''

headers= {'User-Agent':'Mozilla/5.0'}

def scrape():
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find('div', attrs={'class': 'articleCitation'})
    
    with open('soup.txt', 'w', encoding='utf-8') as file:
        for item in line.find_all('div', attrs={'class': 'article-details'}):
            title = item.find('h2', attrs={'class':'title'}).text.split('0')[1]
            brief = item.find('span', attrs={'class':'content'}).text
            link = item.find('a', attrs={'href': lambda L: L and L.startswith('https')}).text
            file.write(f'{title} --- {brief} \n {link} \n')

scrape()
