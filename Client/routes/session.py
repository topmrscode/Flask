from app import app
from flask import render_template, request, redirect, flash, session
import json
import requests
@app.route('/login/', methods=['POST'])
def login():
    # VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is not None :
        return redirect("/")
    # ------------------------------------

    email = request.form['email']
    password = request.form['password']

    if len(email) < 3 or len(email) > 40:
        error = "Your email format is bad. Please try again."
        return render_template ("login.html", error = error)

    if len(password) < 3 or len(password) > 40:
        error = "Your password format is bad. Please try again."
        return render_template ("login.html", error = error)

    # recuperer les donnes de l user et le token
    pload = {'email':email, 'password':password}
    r = requests.post('http://localhost:5000/login/',data = pload)
    # decoder le json ({"data" : "", "error" : ""})
    
    rst = json.loads(r.text)
#     # si il nous retorune une erreur : 
    if rst['error'] != None :
        error = rst['error']
        return render_template("login.html", error = error) 
    else :
        # etape : on remplit la varibale session (import de flask.session)
        session['token'] = rst["data"]["token"]
        session['user'] = rst["data"]["user"]
        flash("Your are connected")
        return redirect('/')

@app.route('/logout/', methods=['GET'])
def logout():
    #etape 1 : je recupere le token de ma session
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    #etape 1 : j apele mon backend
    requests.get('http://localhost:5000/logout?token=' + token)
    # je supprime de la session le token et l user 
    session.pop('token')
    session.pop('user')
    return redirect("/login/")