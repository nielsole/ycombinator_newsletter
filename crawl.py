#!/usr/bin/env python
import requests
from tinydb import TinyDB, where

__author__ = 'flshrmb'

def is_in_db(some_id):
    db = TinyDB('db.json')
    results = db.search((where('id') == some_id))
    return len(results) != 0

def handle(some_story):
    db = TinyDB('db.json')
    if is_in_db(some_story['id']):
        db.update(some_story, where('id') == some_story['id'])
    else:
        to_be_replaced = None
        for element in db.all():
            if some_story['score'] > element['score']:
                try:
                    if element['score'] < to_be_replaced['score']:
                        to_be_replaced = element
                except TypeError:
                    to_be_replaced = element
        if len(db.all()) < 10:
            db.insert(some_story)
        elif to_be_replaced is not None:
            db.remove((where('id') == to_be_replaced['id']))
            db.insert(some_story)


def main():
    top_list = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    if top_list.status_code != 200:
        return # Maybe add exception?
    top_json = top_list.json()
    for i, id in enumerate(top_json):
        story_request = requests.get('https://hacker-news.firebaseio.com/v0/item/{0}.json'.format(id))
        if story_request.status_code != 200:
            continue
        handle(story_request.json())
        print('Number: {0}'.format(i))
        if i > 30:
            break
    #pprint(TinyDB('db.json').all())


if __name__ == "__main__":
    main()
