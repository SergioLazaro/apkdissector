__author__ = 'sergio'

import sqlite3, os

class hashesDB:

    def __init__(self, path):
        self.path = path
        self.database = None

    def create(self):
        self.path = self.path + "hashes.db"
        self.connect()

    def connect(self):
        if os.path.isfile(self.path):
            self.database = sqlite3.connect(self.path)
        else:
            print "[!!] Database path is not a sqlite database. Exiting..."
            exit(1)

    def close(self):
        if self.database is not None:
            self.database.close()

    def execute_query(self, query):
        self.database.execute(query)
        self.database.commit()

    def create_cursor(self, query):
        cursor = self.database.cursor()
        cursor.execute(query)

        return cursor.fetchall()

