import os

from flask import Flask, request
from os import system


app = Flask(__name__)

@app.route('/')
def home():  # put application's code here
    return 'Changed pipeline - not entirely autonomous...but yah...'


if __name__ == '__main__':
    app.run()
