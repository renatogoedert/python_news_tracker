from flask import Flask, request, jsonify
from newspaper import Article

app = Flask(__name__)

@app.route('/get-title', methods=['POST'])
def get_title():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try: 
        article = Article(url)
        article.download()
        article.parse()
        return jsonify({'title': article.title})
    except Exception as e:
        return ({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)