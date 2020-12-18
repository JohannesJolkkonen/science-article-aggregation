import requests
from bs4 import BeautifulSoup
import boto3
import datetime


def form_query(terms):
    # Format a search-url for scraping, takes list of search terms as argument
    search_str = ''
    for term in terms:
        search_str += (term + '%20')
    url = f'https://www.nature.com/search?q={search_str}&order=date_desc&article_type=research&journal=nature'
    return url

# print(url)
headers = {'User-Agent': 'Mozilla/5.0'}

def scrape(DBConn, terms):
    url = form_query(terms)
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")

    for article in soup.find_all('h2', attrs={'role': 'heading'}, limit=6):
        link = article.find('a', attrs={'href': lambda L: L and L.startswith('/articles')})
        
        if link is not None:
            url = 'https://nature.com' + link['href']
        else:
            continue
        details = requests.get(url, headers=headers).content
        det_soup = BeautifulSoup(details, "html.parser")
        title = det_soup.find('title').text.split('|')[0].rstrip()
        abstract = det_soup.find('meta', attrs={'name': 'dc.description'})['content'][:255] + '...'
        date = det_soup.find('time', attrs={'itemprop':'datePublished'}).text
        obj = {'title': title, 'abstract': abstract,
               'link': url, 'date': date, 'source': 'Nature'}
        DBConn.write(obj)
    
# scrape(['virus', 'pandemic'])
