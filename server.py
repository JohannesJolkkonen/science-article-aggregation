from flask import Flask, render_template, redirect
from db.mysql_handler import DBConnection
import threading
import main

app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    content = main.getContent('Cell')
    return render_template('index.html', content=content)

if __name__ == '__main__':
    app.run()