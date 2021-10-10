import datetime
import feedparser
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from urllib.request import urlopen
import json
import urllib
import urllib.parse

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
    publication = get_value_with_fallback('publication')
    articles = get_news(publication.lower())

    city = get_value_with_fallback('city')
    weather = get_weather(city)

    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback("currency_to")

    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(
        render_template(
            "home.html",
            articles=articles,
            weather=weather,
            currency_from=currency_from,
            currency_to=currency_to,
            rate=rate,
            currencies=sorted(currencies),
        )
    )
    expires_at = datetime.datetime.now() + datetime.timedelta(days=1)
    response.set_cookie("publication", publication, expires=expires_at)
    response.set_cookie("city", city, expires=expires_at)
    response.set_cookie("currency_from", currency_from, expires=expires_at)
    response.set_cookie("currency_to", currency_to, expires=expires_at)

    return response


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return default_data[key]


def get_news(publication):
    feed = feedparser.parse(rss_feed[publication.lower()])
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
    return (to_rate / frm_rate, parsed_data.keys())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

