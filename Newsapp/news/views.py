import feedparser
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpRequest

# RSS Feeds
RSS_FEEDS = {
    'Yahoo Finance': 'https://finance.yahoo.com/news/rssindex',
    'Hacker News': 'https://news.ycombinator.com/rss',
    'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'
}

def index(request: HttpRequest):
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)

    # Sort articles by publication date
    articles = sorted(articles, key=lambda x: x[1].published_parsed, reverse=True)

    # Paginate articles
    paginator = Paginator(articles, 10)  # 10 articles per page
    page_number = request.GET.get('page')
    paginated_articles = paginator.get_page(page_number)

    return render(request, 'home.html', {
        'articles': paginated_articles,
        'page': page_number,
        'total_pages': paginator.num_pages,
    })

def search(request: HttpRequest):
    query = request.GET.get('q', '')

    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [(source, entry) for entry in parsed_feed.entries]
        articles.extend(entries)

    # Filter articles based on search query
    results = [article for article in articles if query.lower() in article[1].title.lower()]

    return render(request, 'search.html', {
        'articles': results,
        'query': query,
    })
