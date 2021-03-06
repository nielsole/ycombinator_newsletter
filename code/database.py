
__author__ = 'flshrmb'

import sqlite3 as lite

def is_in_db(number, cur):
    cur.execute("SELECT * FROM Stories WHERE Id = ?;", (str(number),))
    rows = cur.fetchone()
    if rows is not None:
        return True
    return False

def insert(json_data, cur):
    try:
        url = json_data['url']
    except KeyError:
        url = "https://news.ycombinator.com/item?id={0}".format(json_data["id"])
    try:
        title = json_data['title']
    except KeyError:
        title = '[No title provided]'
    if is_in_db(json_data["id"], cur):
        cur.execute("UPDATE Stories SET Score = ?, Url = ?, Title = ? WHERE id = ?;", (json_data['score'], url, title, json_data["id"] ))
    else:
        cur.execute("""insert into Stories (Id, Score, Url, Title) values
  (?, ?, ?,? );""", (json_data["id"], json_data['score'], url, title))
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

def get_con(dbname='/data/prod.db'):
    return lite.connect(dbname)

    if con:
        con.close()
