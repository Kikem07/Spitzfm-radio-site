from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

STREAM_URL = "https://or.mysonicserver.com:8058/stream"
TAGLINE = "FULL WEBSITE COMING SOON"
SCHEDULE = []


def get_current_show():
    return "Now Playing"


def get_market_day():
    weekday = datetime.today().weekday()  # Monday = 0, Sunday = 6

    mapping = {
        0: "Nkwo",   # Monday
        1: "Afor",   # Tuesday
        2: "Orie",   # Wednesday
        3: "Afor",   # Thursday
        4: "Nkwo",   # Friday
        5: "Eke",    # Saturday
        6: "Eke"     # Sunday
    }

    return mapping[weekday]


# -------------------------
# PRODUCT LIST
# -------------------------
PRODUCTS = [
    {"id": 1, "name": "T‑Shirt (Standard Logo)", "price": 19.99, "image": "tshirt_standard_logo.jpg"},
    {"id": 2, "name": "T‑Shirt (Vinyl Logo)", "price": 24.99, "image": "tshirt_vinyl_logo.jpg"},
    {"id": 3, "name": "Mug (Standard Logo)", "price": 9.99, "image": "mug_standard_logo.jpg"},
    {"id": 4, "name": "Mug (Vinyl Logo)", "price": 12.99, "image": "mug_vinyl_logo.jpg"},
    {"id": 5, "name": "Candle (Standard Logo)", "price": 14.99, "image": "candle_standard_logo.jpg"},
    {"id": 6, "name": "Candle (Vinyl Logo)", "price": 18.99, "image": "candle_vinyl_logo.jpg"},
    {"id": 7, "name": "Lemon Tree (Standard Logo)", "price": 7.99, "image": "lemon_tree_standard_logo.jpg"},
    {"id": 8, "name": "Lemon Tree (Vinyl Logo)", "price": 9.99, "image": "lemon_tree_vinyl_logo.jpg"},
]


# -------------------------
# HOMEPAGE
# -------------------------
@app.route("/")
def index():
    return render_template(
        "index.html",
        tagline=TAGLINE,
        stream_url=STREAM_URL,
        schedule=SCHEDULE,
        current_show=get_current_show(),
        market_day=get_market_day(),
    )


# -------------------------
# SHOP
# -------------------------
@app.route("/shop")
def shop():
    return render_template(
        "shop.html",
        products=PRODUCTS,
        tagline=TAGLINE,
        market_day=get_market_day(),
        stream_url=STREAM_URL,
    )


# -------------------------
# PRODUCT DETAIL PAGE
# -------------------------
@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404

    return render_template(
        "products.html",
        product=product,
        tagline=TAGLINE,
        market_day=get_market_day(),
        stream_url=STREAM_URL,
    )


# -------------------------
# SCHEDULE
# -------------------------
@app.route("/schedule")
def schedule():
    return render_template(
        "schedule.html",
        tagline=TAGLINE,
        market_day=get_market_day(),
        stream_url=STREAM_URL,
    )


# -------------------------
# ADVERTISING
# -------------------------
@app.route("/advertising")
def advertising():
    return render_template("advertising.html")


# -------------------------
# ABOUT
# -------------------------
@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------
# ROTA
# -------------------------
@app.route("/rota")
def rota():
    return render_template("rota.html")


from flask import request, jsonify, session
app.secret_key = "spitzfm-secret-key"  # required for session cart


def get_cart():
    if "cart" not in session:
        session["cart"] = {}
    return session["cart"]


@app.route("/cart/add", methods=["POST"])
def cart_add():
    data = request.get_json()
    product_id = str(data.get("id"))
    size = data.get("size")

    product = next((p for p in PRODUCTS if p["id"] == int(product_id)), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    cart = get_cart()

    key = product_id
    if size:
        key = f"{product_id}_{size}"

    if key not in cart:
        cart[key] = {
    "id": product["id"],
    "name": product["name"],
    "price": product["price"],
    "qty": data.get("qty", 1),
    "size": size
}

    else:
        ccart[key]["qty"] += data.get("qty", 1)

    session.modified = True
    return jsonify({"success": True})


@app.route("/cart/get")
def cart_get():
    return jsonify(get_cart())


@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    data = request.get_json()
    product_id = str(data.get("id"))

    cart = get_cart()

    # remove all variants (size or no size)
    keys_to_delete = [k for k in cart if k.startswith(product_id)]
    for k in keys_to_delete:
        del cart[k]

    session.modified = True
    return jsonify({"success": True})


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
