import os
from flask import Flask, render_template, request, jsonify, abort, send_file, flash, redirect, url_for, session
import smtplib
from datetime import datetime
import stripe  # New: import stripe

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get("FLASH_TOKEN")

# Initialize Stripe with your secret key
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# product definition
PRODUCTS = {
    "complete_kit": {"name": "Complete Hydroponics Kit", "price": 200,
                     "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
    "module_component": {"name": "Module Component", "price": 10,
                         "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
    "base_component": {"name": "Base Component", "price": 10,
                       "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
    "bucket_stiffener": {"name": "Bucket Stiffener", "price": 10,
                         "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
    "cap_components": {"name": "Cap Components", "price": 10,
                       "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
    "pump": {"name": "Pump", "price": 50,
             "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
    "grow_basket": {"name": "Grow Basket", "price": 1,
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent vel lorem eget libero tincidunt tincidunt."},
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
        # Ensure quantity is recorded (default to 1 if missing)
        if 'quantity' not in raw_form_data:
            raw_form_data['quantity'] = 1
        session['cart'].append(raw_form_data)
        print(session['cart'])
        session.modified = True
        return render_template("store.html", products=PRODUCTS.values(), cart=session['cart'])
    else:
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
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("PASSWORD")
    recipient_email = os.environ.get("EMAIL_TARGET")
    subject = f"New Contact Form Submission from {name}"
    body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, f"Subject: {subject}\n\n{body}")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/download_bib')
def download_bib():
    path = f"{os.getcwd()}/static/quickbib.pdf"
    return send_file(path, as_attachment=True)

@app.route('/dice')
def dice():
    return render_template("dice.html")

# ----------------- New Checkout and Stripe Integration -----------------

@app.route('/checkout')
def checkout():
    initialize_cart()
    total = 0
    for item in session["cart"]:
        # Convert quantity to int (defaulting to 1 if not present)
        quantity = int(item.get('quantity', 1))
        total += float(item['price']) * quantity
    # Pass the Stripe publishable key to the template for Stripe.js
    publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")
    return render_template("checkout.html", cart=session["cart"], total=total, publishable_key=publishable_key)


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    initialize_cart()
    line_items = []
    for item in session["cart"]:
        quantity = int(item.get('quantity', 1))
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['product_id'],
                },
                'unit_amount': int(float(item['price']) * 100),
            },
            'quantity': quantity,
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            # Collect shipping address from allowed countries
            shipping_address_collection={
                'allowed_countries': ['US', 'CA', 'GB', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'BR', 'MX', 'JP', 'SG']
            },
            # Optionally set shipping options (e.g., standard vs. express)
            shipping_options=[
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {'amount': 500, 'currency': 'usd'},
                        'display_name': 'Standard Shipping',
                        'delivery_estimate': {
                            'minimum': {'unit': 'business_day', 'value': 5},
                            'maximum': {'unit': 'business_day', 'value': 7},
                        },
                    },
                },
                {
                    'shipping_rate_data': {
                        'type': 'fixed_amount',
                        'fixed_amount': {'amount': 1500, 'currency': 'usd'},
                        'display_name': 'Express Shipping',
                        'delivery_estimate': {
                            'minimum': {'unit': 'business_day', 'value': 2},
                            'maximum': {'unit': 'business_day', 'value': 3},
                        },
                    },
                },
            ],
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('checkout', _external=True),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/success')
def success():
    # Optionally clear the cart after successful payment
    session["cart"] = []
    session.modified = True
    return render_template("success.html")

if __name__ == "__main__":
    app.run()
