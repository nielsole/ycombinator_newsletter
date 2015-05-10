import json

__author__ = 'flshrmb'

import sqlite3 as lite

def is_in_db(number, con):
    cur = con.cursor()
    cur.execute("SELECT * FROM Stories WHERE Id = ?;", (str(number)))
    rows = cur.fetchone()
    if rows is not None:
        return True
    return False

def insert(number, json_data, cur):
    cur.execute("""insert or replace into Stories (Id, Json, Score, Sent) values
  (?, ?, ?,?);""", (number, json.dumps(json_data), json_data['score'], 0))
    pass

def create_table(cur):
    cur.execute("CREATE TABLE IF NOT EXISTS Stories(Id INTEGER PRIMARY KEY, Score INTEGER, Json BLOB, Sent INTEGER );")
    return

def get_top_ten(cur):
    cur.execute("SELECT * FROM Stories WHERE SENT IS 0 ORDER BY SCORE DESC LIMIT 10;")
    return cur.fetchall()

def was_sent(cur, stories):
    for story in stories:
        cur.execute("UPDATE Stories SET SENT = 1 WHERE Id = {0}".format(story[0]))

def delete_unsent(cur):
    cur.execute("DELETE FROM Stories WHERE SENT IS 0 ;")

def get_con(dbname='prod.db'):
    return lite.connect(dbname)

    if con:
        con.close()