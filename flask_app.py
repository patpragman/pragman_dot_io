# Main flask app for Pragman Family Farms!

import os
from flask import Flask, render_template, request, jsonify, abort, send_file
from flask import send_file

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/download_bib')
def download_bib():
    # legacy code from my thesis
    path = f"{os.getcwd()}/static/quickbib.pdf"
    return send_file(path, as_attachment=True)


@app.route('/dice')
def dice():
    # dice rolling tool for my kids since they cannot get along
    return render_template("dice.html")




if __name__ == "__main__":
    app.run()
