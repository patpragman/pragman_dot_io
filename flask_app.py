import os

from flask import Flask, request
from os import system


app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'Soon to be something... anything... again.... no again'

@app.route('/test')
def test():
    output = "<br>".join([str(number) for number in range(50, 100)])
    return f"Uno dos tres!  More testing, further again and again and again! <br>{output}"

if __name__ == '__main__':
    app.run()
