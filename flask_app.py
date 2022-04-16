import os

from flask import Flask, request
from os import system


app = Flask(__name__)

@app.route('/')
def home():  # put application's code here
    return 'Changed pipeline - not entirely autonomous...but yah...'

@app.route('/check_in_am')
def check():
    return "Let's see if this worked..."



if __name__ == '__main__':
    app.run()
