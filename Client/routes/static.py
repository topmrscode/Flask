from app import app
from flask import render_template, request, redirect, flash, session
import json
import requests
from routes import article, comment, static, user
from routes import session as sess

# ROUTES RELATED TO HOME 
@app.route('/')
def home():
    """Render website's home page."""
    # recuperer le user stocker dans session
    usr = session.get('user')
    return render_template("index.html", user = usr)

# ROUTES RELATED TO LOGIN FORM
@app.route('/login/', methods=['GET'])
def login_form():
    """Render website's login page."""
    return render_template("login.html")

# ROUTES RELATED TO REGISTER
@app.route('/register/', methods=['GET'])
def register_form():
    """Render website's register page."""
    return render_template("register.html")

# ROUTES RELATED TO ERROR 404 
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
