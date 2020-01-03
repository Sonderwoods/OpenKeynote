#!/usr/bin/env python
# encoding: utf-8

# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019-2020

import sqlite3

"""
HIGHLY inspired, if not copied, from Ardit Sulces MEGA 10 PYTHON SCRIPTS COURSE
"""

DB_NAME = "keynotes_database"

class DatabaseHandler():
    """
    Class to handle file loading and saving
    """
    def __init__(self, path=None, prebackup=True):
        self.path = path
        self.itemlist = []

    def connect(self, path, current_itemlist):
        self.DB_FILE = path
        print(f"attempted to create table on {self.DB_FILE}")
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS keynotes_database (\
        id INTEGER PRIMARY KEY, title STRING, keynote STRING UNIQUE, long_description TEXT,\
        short_description TEXT, entreprise STRING, category STRING)")
        conn.commit()
        conn.close()
        self.update_database(current_itemlist)

    def update_database(self, itemlist):
        for item in itemlist:
            title = item['name']
            keynote = item['content']
            if len(title)>0:
                if len(self.lookup_keynote(title=title))==0:
                    self.insert(title=title, keynote=keynote)
                    print(f"added {title} to the database")
                else:
                    self.update_title_keynote(title, keynote)
        print("updated in the database..")


    def insert(self, title="", keynote="", long_description="", \
        short_description="", entreprise="",category=""):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("INSERT INTO keynotes_database VALUES (NULL,?,?,?,?,?,?)",\
        (title,keynote, long_description, short_description, entreprise,category))
        conn.commit()
        conn.close()

    def rename_item(self, oldname=None, newname=None):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("UPDATE keynotes_database SET keynote=? WHERE keynote=?",
        (newname, oldname))
        conn.commit()
        conn.close()
        print(f"database changed keynote {oldname} to {newname}")

    def view(self):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("SELECT * FROM keynotes_database")
        rows=cur.fetchall()
        conn.close()
        return rows

    def lookup_keynote(self, title="", entreprise="", category=""):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        if len(entreprise)>0 and len(category)>0:
            cur.execute("SELECT * FROM keynotes_database WHERE title=? \
            AND entreprise=? AND category=?", (title,entreprise,category))
        elif len(entreprise)>0:
            cur.execute("SELECT * FROM keynotes_database WHERE title=? \
            AND entreprise=?", (title,entreprise))
        elif len(category)>0:
            cur.execute("SELECT * FROM keynotes_database WHERE title=? \
            AND category=?", (title,category))
        else:
            cur.execute("SELECT * FROM keynotes_database WHERE title=?",(title,))
        rows=cur.fetchall()
        conn.close()
        return rows

    def search(self, title="23r3f3",keynote="awdd3g", short_description="awggr",
    long_description="adwopdk", entreprise="a2d2ag",category="g4wgf3f"):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("SELECT * FROM keynotes_database WHERE title=? OR keynote=?\
         OR entreprise=? OR category=?", (title,keynote,entreprise,category))
        rows=cur.fetchall()
        conn.close()
        return rows

    def delete(self, title):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("DELETE FROM keynotes_database WHERE title=?",(id,))
        conn.commit()
        conn.close()

    def update_title_keynote(self, title, keynote):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("UPDATE keynotes_database SET keynote=? WHERE title=?",
        (keynote, title))
        conn.commit()
        conn.close()

    def update(self, id,title,keynote,short_description,long_description,entreprise,category):
        conn=sqlite3.connect(self.DB_FILE)
        cur=conn.cursor()
        cur.execute("UPDATE keynotes_database SET title=?, keynote=?,\
        short_description=?, long_description=?, entreprise=?, category=? \
        WHERE id=?",
        (title,keynote, short_description, long_description,entreprise,category,id))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    from main import main
    main()
