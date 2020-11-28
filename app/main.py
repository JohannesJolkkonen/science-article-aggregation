from db.mysql_handler import DBConnection
from scraper import cell
import json
 
def scrapeAll():
    db = DBConnection()
    cell.scrape(db)

def getContent(source):
    db = DBConnection()
    sql = f"SELECT * from journal_articles where source='{source}'"
    jsonfile = db.query(sql)
    with open('results.txt', 'w') as file:
        json.dump(jsonfile, file, indent=4)
    return jsonfile


def runQuery():
    db = DBConnection()
    sql = "TRUNCATE TABLE journal_articles;"
    db.cursor.execute(sql)
    

if __name__ == '__main__':
	scrapeAll()

# runQuery()
# scrapeAll()
# getContent('Cell')
