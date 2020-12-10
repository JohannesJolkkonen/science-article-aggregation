from flask import Flask, render_template
from app import app
from app import main
import os

@app.route('/', methods = ["GET"])
def home():
    content = main.getContent('Cell')
    return render_template('index.html', content=content) 



