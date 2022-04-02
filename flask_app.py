import os

import git
from flask import Flask, request
from os import system

app = Flask(__name__)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        system('. /home/ciegoservices/test/sync.sh')
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/')
def hello_world():  # put application's code here
    return 'Soon to be something... anything... again.... no again'

@app.route('/test')
def test():
    output = "<br>".join([str(number) for number in range(50, 100)])
    return f"More testing, further testing! <br>{output}"

if __name__ == '__main__':
    app.run()
