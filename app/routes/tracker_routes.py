from flask import Blueprint, request, jsonify, current_app

tracker_bp = Blueprint('source', __name__)

#post request to set tracker to a url
@tracker_bp.route('/set-source',methods=['POST'])
def set_source():
    """
    Set a URL to tracker 
    ---
    parameters:
      - name: url
        in: query
        type: string
        required: true
    responses:
      200:
        description: Source URL set to {source_url}
      400:
        description: Bad request: missing source url
    """
    try:
        source_url = request.args.get('url')

        if not source_url:
            return 'Bad request: missing source_url', 400

        current_app.config['SOURCE_URL'] = source_url
        return f'Source URL set to {source_url}', 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500