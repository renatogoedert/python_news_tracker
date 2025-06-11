import feedparser
from datetime import datetime, timezone
from flask import current_app
from dateutil.parser import parse
from newspaper import Article
from sqlalchemy import func

from app.extensions import db
from app.models.article import ArticleModel
from app.models.author import AuthorModel


def add_news_from_rss(app_context):
    print("testing")
    """
    Parses a RSS url, extracts full content using newspaper3k,
    and adds new articles to the database.
    """
    with app_context:
        rss_url = current_app.config.get('SOURCE_URL')
        print(f"[{datetime.now()}] Checking URL RSS feed...")
        feed = feedparser.parse(rss_url)

        if feed.bozo:
            print(f"Warning: RSS feed issues for {rss_url}: {feed.bozo_exception}")

        for entry in feed.entries:
            try:
                url = entry.link
                # Check if article already exists by URL
                existing_article = ArticleModel.query.filter_by(url=url).first()
                if existing_article:
                    print(f"Article already exists: {url}")
                    continue  

                article = Article(url)
                try:
                    article.download()
                    article.parse()
                    article.nlp() 
                except Exception as e:
                    print(f"Error downloading or parsing article {url}: {e}")
                    continue  

                # Extract author
                author_name = article.authors[0] if article.authors else None
                author = None
                if author_name:
                    author = AuthorModel.query.filter(func.lower(AuthorModel.name) == author_name.lower()).first()
                    if not author:
                        author = AuthorModel(name=author_name)
                        db.session.add(author)
                        db.session.flush()

                published_date = None
                if hasattr(entry, 'published'):
                    try:
                        dt_object_with_tz = parse(entry.published)
                        published_date = dt_object_with_tz.astimezone(timezone.utc)
                    except Exception as e:
                        print(f"Could not parse pubDate '{entry.published}': {e}")
                elif hasattr(entry, 'published_parsed'):
                    published_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

                new_article = ArticleModel(
                    url=url,
                    title=article.title,
                    author_id=author.id if author else None,
                    published_date=published_date,
                    content=article.text,
                    keywords=article.keywords, 
                )
                db.session.add(new_article)
                print(f"Added new article: {new_article.title}")

            except Exception as e:
                db.session.rollback()
                print(f"Error processing RSS entry: {e}")
                print(f"Entry data: URL='{entry.link}', Title='{entry.title}'")

        try:
            db.session.commit()
            print(f"[{datetime.now()}] Database updated with RSS feed entries.")
        except Exception as e:
            db.session.rollback()
            print(f"[{datetime.now()}] Database commit failed: {e}")
        finally:
            db.session.close()