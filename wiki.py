from constants import ADVANCED, ADVANCED_TO_QUESTION, BASIC, WIKI_API, ARTICLES, METADATA, TITLE_TO_INFO, KEYWORD_TO_TITLES
import json
import re
import requests

threshold = 5

def _find_keywords(article):
  keywords = []
  count = {}
  final_count = {}

  article = re.sub('\W+',' ', article).split(' ')

  for word in article:
    count[word.lower()] = count[word.lower()] + 1 if word.lower() in count.keys() else 1

  for key, value in count.items():
    if value > threshold and len(key) > 2:
      keywords.append(key)
      final_count[key] = value

  return keywords

def _create_id_to_metadata(info):
  """Creates a dictionary of article ID to title, author, timestamp, num_characters, and list of keywords

  Args:
    info - JSON of information from BigQuery
  """
  id_to_metadata = {}
  id_set = set()
  
  for item in info:
    article_id = item.get('id')
    #if article_id in id_set:
    #  print(article_id)
    id_set.add(article_id)
    # Delete the id from the dict
    del item['id']
  
    #print(article_id)
    # Make a request to Wikipedia
    resp = requests.get(WIKI_API.format(article_id))

    if resp.status_code == 200:
      item['keywords'] = _find_keywords(resp.json().get('query').get('pages')[0].get('extract'))
      id_to_metadata[article_id] = item
  
  return id_to_metadata

def _metadata_list(info):
  """Creates a list of title, author, timestamp, num_characters, and list of keywords

  Args:
    info - JSON of information from BigQuery
  """
  metadata = []
  
  for item in info:
    # Make a request to Wikipedia
    article_id = item.get('id')
    resp = requests.get(WIKI_API.format(article_id))

    if resp.status_code == 200:
      item['keywords'] = _find_keywords(resp.json().get('query').get('pages')[0].get('extract'))
      metadata.append(item)
  
  print(metadata)
  return metadata

def article_titles():
  """ Returns a list of article titles
  """
  return list(map(lambda article: article.get('title'), ARTICLES))

def article_metadata():
  """ Returns a list of article metadata (list of lists)
  """
  return METADATA

def title_to_info_map():
  """ Returns a mapping of article title to metadata mapping
  """
  return TITLE_TO_INFO

def keyword_to_titles_map():
  """ Returns a mapping of keyword to article titles with keyword
  """
  return KEYWORD_TO_TITLES

def _count_for_titles():
  """ Returns titles that have words in other titles
  """
  count = {}
  titles = article_titles()
  for title in titles:
    title_split = title.split(' ')
    for word in title_split:
      count[word] = count[title] + 1 if title in count.keys() else 1

  for key, value in count.items():
    if value > 1:
      print(key)
  return count

def ask_search():
  return input(BASIC)

def ask_advanced_search():
  request = int(input(ADVANCED))
  none = [1, 3, 6]
  answer = input(ADVANCED_TO_QUESTION[request]) if request not in none else ''
  return [request, answer if request != 2 else int(answer)]
