import os

from flask import Flask, request
from os import system


app = Flask(__name__)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        cwd = os.getcwd()
        os.system(f'{cwd}/test/reload.sh')  # reload
        return 'Website update attempted...', 200
    else:
        return 'Wrong event type', 400


@app.route('/')
def hello_world():  # put application's code here
    return 'Soon to be something... anything... again.... no again'

@app.route('/test')
def test():
    output = "<br>".join([str(number) for number in range(50, 100)])
    return f"Work Dammit!  More testing, further again and again and again! <br>{output}"

if __name__ == '__main__':
    app.run()
