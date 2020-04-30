from app import app
from flask import render_template, request, redirect, flash, session
import json
import requests

@app.route('/register/', methods=['POST'])
def register():
    """Render register page."""
    #recuper le user pour le passer au render template
    if "token" in session : 
        return redirect('/')

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if len(username) < 3 or len(username) > 40:
        error = "Your username format is bad. Please try again."
        return render_template ("register.html", error = error)

    if len(email) < 3 or len(email) > 40:
        error = "Your email format is bad. Please try again."
        return render_template ("register.html", error = error)

    if len(password) < 3 or len(password) > 40:
        error = "Your password format is bad. Please try again."
        return render_template ("register.html", error = error)
    
    # APPEL HTTP 
    pload = {'username':username, 'email':email, 'password':password}
    r = requests.post('http://localhost:5000/register/',data = pload)
    # decoder le json ({"data" : "", "error" : ""})
    
    rst = json.loads(r.text)
    # "data": {
    #     "email": "toto@gmail.com",
    #     "id": -1,
    #     "password": "$5$rounds=535000$T6kR3/TaHsBPueCq$XcwX2P8vm34Y8WvzKY1whxyjlC5P9g7jCggXSrg2Eh1",
    #     "username": "toto"
    # },
    # "error": null
    # print(r.text)
    # si il nous retorune une erreur : 
    if rst['error'] != None :
        error = rst["error"]
        return render_template("register.html", error = error) 
    else :
        flash("User created")
        return redirect('/login/')

@app.route('/users/<id>', methods=['GET'])
def get_user(id):

    # VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------

    # APPEL HTTP 
    r = requests.get('http://localhost:5000/users/' + id + "?token=" + token)
    # decoder le json ({"data" : "", "error" : ""})
    
    rst = json.loads(r.text)
    # si il nous retorune une erreur : 
    # if rst['error'] != None :
    #     error = "Internal error. Please try again."
    #     return render_template(".html", error = error) 
    # else :
    # print(r.text) # nous donne sur le terminal :
    #     "data": {
    #     "email": "laura.baudean",
    #     "id": 2,
    #     "password": "$5$rounds=535000$Pa.OIcujC1z5Ps1v$23OFJFhvPYsQBh2RJfuSoD8Sg.hd6.VztJqCGgxRRQD",
    #     "username": "ghjghj"
    # },
    # "error": null
    res = rst["data"]
    return render_template("user_details.html", user = user, user_details = res)

# ----------------------met a jour user by id (PAGE AFFICHAGE DE FORMULAIRE)-------------------------
@app.route('/users/<id>/modify', methods=['GET'])
def update_form(id):
    """Render website's MODYFY page."""
    # VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    
    # recupere les details de l user avec l id
    r = requests.get('http://localhost:5000/users/' + id + "?token=" + token)
    rst = json.loads(r.text)
    if rst["data"]["id"] != user["id"]:
        return redirect("/users/")

    return render_template("user_modify.html", user = user, user_details = rst["data"])

# ----------------------met a jour user by id (PAGE FORMULAIRE)-------------------------
@app.route('/users/<id>/modify', methods=['POST'])
def update_user(id):

    # VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    #RECUPERER LES INFOS DU FORM
    username = request.form['username']
    email = request.form['email']
    if "password" in request.form :
        password = request.form['password']
    else :
        password = ""
    #---------------------------
    #CREATION DU PLOAS POUR ENVOYER AU BACKEND
    pload = {'username':username, 'email':email, 'password':password}
    #----------------------------
    # APPEL DU BACKEND
    requests.put('http://localhost:5000/users/' + id + "?token=" + token,data = pload)
    # si on essaye de modifier notre propore compte, on enregister les modif dans la session
    if user["id"] == id :
        user["username"] = username
        user["email"] = email
        session["user"] = user
        
    flash("Informations have been modified")
    return redirect('/users/' + id)

# ----------------------supprimer user by id -------------------------
@app.route('/users/<id>/delete', methods=['GET'])
def delete_user(id):
    # VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    requests.delete('http://localhost:5000/users/' + id + "?token=" + token)
    
    if id == str(user["id"]) :
        return redirect("/logout/")
    flash("Account has been deleted")
    return redirect('/')

# ----------------------lister tous les users -------------------------
@app.route('/users/', methods=['GET'])
def list_users():
    # VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------

    r = requests.get('http://localhost:5000/users?token=' + token) # je data qui contient recupere les listes 
    rst = json.loads(r.text) 

    res = rst["data"]
    return render_template("users_list.html", user = user, users_list = res)