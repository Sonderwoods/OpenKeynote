#!/usr/bin/env python
# encoding: utf-8

# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019-2020

import sqlite3

"""
HIGHLY inspired, if not copied, from Ardit Sulces MEGA 10 PYTHON SCRIPTS COURSE
"""

DB_FILE = "description_database.db"
DB_NAME = "keynotes_database"

def connect():
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS keynotes_database (id INTEGER PRIMARY KEY, title text, keynote text, entreprise text, category text)")
    conn.commit()
    conn.close()


def insert(title="",keynote="",entreprise="",category=""):
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("INSERT INTO keynotes_database VALUES (NULL,?,?,?,?)",(title,keynote,entreprise,category))
    conn.commit()
    conn.close()
    view()

def view():
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("SELECT * FROM keynotes_database")
    rows=cur.fetchall()
    conn.close()
    return rows

def lookup_keynote(keynote="", entreprise="", category=""):
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    if len(entreprise)>0 and len(category)>0:
        cur.execute("SELECT * FROM keynotes_database WHERE keynote=? AND entreprise=? AND category=?", (keynote,entreprise,category))
    elif len(entreprise)>0:
        cur.execute("SELECT * FROM keynotes_database WHERE keynote=? AND entreprise=?", (keynote,entreprise))
    elif len(category)>0:
        cur.execute("SELECT * FROM keynotes_database WHERE keynote=? AND category=?", (keynote,category))
    else:
        cur.execute("SELECT * FROM keynotes_database WHERE keynote=?", (keynote))
    rows=cur.fetchall()
    conn.close()
    return rows

def search(title="23r3f3",keynote="awdd3g",entreprise="a2d2ag",category="g4wgf3f"):
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("SELECT * FROM keynotes_database WHERE title=? OR keynote=? OR entreprise=? OR category=?", (title,keynote,entreprise,category))
    rows=cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("DELETE FROM keynotes_database WHERE id=?",(id,))
    conn.commit()
    conn.close()

def update(id,title,keynote,entreprise,category):
    conn=sqlite3.connect(DB_FILE)
    cur=conn.cursor()
    cur.execute("UPDATE keynotes_database SET title=?, keynote=?, entreprise=?, category=? WHERE id=?",(title,keynote,entreprise,category,id))
    conn.commit()
    conn.close()

connect()
#insert("The Sun","John Smith",1918,913123132)
#delete(3)
#update(4,"The moon","John Smooth",1917,99999)
#print(view())
#print(search(author="John Smooth"))
