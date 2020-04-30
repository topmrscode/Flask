# Point dentree de mon programme (config et lancement du programme)
#------------------------------


import click
import flask
import os
from flask.cli import with_appcontext
from config.db import init_db, query_db
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'), SECRET_KEY='development key',
    USERNAME='admin ',
    PASSWORD='default '
))
app.config.from_envvar('FLASKR_SETTINGS ', silent=True)

@app.cli.command('init-db')
@with_appcontext
def _init_db_command():
    init_db()
    click.echo('Initialized the database.')

import routes
