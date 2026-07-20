from flask import Flask, render_template, request
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = os.environ.get("45b362c7ab688d5df868b8b05319f215") or "45b362c7ab688d5df868b8b05319f215"

CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def city_time(unix_time, timezone):
    return datetime.utcfromtimestamp(unix_time + timezone)


@app.route("/", methods=["GET", "POST"])
def home():
    city = "Uyo"

    if request.method == "POST":
        city = request.form.get("city", "").strip() or "Uyo"

    weather = None
    forecast = []
    error = None

    try:
        current = requests.get(
            CURRENT_URL,
            params={
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            },
            timeout=10
        )

        if current.status_code == 200:
            data = current.json()

            weather = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"]),
                "feels_like": round(data["main"]["feels_like"]),
                "temp_min": round(data["main"]["temp_min"]),
                "temp_max": round(data["main"]["temp_max"]),
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind": data["wind"]["speed"],
                "visibility": data.get("visibility", 0) // 1000,
                "clouds": data["clouds"]["all"],
                "description": data["weather"][0]["description"].title(),
                "icon": data["weather"][0]["icon"],
                "date": city_time(data["dt"], data["timezone"]).strftime("%A • %d %B %Y"),
                "sunrise": city_time(data["sys"]["sunrise"], data["timezone"]).strftime("%I:%M %p"),
                "sunset": city_time(data["sys"]["sunset"], data["timezone"]).strftime("%I:%M %p")
            }

            forecast_request = requests.get(
                FORECAST_URL,
                params={
                    "q": city,
                    "appid": API_KEY,
                    "units": "metric"
                },
                timeout=10
            )

            if forecast_request.status_code == 200:
                fdata = forecast_request.json()

                seen = set()
                for item in fdata["list"]:
                    dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    if dt.hour == 12 and dt.date() not in seen:
                        seen.add(dt.date())
                        forecast.append({
                            "day": dt.strftime("%a"),
                            "temp": round(item["main"]["temp"]),
                            "description": item["weather"][0]["main"],
                            "icon": item["weather"][0]["icon"]
                        })
                        if len(forecast) == 5:
                            break
        else:
            error = "City not found. Please check the spelling."

    except requests.RequestException:
        error = "Unable to connect to the weather service."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        error=error
    )


@app.route("/forecast")
def forecast():
    return render_template("forecast.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
