# Point dentree de mon programme (config et lancement du programme)
#------------------------------


from flask_session import Session
import flask
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config.from_object(__name__)

# TERMINAL : sert a mentionner que je veux que le front tourne sur le port 3000 a la difference du back qui tourne sur le 5000
# flask run --host=0.0.0.0 --port=3000

from routes import article, comment, session, static, user