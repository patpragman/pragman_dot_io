import os

import git
from flask import Flask, request
from os import system

app = Flask(__name__)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        system('sync.sh')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/')
def hello_world():  # put application's code here
    return 'Soon to be something... anything... again.... no again'

@app.route('/test')
def test():
    output = [number for number in range(0, 100)]
    return f"More testing, further testing! <br>{output}"

if __name__ == '__main__':
    app.run()
