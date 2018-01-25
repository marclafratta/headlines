import feedparser
import json
from urllib.request import urlopen
import urllib
from flask import Flask, render_template, request

application = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za.ezproxy.torontopubliclibrary.ca/cmlink/1.640',
             'cbc': 'http://rss.cbc.ca/lineup/topstories.xml',
             'ctv': 'http://ctvnews.ca/rss/TopStories',
             'torstar': 'http://www.thestar.com/feeds.topstories.rss'}

DEFAULTS = {'publication': 'ctv',
            'city': 'Toronto'}

@application.route("/")
def get_news():
    # get custom publication or default
    publication = request.args.get('publication')
    if not publication or publication.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = publication.lower()

    articles = get_news(publication)

    # get customized weather based on user input or default
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']

    weather = get_weather(city)

    return render_template("home.html", articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=35a35cfa5c2355830abde9fe2c1896d0"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],"temperature":parsed["main"]["temp"],"city":parsed["name"]
                  }
    return weather


if __name__ == '__main__':
    application.run(port=5000, debug=True)
