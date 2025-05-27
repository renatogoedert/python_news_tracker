from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from newspaper import Article

from model.article import ArticleModel, db

#initialize flask
app = Flask(__name__)

#set up db
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_username:admin_password@localhost:5432/news_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize db
db.init_app(app)

#create tables if they don't exist
with app.app_context():
    db.create_all()

#post request to add article, it recives the url and extracts fields using newspaper
@app.route('/add-article', methods=['POST'])
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
@app.route('/get-all-articles', methods=['GET'])
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

#runs flask app
if __name__ == '__main__':
    app.run(debug=True)