#coding: utf-8
import flask
from config import *
from db import selectrow

app = Flask(__name__)
application = app

@app.route('/')
def main():
    row = selectrow()
    return render_template("main.html", list=row)
    
if __name__ == '__main__':
    app.run()