import boto3
import mysql.connector
import os

class DBConnection:
    
    def __init__(self):
        self.name = 'content'
        self.host = os.getenv('DB_HOST')
        self.pwd = os.getenv('DB_PASS')
        self.usr = os.getenv('DB_USER')
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.usr,
                password=self.pwd,
                database=self.name)
            
            print(f"Connected to database: '{self.name}''")
            return conn
            
        except Exception as e:
            print(f"Database connection failed; {e}")
            exit()
        
    def create_table(self):
        sql_create_table = """
                CREATE TABLE IF NOT EXISTS journal_articles(
                title text NOT NULL, 
                abstract text NOT NULL, 
                url text NOT NULL, 
                source text NOT NULL, 
                id int NOT NULL AUTO_INCREMENT PRIMARY KEY)
            """
        conn.cursor().execute(sql_create_table)
        return True

    def write(self, dict):
        if self.check_title_exists(dict['title']):
            print(f"{dict['title']} already in database -- skip duplicate.\n")
            return
        sql = f"""
            INSERT INTO journal_articles (title, abstract, url, published_date, source) 
            VALUES (
                '{dict['title']}',
                '{dict['abstract']}',
                '{dict['link']}',
                '{dict['date']}',
                '{dict['source']}');
            """
        self.cursor.execute(sql)
        self.conn.commit()
        print(f"Added {dict['title']}. Published: {dict['date']} on journal: {dict['source']}")

    def query(self, sql):
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def truncate(self):
        sql = """TRUNCATE TABLE journal_articles"""
        self.cursor.execute(sql)
        return 

    def check_title_exists(self, title):
        sql = f"""
            SELECT * FROM journal_articles 
            WHERE title = "{title}"; 
            """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        if len(data) > 0:
            return True
        else:
            return False
