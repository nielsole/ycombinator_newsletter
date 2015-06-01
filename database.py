import json

__author__ = 'flshrmb'

import sqlite3 as lite

def is_in_db(number, cur):
    cur.execute("SELECT * FROM Stories WHERE Id = ?;", (str(number),))
    rows = cur.fetchone()
    if rows is not None:
        return True
    return False

def insert(number, json_data, cur):
    if is_in_db(number, cur):
        cur.execute("UPDATE Stories SET Score = ?, Url = ?, Title = ? WHERE id = ?;", (json_data['score'], json_data['url'], json_data['title'], number ))
    else:
        try:
            url = json_data['url']
        except KeyError:
            url = ''
        try:
            title = json_data['title']
        except KeyError:
            title = ''
        cur.execute("""insert into Stories (Id, Score, Url, Title) values
  (?, ?, ?,? );""", (number, json_data['score'], url, title))
    pass

def create_table(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS Stories(Id INTEGER PRIMARY KEY, Score INTEGER, Url VARCHAR, Title VARCHAR, Sent INTEGER DEFAULT 0);")
    return

def get_top_ten(cur):
    cur.execute("SELECT * FROM Stories WHERE sent = 0 ORDER BY SCORE DESC LIMIT 10;")
    return cur.fetchall()

def was_sent(cur, stories):
    for story in stories:
        cur.execute("UPDATE Stories SET SENT = 1 WHERE Id = ?", (story[0],))

def delete_unsent(cur):
    cur.execute("DELETE FROM Stories WHERE SENT IS 0 ;")

def get_con(dbname='prod.db'):
    return lite.connect(dbname)

    if con:
        con.close()
