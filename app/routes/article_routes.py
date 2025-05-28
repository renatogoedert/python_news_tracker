from flask import Blueprint, request, jsonify
from newspaper import Article
from app.models.article import ArticleModel
from app.extensions import db

article_bp = Blueprint('article_bp', __name__)

#post request to add article, it recives the url and extracts fields using newspaper
@article_bp.route('/add-article', methods=['POST'])
def add_article():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error':'no URL provided'}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()

        #check if article exists
        existing_article = ArticleModel.query.filter_by(url=url).first()
        if existing_article:
            return jsonify({'message': 'Article already exists'}), 200
        
        #create a new article instance
        new_article = ArticleModel(
            url=url,
            title=article.title,
            author=article.authors[0] if article.authors else None,
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
    try:
        #add pagination
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page',default=10,type=int)

        pagination = ArticleModel.query.paginate(page=page, per_page=per_page, error_out=False)
        articles_list = [{
            'url': article.url,
            'title': article.title,
            'author': article.author,
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
            'author': article.author,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'content': article.content,
            'keywords': article.keywords
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#get last article
@article_bp.route('/get-latest-article', methods=['GET'])
def get_lastest_article():
    try:
        article = ArticleModel.query.order_by(ArticleModel.published_date.desc()).first()

        if not article:
            return jsonify({'error':'No Article found'}), 404

        return jsonify({
            'id': article.id,
            'url': article.url,
            'title': article.title,
            'author': article.author,
            'published_date': article.published_date.isoformat() if article.published_date else None,
            'content': article.content,
            'keywords': article.keywords
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}),500