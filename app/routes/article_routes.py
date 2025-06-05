from flask import Blueprint, request, jsonify
from newspaper import Article
from app.models.article import ArticleModel
from app.extensions import db
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

article_bp = Blueprint('article_bp', __name__)

#post request to add article, it recives the url and extracts fields using newspaper
@article_bp.route('/add-article', methods=['POST'])
def add_article():
    """
    Add article to DB
    ---
    parameters:
      - name: url
        in: query
        type: string
        required: false
    responses:
      200:
        description: Article already exists
      201:
        description: Article added successfully
      400:
        description: no URL provided
      415:
        description: Unsupported media type
    """
        
    url = request.args.get('url')
    if not url:
        return jsonify({'error':'no URL provided'}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        #check if article exists
        existing_article = ArticleModel.query.filter_by(url=url).first()
        if existing_article:
            return jsonify({'message': 'Article already exists'}), 200
        
        #create a new article instance
        new_article = ArticleModel(
            url=url,
            title=article.title,
            author_id=0,
            published_date=article.publish_date,
            content=article.text,
            keywords=article.keywords,
        )

        #add to db
        db.session.add(new_article)
        db.session.commit()

        return jsonify({'message': 'Article added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}),500

#get all articles
@article_bp.route('/get-all-articles', methods=['GET'])
def get_all_articles():
    """
    Add all articles from DB
    ---
    parameters:
      - name: page
        in: query
        type: int
        required: false
      - name: per_page
        in: query
        type: int
        required: false
    responses:
      200:
        description: List Articles
      415:
        description: Unsupported media type
    """
    try:
        #add pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page',default=10,type=int)

        pagination = ArticleModel.query.paginate(page=page, per_page=per_page, error_out=False)
        articles_list = [{
            'url': article.url,
            'title': article.title,
            'author_id': article.author_id,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'content': article.content,
            'keywords': article.keywords
        } for article in pagination.items]

        return jsonify({
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'articles': articles_list
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#get article by id
@article_bp.route('/get-article', methods=['GET'])
def get_article():
    """
    Get an article by ID or URL (at least one required)
    ---
    parameters:
      - name: id
        in: query
        type: integer
        required: false
      - name: url
        in: query
        type: string
        required: false
    responses:
      200:
        description: Article found
      400:
        description: no ID or URL provided
      404:
        description: Article not found
      415:
        description: Unsupported media type
    """
    article_id = request.args.get('id')
    url = request.args.get('url')

    if not url and not article_id:
        return jsonify({'error': ' no ID or URL provided'}), 400 

    try:
        if article_id:
            article = ArticleModel.query.get(article_id)
        else:
            article = ArticleModel.query.filter_by(url=url).first()

        if not article:
            return jsonify({'error': 'Article not found'}), 404

        return jsonify({
            'id': article.id,
            'url': article.url,
            'title': article.title,
            'author_id': article.author_id,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'content': article.content,
            'keywords': article.keywords
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#get last article
@article_bp.route('/get-latest-article', methods=['GET'])
def get_lastest_article():
    """
    Get latest article
    ---
    responses:
      200:
        description: Article found
      404:
        description: Article not found
      415:
        description: Unsupported media type
    """
    try:
        article = ArticleModel.query.order_by(ArticleModel.created_at.desc()).first()

        if not article:
            return jsonify({'error':'No Article found'}), 404

        return jsonify({
            'id': article.id,
            'url': article.url,
            'title': article.title,
            'author_id': article.author_id,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'content': article.content,
            'keywords': article.keywords
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}),500