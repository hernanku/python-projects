from flask import Flask
from flask import render_template
from flask import request
import feedparser

app = Flask(__name__)

rss_feed = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}



@app.route('/')
def get_news(publication="bbc"):
    query = request.args.get('publication')
    if not query or query.lower() not in rss_feed:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(rss_feed[publication])
    return render_template('home.html', articles=feed['entries'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

