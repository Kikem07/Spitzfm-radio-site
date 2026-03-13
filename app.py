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


# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
