# Main flask app for Pragman Family Farms!

import os
from flask import Flask, render_template, request, jsonify, abort, send_file, flash, redirect, url_for, session
from flask import send_file
import smtplib
from datetime import datetime

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get("FLASH_TOKEN")

# product definition
PRODUCTS = {
    "complete_kit": {"name": "Complete Hydroponics Kit", "price": 200,
                     "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget "
                                   "libero tincidunt tincidunt. "
                     },
    "module_component": {"name": "Module Component", "price": 10,
                         "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem "
                                       "eget libero tincidunt tincidunt."},
    "base_component": {"name": "Base Component", "price": 10, "description":"Lorem ipsum dolor sit amet, consectetur "
                                                                            "adipiscing elit. Praesent vel lorem eget "
                                                                            "libero tincidunt tincidunt."},
    "bucket_stiffener": {"name": "Bucket Stiffener", "price": 10, "description":"Lorem ipsum dolor sit amet, "
                                                                                "consectetur adipiscing elit. "
                                                                                "Praesent vel lorem eget libero "
                                                                                "tincidunt tincidunt."},
    "cap_components": {"name": "Cap Components", "price": 10, "description":"Lorem ipsum dolor sit amet, consectetur "
                                                                            "adipiscing elit. Praesent vel lorem eget"
                                                                            " libero tincidunt tincidunt."},
    "pump": {"name": "Pump", "price": 50, "description":"Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                                                        "Praesent vel lorem eget libero tincidunt tincidunt."},
    "grow_basket": {"name": "Grow Basket", "price": 1, "description":"Lorem ipsum dolor sit amet, consectetur "
                                                                     "adipiscing elit. Praesent vel lorem eget libero "
                                                                     "tincidunt tincidunt."},
}

def initialize_cart():
    """Ensure the cart exists in the session."""
    if "cart" not in session:
        session["cart"] = []


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/store')
def store():
    initialize_cart()
    print(session['cart'])
    return render_template("store.html", products=PRODUCTS.values(), cart=session['cart'])

@app.route("/clear-cart")
def clear_cart():
    session["cart"] = []  # Reset cart
    session.modified = True
    return redirect(url_for("store"))


@app.route('/remove-from-cart', methods=['GET', 'POST'])
def remove_from_cart():
    if request.method == "POST":
        print(request.form.to_dict())
        hash_to_remove = request.form.to_dict()['id']
        session['cart'] = [item for item in session['cart'] if item['id'] != hash_to_remove]
        session.modified = True
        return render_template("store.html", products=PRODUCTS.values(), cart=session['cart'])
    else:
        return render_template("store.html", products=PRODUCTS.values(), cart=session['cart'])


@app.route('/add-to-cart', methods=["GET", 'POST'])
def add_to_cart():
    if request.method == "POST":
        raw_form_data = request.form.to_dict()
        raw_form_data['ingest_time'] = datetime.utcnow().timestamp()
        raw_form_data['id'] = f"{hash(raw_form_data['ingest_time'])}-{raw_form_data['product_id']}"
        session['cart'].append(raw_form_data)
        #print(raw_form_data)
        print(session['cart'])
        session.modified = True
        return render_template("store.html", products=PRODUCTS.values(), cart=session['cart'])
    else:
        #print(PRODUCTS.values())
        print(session['cart'])
        return render_template("store.html", products=PRODUCTS.values(), cart=session["cart"])

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
