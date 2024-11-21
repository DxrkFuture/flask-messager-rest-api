import requests
from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify

bp = Blueprint('search_gif', __name__)  # Blueprint for the route

def search_gifs_on_tenor(query):
    url = f"https://tenor.com/ru/search/{query}-gifs"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    gifs = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and 'media.tenor.com' in src:
            gifs.append(src)

    return gifs[:40]  # Return the first 10 results

# пример http://127.0.0.1:5000/search_gif?query=кошка
@bp.route('/search_gif', methods=['GET'])  # Route for search requests
def search_gif():
    query = request.args.get('query')  # Access query parameter from the request

    if not query:
        # Handle missing query parameter (optional)
        return jsonify({'error': 'Missing query parameter'}), 400

    results = search_gifs_on_tenor(query)
    return jsonify({'results': results}), 200