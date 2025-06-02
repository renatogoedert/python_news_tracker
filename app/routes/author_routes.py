from flask import Blueprint, request, jsonify
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
        )

        #add to db
        db.session.add(new_author)
        db.session.commit()

        return jsonify({'message': 'Author added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}),500
