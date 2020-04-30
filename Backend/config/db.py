# commandes pour interagrir avec  MA BASE DE DONNES 
#---------------------------------------------------

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_db():
    connect_db()
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def connect_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

def get_db():
    if 'db' not in g:
        connect_db()
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    get_db().commit()
    rv = cur.fetchall()
    # contient l id de la derniere colomne modifiee (gestion des id = -1)
    last_id = cur.lastrowid
    cur.close()
    if rv == []:
        return None, last_id
    if one == True:
        return rv[0], last_id
    return rv, last_id
    # return (rv[0] if rv else None) if one else rv