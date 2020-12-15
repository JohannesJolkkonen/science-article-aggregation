from flask import Flask, render_template
from app import app
from app import main
import os

@app.route('/', methods = ["GET"])
def home():
    # Content is a dictionary of lists from different journals 
    content = main.getContent()
    return render_template('index.html', 
                cell_content=content['Cell'], nature_content=content['Nature']) 



