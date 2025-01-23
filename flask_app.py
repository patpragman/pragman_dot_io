# Main flask app for Pragman Family Farms!

import os
from flask import Flask, render_template, request, jsonify, abort, send_file, flash, redirect, url_for
from flask import send_file
import smtplib

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get("FLASH_TOKEN")

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/contact', methods=["GET", 'POST'])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash('Thanks for reaching out!  We\'ll get back to you quick!', "success")
        send_email_notification(name, email, message)
        return redirect(url_for("contact") + "#contact")
    else:
        return render_template("main.html", form_submitted=True)

def send_email_notification(name, email, message):
    # Your email credentials
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("PASSWORD")
    recipient_email = os.environ.get("EMAIL_TARGET")

    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

    # Sending email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:  # Replace SMTP if not using Gmail
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{body}")
    except Exception as e:
        print(f"Error sending email: {e}")

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
