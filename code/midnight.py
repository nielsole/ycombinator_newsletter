#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import requests
import cgi
from credentials import API_KEY, USER, HOST
import database

__author__ = 'flshrmb'


def send_simple_message(some_list):
    with open('addresses.txt') as f:
        addresses = f.read().splitlines()
    return requests.post(
        "https://api.mailgun.net/v3/" + HOST + "/messages",
        auth=("api", API_KEY),
        data={"from": u'"Hacker News - Daily Report "<{0}@{1}>'.format(USER, HOST),
              "to": u'<{0}@{1}>'.format(USER, HOST),
              "bcc": addresses,
              "subject": "Hacker News Update",
              "html": u'<html>{0}<br>To be removed from this mailing list write an email with the subject \'unsubscribe\' to hackernewsletter-request@freelists.org</html>'.format(some_list)})

def main():
    message = "Top messages:<br>"
    conn = database.get_con()
    cur = conn.cursor()
    top_ten = database.get_top_ten(cur)
    for result in top_ten:
        # Id INTEGER PRIMARY KEY, Score INTEGER, Url VARCHAR, Title VARCHAR, Sent
        number = result[0]
        score = result[1]
        url = result[2]
        title = cgi.escape(result[3])
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
