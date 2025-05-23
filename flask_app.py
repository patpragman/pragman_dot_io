import os
from flask import Flask, render_template, request, jsonify, abort, send_file, flash, redirect, url_for, session
import smtplib
from datetime import datetime
import stripe
import traceback

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = os.environ.get("FLASH_TOKEN")

# Initialize Stripe with your secret key
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

def initialize_cart():
    """Ensure the cart exists in the session."""
    if "cart" not in session:
        session["cart"] = []

def get_stripe_products():
    """
    Fetch active products from Stripe with their default price expanded.
    Each product is augmented with:
      - price: the price in dollars (converted from cents)
      - price_id: the ID of the default price
      - image_url: the first image URL from the product's images array (if available)
    """
    products = []
    stripe_products = stripe.Product.list(active=True, expand=["data.default_price"])
    for prod in stripe_products.data:
        if prod.get("default_price"):
            prod.price = prod.default_price.unit_amount / 100.0  # Convert cents to dollars
            prod.price_id = prod.default_price.id
        else:
            prod.price = None
            prod.price_id = None

        prod.inventory = int(prod.metadata.get("inventory", 0))


        if prod.metadata.get("online_sales") == "True":
            prod.image_url = prod.images[0] if prod.images and len(prod.images) > 0 else None
            products.append(prod)

    return products

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/store')
def store():
    initialize_cart()
    products = get_stripe_products()
    publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")

    return render_template("store.html", products=products, cart=session['cart'], publishable_key=publishable_key)

@app.route('/services')
def services():
    initialize_cart()
    products = get_stripe_products()
    publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")

    return render_template("services.html")


@app.route("/clear-cart")
def clear_cart():
    session["cart"] = []  # Reset cart
    session.modified = True
    return redirect(url_for("store"))

@app.route('/remove-from-cart', methods=['GET', 'POST'])
def remove_from_cart():
    if request.method == "POST":
        form_data = request.form.to_dict()
        hash_to_remove = form_data.get('id')
        session['cart'] = [item for item in session['cart'] if item.get('id') != hash_to_remove]
        session.modified = True
        products = get_stripe_products()
        return redirect(url_for("store"))
    else:
        products = get_stripe_products()
        return redirect(url_for("store"))

@app.route('/add-to-cart', methods=["GET", "POST"])
def add_to_cart():
    if request.method == "POST":
        raw_form_data = request.form.to_dict()
        raw_form_data['ingest_time'] = datetime.utcnow().timestamp()
        # Use the Stripe price_id in the unique identifier
        raw_form_data['id'] = f"{hash(raw_form_data['ingest_time'])}-{raw_form_data.get('price_id','')}"
        if 'quantity' not in raw_form_data or not raw_form_data['quantity']:
            raw_form_data['quantity'] = 1
        session['cart'].append(raw_form_data)
        print("Cart after adding item:", session['cart'])
        session.modified = True
        products = get_stripe_products()
        return redirect(url_for("store"))
    else:
        products = get_stripe_products()
        print("Cart:", session['cart'])
        return redirect(url_for("store"))

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        flash("Thanks for reaching out! We'll get back to you quick!", "success")
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
    path = os.path.join(os.getcwd(), "static", "quickbib.pdf")
    return send_file(path, as_attachment=True)

@app.route('/instructions-mark3')
def instructions_mark3():
    path = os.path.join(os.getcwd(), "static", "instructions-mark3.pdf")
    return send_file(path, as_attachment=True)

@app.route('/robots.txt')
def robots():
    path = os.path.join(os.getcwd(), "static", "robots.txt")
    return send_file(path)


@app.route('/dice')
def dice():
    return render_template("dice.html")

# ----------------- Stripe Checkout Integration -----------------




@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    initialize_cart()
    line_items = []
    for item in session["cart"]:
        quantity = int(item.get('quantity', 1))
        if item.get('price_id'):
            line_items.append({
                'price': item['price_id'],
                'quantity': quantity,
            })
        else:
            try:
                unit_amount = int(float(item.get('price', 0)) * 100)
            except Exception:
                unit_amount = 0
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.get('product_id', 'Unknown Product'),
                    },
                    'unit_amount': unit_amount,
                },
                'quantity': quantity,
            })
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            shipping_address_collection={
                'allowed_countries': ['US', 'CA']
            },
            shipping_options=[
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 0, "currency": "usd"},
                        "display_name": "Pickup in Anchorage",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 1},
                            "maximum": {"unit": "business_day", "value": 7}
                        }
                    }
                },
                {
                    "shipping_rate_data": {
                        "type": "fixed_amount",
                        "fixed_amount": {"amount": 25000, "currency": "usd"},
                        "display_name": "Shipping to US/Canada",
                        "delivery_estimate": {
                            "minimum": {"unit": "business_day", "value": 7},
                            "maximum": {"unit": "business_day", "value": 14}
                        }
                    }
                }
            ],
            success_url=url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('store', _external=True),
        )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(error=str(e)), 500



@app.route('/success')
def success():
    session["cart"] = []
    session.modified = True
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
