from flask import Flask
from flask import render_template
from flask import request
import feedparser
import json
import urllib
import urllib.parse
from urllib.request import urlopen

# import requests


app = Flask(__name__)

default_data = {
    "publication": "bbc",
    "city": "London",
    "currency_from": "GBP",
    "currency_to": "USD",
}
weather_api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3272e848e3884ad703c6b9763f15c6ce"
currency_api_url = "https://openexchangerates.org//api/latest.json?app_id=626fb5b702c240cda0db4a1c33c35dba"
rss_feed = {
    "bbc": "http://feeds.bbci.co.uk/news/rss.xml",
    "cnn": "http://rss.cnn.com/rss/edition.rss",
    "fox": "http://feeds.foxnews.com/foxnews/latest",
    "iol": "http://www.iol.co.za/cmlink/1.640",
}


@app.route("/")
def home():
    publication = request.args.get("publication")
    if not publication:
        publication = default_data["publication"]
    articles = get_news(publication)

    city = request.args.get("city")
    if not city:
        city = default_data["city"]
    weather = get_weather(city)

    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = default_data["currency_from"]
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = default_data["currency_to"]
    rate = get_rate(currency_from, currency_to)

    return render_template(
        "home.html",
        articles=articles,
        weather=weather,
        currency_from=currency_from,
        currency_to=currency_to,
        rate=rate,
    )


def get_news(publication):
    feed = feedparser.parse(rss_feed[publication])
    return feed["entries"]


def get_weather(query):
    query = urllib.parse.quote_plus(query)
    url = weather_api_url.format(query)
    data = urlopen(url).read()
    parsed_data = json.loads(data)
    weather = None
    if parsed_data.get("weather"):
        weather = {
            "description": parsed_data["weather"][0]["description"],
            "temperature": parsed_data["main"]["temp"],
            "city": parsed_data["name"],
            "country": parsed_data["sys"]["country"],
        }
    return weather


def get_rate(frm, to):
    all_currency = urlopen(currency_api_url).read()
    parsed_data = json.loads(all_currency).get("rates")
    frm_rate = parsed_data.get(frm.upper())
    to_rate = parsed_data.get(to.upper())
    return to_rate / frm_rate


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
