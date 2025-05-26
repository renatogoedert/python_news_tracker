class ArticleModel(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    published_date = db.Column(db.DateTime)
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    source = db.Column(db.String)
    category = db.Column(db.String)
    keywords = db.Column(db.ARRAY(db.String))
    language = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, url, title, author=None, published_date=None, summary=None, content=None, source=None, category=None, keywords=None, language=None):
        self.url = url
        self.title = title
        self.author = author
        self.published_date = published_date
        self.summary = summary
        self.content = content
        self.source = source
        self.category = category
        self.keywords = keywords
        self.language = language
