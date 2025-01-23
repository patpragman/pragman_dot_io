# Digital Resume!
# Patrick Pragman
# Ciego Services
# 16APRIL2022
# Flask App to watch for changes in the weather

import os
import toml
from flask import Flask, render_template, request, jsonify, abort, send_file
from metar import Metar
from get_metar import get_metar
from wxdata import get_metars, get_tafs
from local_config import Path
from datetime import datetime
from flask import send_file

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route('/')
def index():
    return render_template('main.html')





@app.route('/download_bib')
def download_bib():
    path = f"{os.getcwd()}/static/quickbib.pdf"
    return send_file(path, as_attachment=True)


@app.route('/dice')
def dice():
    return render_template("dice.html")




if __name__ == "__main__":
    app.run()
