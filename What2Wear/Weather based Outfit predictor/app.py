import requests
from flask import Flask, render_template, request
import utils

app = Flask(__name__)

def get_location_city():
    """Fetch user's city from IP (fallback to 'London' if fails)."""
    try:
        res = requests.get("https://ipinfo.io/json")
        if res.status_code == 200:
            data = res.json()
            return data.get("city", "London")
    except:
        return "London"

@app.route("/", methods=["GET", "POST"])
def index():
    outfit = None
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")
        if not city:  # if user didn’t enter a city, auto-detect
            city = get_location_city()
        weather_data = utils.get_weather(city)
        if weather_data:
            outfit = utils.get_outfit_suggestion(weather_data)

    return render_template("index.html", outfit=outfit, weather=weather_data)


# 👇 Add this so Flask actually runs
if __name__ == "__main__":
    app.run(debug=True)
