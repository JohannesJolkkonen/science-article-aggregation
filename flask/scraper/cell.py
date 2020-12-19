import requests
from bs4 import BeautifulSoup
import boto3
import datetime

def form_query(terms):
    # Format a search-url for scraping, takes list of search terms as argument
    search_str = "+".join(terms)
    url = f"https://www.cell.com/action/doSearch?text1={search_str}&field1=AllField&Ppub=&Ppub=&journalCode=cell&sortBy=Earliest&startPage=&currentPage=&ContentItemType=fla"
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
    
    for article in soup.find_all('h2', attrs={'class': 'meta__title'}, limit=6):
        link = article.find('a')['href']
        if link is not None:
            url = 'https://cell.com' + link
        else:
            continue
        
        details = requests.get(url, headers=headers).content
        det_soup = BeautifulSoup(details, "html.parser")

        title = det_soup.find('meta', attrs={'property':'og:title'})['content']
        abstract = det_soup.find('meta', attrs={'property':'og:description'})['content']
        try: 
            date = det_soup.find('span', attrs={
                             'class': "article-header__publish-date__value"}).text
        except :
            date = 'Publication date unavailable'
        obj = {'title': title, 'abstract': abstract, 'link': url, 'date': date,'source': 'Cell'}
        DBConn.write(obj)
        print(url)
        
