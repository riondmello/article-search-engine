import re
from sys import argv
from cache import cache_check, cache_add
from database import get_data, fetch_by_id

skip_words = ['a', 'an', 'and', 'the', 'is', 'are']

# For now, we keep this as a simple dict - later expand using regex or a database in itself.
typo_dict = {'article': ['article', 'articel', 'articl', 'srticle', ]}

isIndexBuilt = False


def article_search(input_query=''):
    """
    :param input_query: The input query. A list of words forming the search query
    :return: A list of articles from database most relavent to the search. Empty list if no matches.
    """
    result = []

    cleaned_query = clean_query(input_query)

    quick_result = cache_check(cleaned_query)
    if quick_result:
        return quick_result


    # We've performed a new search. Add this to Cache for future use
    cache_add(query, result)

    return result


def clean_query(input_query):
    """
    This function cleans the query off english article words that are irrelevant to search
    :param input_query: raw query text
    :return: Cleaned query test
    """
    query = input_query.strip()
    lower_query = query.lower()
    re.sub('|'.join(skip_words), '', lower_query)
    return lower_query


def build_results(query):
    query_words = query.split(' ')
    results_from_index = []
    for i, word in enumerate(query_words):
        if i == 0 and word in typo_dict('article'):
            # Requirement # 1
            return direct_fetch(query_words[1])

        results_from_index.append(search_index(word))

    return rank_results(query_words, results_from_index)


def search_index(word):
    """
    Search the index that we have built
    :param word:
    :return: A list of article Id's matching the word
    """
    if not isIndexBuilt:
        build_index(get_data())

    return []


def build_index(data):
    """
    parse each word in our data and build a reverse index of articles corresponding to each no-skip word in the data.
    :param data:
    :return:
    """
    global isIndexBuilt

    # We try to create a TF-IDF (term frequency inverse document frequency) index here

    isIndexBuilt = True


def rank_results(query_words, results_from_index):
    """
    Aggregate and rank the search results for each word in the query
    :param query_words:
    :param results_from_index:
    :return:
    """

    return []


def direct_fetch(article_id):
    """
    Requirement # 1 : Fetch an article by its identifier
    :param article_id:
    :return:
    """
    return fetch_by_id(article_id)


if __name__ == "__main__":
    query = ' '.join(argv)
    print("Searching for query: {}".format(query))
    results = article_search(query)
    if results:
        for result in results:
            print(result)
    else:
        print('No results found.')
