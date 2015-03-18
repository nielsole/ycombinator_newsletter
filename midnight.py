#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from tinydb import TinyDB
import cgi
from credentials import API_KEY, HOST
__author__ = 'flshrmb'


def send_simple_message(some_list,address):
    return requests.post(
        "https://api.mailgun.net/v2/" + HOST + "/messages",
        auth=("api", API_KEY),
        data={"from": u"Hacker News - Täglicher Report <mailgun" + HOST + ">",
              "to": address,
              "subject": "Hacker News Update",
              "html": u'<html>{0}<br>To be removed from this mailing list please contact nielsole.kuehl@gmail.com</html>'.format(some_list)})

def main():
    db = TinyDB('db.json')
    message = "Top messages:<br>"
    for story in db.all():
        message += u'{0} <a href="{1}">{2}</a><br>'.format(story['score'], story['url'], cgi.escape(story['title']))
    with open('addresses.txt') as f:
        addresses = f.read().splitlines()
    for address in addresses:
        send_simple_message(message, address)
    os.remove('db.json')


if __name__ == "__main__":
    main()
