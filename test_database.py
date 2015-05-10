import json
import os
import database

__author__ = 'flshrmb'

import unittest


class MyTestCase(unittest.TestCase):
    conn = None
    def setUp(self):
        try:
            os.remove('test.db')
        except OSError, e:
            pass
        self.conn = database.get_con('test.db')
        database.create_table(self.conn.cursor())

    def tearDown(self):
        self.conn.close()

    def test_get_con(self):
        self.assertIsNotNone(self.conn)

    def test_create_table(self):
        database.create_table(self.conn.cursor())

    def test_is_in_db(self):
        cursor = self.conn.cursor()
        database.insert(1,{'score': 30}, cursor)
        self.assertTrue(database.is_in_db(1, cursor))
        self.assertFalse(database.is_in_db(2, cursor))

    def test_get_top_ten(self):
        database.insert(2,{'score': 30}, self.conn.cursor())
        database.insert(1,{'score': 30}, self.conn.cursor())
        top_ten = database.get_top_ten(self.conn.cursor())
        self.assertTrue(len(top_ten) == 2)
        for entry in top_ten:
            json_data = json.loads(entry[2])
            self.assertEquals(json_data['score'], 30)




if __name__ == '__main__':
    unittest.main()
