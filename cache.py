# This file mimics the Cache for our database that we will be building

# For now, we will restrict this to a simple dictionary
# In production this can be a redis DB or something

# Since our data is fairly structured, we will be storing the search query as the key and a list of
# article IDs as the value/result to be returned.

article_cache = {}


def cache_check(query):
    global article_cache
    if query in article_cache:
        return article_cache[query]
    return None


def cache_add(query, results):
    if query not in article_cache:
        article_cache[query] = results
    return True


def cache_clear():
    global article_cache
    article_cache = {}
    return True
