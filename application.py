import feedparser
from flask import Flask, render_template, request

application = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za.ezproxy.torontopubliclibrary.ca/cmlink/1.640',
             'cbc': 'http://rss.cbc.ca/lineup/topstories.xml',
             'ctv': 'http://ctvnews.ca/rss/TopStories'}


@application.route("/")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "ctv"
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])

    return render_template("home.html", articles=feed['entries'])


if __name__ == '__main__':
    application.run(port=5000, debug=True)