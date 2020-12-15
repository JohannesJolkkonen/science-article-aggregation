from db.mysql_handler import DBConnection
from scraper import cell, nature
import json
 
search = ["coronavirus"]

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
            with open(f'{source}-results.txt', 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(e)
    return content


def runQuery():
    db = DBConnection()
    sql = "TRUNCATE TABLE journal_articles;"
    db.cursor.execute(sql)
    

if __name__ == '__main__':
	scrapeAll()

# runQuery()
# scrapeAll()
# getContent('Cell')
