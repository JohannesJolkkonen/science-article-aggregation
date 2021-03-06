from db.mysql_handler import DBConnection
from scraper import cell, nature
import json
 
search = ["covid-19"]

def scrapeAll():
    db = DBConnection()
    db.truncate()
    cell.scrape(db, search)
    print('Finished scraping Cell.\n')
    nature.scrape(db, search)
    print('Finished scraping Nature.\n')

def getContent():
    print('Fetching content from database\n')
    sources = ["Cell", "Nature"]
    content = {}
    db = DBConnection()
    for source in sources:
        try:
            sql = f"SELECT * from journal_articles where source='{source}'"
            data = db.query(sql)
            content[source] = data
        except Exception as e:
            print(e)
    content['meta'] = {'topic': ' '.join(search)}
    return content


def runQuery():
    db = DBConnection()
    sql = "TRUNCATE TABLE journal_articles;"
    db.cursor.execute(sql)

# scrapeAll()

# runQuery()
# getContent('Cell')
