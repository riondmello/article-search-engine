# This module contains the service that provides api end-points to our search engine

from flask import request, Flask, jsonify
from flask_restful import Resource, Api, reqparse
import database as db
from search import article_search
from database import fetch_by_id, fetch_by_attribute, get_data_attributes

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)


class Search(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('query', required=True)
        parser.add_argument('id', required=False)
        for attr in get_data_attributes():
            parser.add_argument(attr, required=False)

        args = parser.parse_args()  # parse arguments to dictionary
        results = []

        if 'id' in args:
            # return jsonify(fetch_by_id(args['id'])), 200
            results.append(fetch_by_id(args['id']))

        for attr in get_data_attributes():
            if attr in args:
                results.append(fetch_by_attribute(attr, args[attr]))

        if results:
            return jsonify(results), 200
        else:
            return jsonify(article_search(args['query'])), 200


api.add_resource(Search, '/search')


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Article Search Engine</h1>
<p>Please use onr of the following APIs endpoints to use this service:-<br>
1) /articles
2) /article-attributes
3) /search/query=?&lttext&gt</p>'''


@app.route('/api/v1/article-attributes', methods=['GET', 'POST'])
def api_attribute():
    for attr in request.args:
        if attr in db.get_data_attributes():
            return db.fetch_by_attribute(attr)
    return "Error: Attribute not present in data"


@app.route('/api/v1/articles', methods=['GET', 'POST'])
def api_id():
    # Check if id was present in the input parameters of the GET request
    if 'id' in request.args:
        art_id = request.args['id']
    else:
        return "Error: Article id field not present in the request."

    return db.fetch_by_id(art_id)


# @app.route('/api/v1/search', methods=['POST'])
# def api_search():
#     # Check if id was present in the input parameters of the GET request
#
#
#     return article_search(art_id)


if __name__ == "__main__":
    if not db.isDataLoaded:
        db.load_data()
    app.run()
