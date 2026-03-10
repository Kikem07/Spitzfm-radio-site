from datetime import datetime, time
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

STREAM_URL = "https://or.mysonicserver.com:8058/stream"
NOW_PLAYING_API = "https://or.mysonicserver.com/cp/get_info.php?p=8058"

SCHEDULE = [
    {"name": "Morning Vibes", "start": time(6, 0), "end": time(10, 0), "description": "Chilled, uplifting tracks."},
    {"name": "Workday Flow", "start": time(10, 0), "end": time(17, 0), "description": "Focus-friendly beats."},
    {"name": "Evening Session", "start": time(17, 0), "end": time(22, 0), "description": "Feel-good tunes."},
    {"name": "Late Night", "start": time(22, 0), "end": time(23, 59), "description": "Ambient and downtempo."},
]

def get_current_show(now=None):
    if now is None:
        now = datetime.now().time()
    for show in SCHEDULE:
        if show["start"] <= now <= show["end"]:
            return show
    return None

def fetch_now_playing():
    """
    Normalise your host's JSON into a consistent shape.

    Adjust the key names below once you inspect the real JSON from:
    https://or.mysonicserver.com/cp/get_info.php?p=8058
    """
    try:
        r = requests.get(NOW_PLAYING_API, timeout=3)
        data = r.json()

        # Guessing common keys; tweak these to match your actual response
        title = data.get("title") or data.get("song") or "Live Stream"
        artist = data.get("artist", "")
        listeners = int(data.get("listeners", 0))

        # Album art: if your API exposes something like "cover" or "art"
        art_url = data.get("cover") or data.get("art") or data.get("image") or ""

        # Live DJ indicator: if API has a "status" or "source" field
        status = str(data.get("status", "")).lower()
        source = str(data.get("source", "")).lower()
        is_live = "live" in status or "dj" in status or "live" in source

        return {
            "title": title,
            "artist": artist,
            "listeners": listeners,
            "art_url": art_url,
            "is_live": is_live,
        }
    except Exception:
        return {
            "title": "Live Stream",
            "artist": "",
            "listeners": 0,
            "art_url": "",
            "is_live": False,
        }

@app.route("/api/nowplaying")
def api_nowplaying():
    return jsonify(fetch_now_playing())

@app.route("/")
def index():
    return render_template(
        "index.html",
        station_name="Your Station Name",
        tagline="24/7 curated sounds.",
        stream_url=STREAM_URL,
        schedule=SCHEDULE,
        current_show=get_current_show(),
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)

