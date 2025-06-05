from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.models.author import AuthorModel
from app.extensions import db
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

author_bp = Blueprint('author_bp', __name__)

#post request to add author, it recives the url and extracts fields using newspaper
@author_bp.route('/add-author', methods=['POST'])
def add_author():
    """
    Add author to DB
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
    responses:
      200:
        description: Author already exists
      201:
        description: Author added successfully
      400:
        description: no Name provided
      415:
        description: Unsupported media type
    """
        
    name = request.args.get('name')
    if not name:
        return jsonify({'error':'no Name provided'}), 400

    try:
        #check if author exists
        existing_author = AuthorModel.query.filter_by(name=name).first()
        if existing_author:
            return jsonify({'message': 'Author already exists'}), 200
        
        #create a new author instance
        new_author = AuthorModel(
            name=name,
            articles=[],
        )

        #add to db
        db.session.add(new_author)
        db.session.commit()

        return jsonify({'message': 'Author added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}),500

#get request to get all authors    
@author_bp.route('/get-all-authors', methods=['GET'])
def get_all_authors():
    """
    Retrieve all authors from the database.
    ---
    responses:
      200:
        description: A list of authors
    """
    authors = AuthorModel.query.all()
    authors_data = [
        {
            'id': author.id,
            'name': author.name,
            'articles': author.articles,
            'created_at': author.created_at.isoformat(),
            'updated_at': author.updated_at.isoformat()
        }
        for author in authors
    ]
    return jsonify(authors_data), 200

#get author from id
@author_bp.route('/get-author', methods=['GET'])
def get_author_by_id():
    """
    Retrieve an author by ID.
    ---
    parameters:
      - name: author_id
        in: query
        type: integer
        required: true
    responses:
      200:
        description: Author found
      400:
        description: no ID provided
      404:
        description: Author not found
    """

    author_id = request.args.get('id')

    if not author_id:
        return jsonify({'error': ' no ID provided'}), 400
     
    author = AuthorModel.query.get(author_id)
    if author:
        author_data = {
            'id': author.id,
            'name': author.name,
            'articles': author.articles,
            'created_at': author.created_at.isoformat(),
            'updated_at': author.updated_at.isoformat()
        }
        return jsonify(author_data), 200
    else:
        return jsonify({'error': 'Author not found'}), 404
    
#get author id
@author_bp.route('/get-author-id', methods=['GET'])
def get_author_id():
    """
    Retrieve an author ID.
    ---
    parameters:
      - name: author
        in: query
        type: string
        required: true
    responses:
      200:
        description: Author found
      400:
        description: no Name provided
      404:
        description: Author not found
    """

    author_name = request.args.get('name')

    if not author_name:
        return jsonify({'error': ' no Name provided'}), 400
     
    author = AuthorModel.query.filter(func.lower(AuthorModel.name)==author_name.lower()).first()
    if author:
        author_data =  author.id,
        return jsonify(author_data), 200
    else:
        return jsonify({'error': 'Author not found'}), 404