import requests
from bs4 import BeautifulSoup
import boto3
import datetime

def form_query(terms):
    # Format a search-url for scraping, takes list of search terms as argument
    url = 'https://www.cell.com/action/doSearch?journalCode=cell&seriesISSNFltraddfilter=0092-8674&date=range&dateRange=1m&searchAttempt=&searchType=advanced&doSearch=Search'
    n=1
    for term in terms:
        term.replace(' ','+')
        string = f'&op1=or&searchText{str(n)}={term}&occurrences1=all'
        url += string
        n+=1
    return url

# print(url)
headers= {'User-Agent':'Mozilla/5.0'}

def remove_prefix(string, prefix):
    if string.startswith(prefix):
        string = string.replace(prefix, '')
    return string

def scrape(DBConn, terms):
    url = form_query(terms)
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")
    
    for article in soup.find_all('div', attrs={'class': 'article-details'}):
        prefix = article.find('div', attrs={'class':'scopus'}).text
        title = remove_prefix(article.find('h2', attrs={'class':'title'}).text, prefix)
        abstract = article.find('span', attrs={'class':'content'}).text
        date = article.find('div', attrs={'class':"published-online"}).text.split(':')[1].lstrip(' ')
        link = article.find('a', attrs={'href': lambda L: L and L.startswith('https')}).text
        obj = {'title': title, 'abstract': abstract, 'link': link, 'date': date,'source': 'Cell'}
        DBConn.write(obj)
    
        
