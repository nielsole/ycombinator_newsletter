#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from tinydb import TinyDB
import cgi
from credentials import API_KEY, USER, HOST
__author__ = 'flshrmb'


def send_simple_message(some_list):
    with open('addresses.txt') as f:
        addresses = f.read().splitlines()
    return requests.post(
        "https://api.mailgun.net/v3/" + HOST + "/messages",
        auth=("api", API_KEY),
        data={"from": u"Hacker News - Täglicher Report <{0}@{1}>".format(USER, HOST),
              "to": addresses,
              "subject": "Hacker News Update",
              "html": u'<html>{0}<br>To be removed from this mailing list write an email with the subject \'unsubscribe\' to hackernewsletter-request@freelists.org</html>'.format(some_list)})

def main():
    db = TinyDB('db.json')
    message = "Top messages:<br>"
    for story in db.all():
        message += u'{0} <a href="{1}">{2}</a> (<a href="https://news.ycombinator.com/item?id={3}">Comments</a>)<br>'.format(story['score'], story['url'], cgi.escape(story['title']), story['id'])
    result = send_simple_message(message)
    os.remove('db.json')


if __name__ == "__main__":
    main()
