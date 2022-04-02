import git
from flask import Flask, request

app = Flask(__name__)


@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('pragman_dot_io')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route('/')
def hello_world():  # put application's code here
    return 'Soon to be something... anything... again.... no again'


if __name__ == '__main__':
    app.run()
