#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import html

import requests
from credentials import API_KEY
import database

__author__ = 'flshrmb'


def send_simple_message(some_list):
    return requests.post(
        "https://newsletter.niels-ole.com/send",
        headers={"Authorization": "Token {}".format(API_KEY)},
        json={
              "list": 1,
              "subject": "Hacker News Update",
              "html": u'{}'.format(some_list)})

def main():
    message = "Top messages:<br>"
    conn = database.get_con()
    cur = conn.cursor()
    top_ten = database.get_top_ten(cur)
    for result in top_ten:
        # Id INTEGER PRIMARY KEY, Score INTEGER, Url VARCHAR, Title VARCHAR, Sent
        number = html.escape(result[0])
        score = html.escape(result[1])
        url = html.escape(result[2])
        title = html.escape(result[3])
        if url == '':
            link = title
        else:
            link = u'<a href="{0}">{1}</a>'.format(url, title)
        message += u'{0} {1} (<a href="https://news.ycombinator.com/item?id={2}">Comments</a>)<br>'.format(score, link, number)
    result = send_simple_message(message)
    if result.status_code == 200:
        database.was_sent(cur, top_ten)
        database.delete_unsent(cur)
    else:
        raise(Exception("Weird response" + result.text))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()
