#!/usr/bin/env python
import requests
from database import is_in_db
import database

__author__ = 'flshrmb'

def handle(some_story, conn):
    cursor = conn.cursor()
    database.create_table(cursor)
    database.insert(some_story['id'], some_story, cursor)
    conn.commit()


def main():
    top_list = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json')
    if top_list.status_code != 200:
        return # Maybe add exception?
    top_json = top_list.json()
    conn = database.get_con()
    for i, id in enumerate(top_json):
        story_request = requests.get('https://hacker-news.firebaseio.com/v0/item/{0}.json'.format(id))
        if story_request.status_code != 200:
            continue
        handle(story_request.json(), conn)
        print('Number: {0}'.format(i))
        if i > 30:
            break


if __name__ == "__main__":
    main()
