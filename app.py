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


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)
