# This module mimics an interface to a high performance noSQL database
# For now we just store test data in a json file and load it.

import json
import os

isDataLoaded = False
article_data = {}
database_path = 'test/resources/articles.json'
dataAttributes = []


def load_data():
    global isDataLoaded
    global article_data
    if os.path.exists(database_path):
        article_data = json.load(open(database_path))
    else:
        raise Exception('Database file is missing.')
    isDataLoaded = True


def get_data():
    if not isDataLoaded:
        load_data()
    return article_data


def fetch_by_id(identifier):
    try:
        return [a for a in article_data if a['id'] == identifier]
    except KeyError:
        return [{'Error': 'Invalid Id'}]


def fetch_by_attribute(attr, value):
    results = []
    for art in article_data:
        if attr in art and art[attr] == value:
            results.append(art)
    return results


def get_data_attributes():
    global dataAttributes

    # Memoization for subsequent loads
    if dataAttributes:
        return dataAttributes

    for art in article_data:
        for key in art:
            if key not in dataAttributes:
                dataAttributes.append(key)
    return dataAttributes
