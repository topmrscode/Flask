from app import app
from flask import render_template, request, redirect
from passlib.hash import sha256_crypt
from config.db import query_db
from controllers import users, sessions, articles, comments
from helpers import json as h_json
import json

# ROUTES RELATED TO SESSIONS --------------
# ----------------------Routes and controlers related to Login page -------------------------

@app.route('/login/', methods=['POST'])
def login():
    dico = {"error" : None, "data" : None}

    email = request.form['email']
    password = request.form['password']

    if len(email) < 3 or len(email) > 40:
        dico["error"] = "Your email format is bad. Please try again."
        return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

    if len(password) < 3 or len(password) > 40:
        dico["error"] = "Your password format is bad. Please try again."
        return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# on appelle dans le controler sessions la methode create
    token, usr, err = sessions.create(email, password)
    if err != None:
        dico["error"] = err
    else:
        dico["data"] = {"token" : str(token), "user" : usr}
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# ----------------------LOGOUT -------------------------
@app.route('/logout/', methods=['GET'])
def logout():
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #etape 3 : appeller la methode delete du controller 
    sessions.delete(token)
    #etape 4 : on complete la raponse et on la renvoit sous format json
    dico["data"] = "user disconnected"
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)


# ROUTES RELATED TO USERS --------------

# ----------------------Routes and controlers related to  Register page -------------------------

@app.route('/register/', methods=['POST'])
def register():
    dico = {"error" : None, "data" : None}
    """Render register page."""
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    if len(username) < 3 or len(username) > 40:
        dico["error"] = "Your username format is bad. Please try again."
        return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

    if len(email) < 3 or len(email) > 40:
        dico["error"] = "Your email format is bad. Please try again."
        return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

    if len(password) < 3 or len(password) > 40:
        dico["error"] = "Your password format is bad. Please try again."
        return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)
    
    usr, error = users.create(username, email, password)
    if error != None :
        dico["error"] = error 
    else :
        dico["data"] = usr
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True) #j encode en json l user 

# ----------------------GET user by id -------------------------
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    dico = {"error" : None, "data" : None}

    usr, err = users.get_user_by_id(id)
    if err != None:
        dico["error"] = err
    else:
        dico["data"] = usr
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# ----------------------met a jour user by id -------------------------
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    dico = {"error" : None, "data" : None}

    token = request.args.get('token')
    username = request.form['username']
    email = request.form['email']
    if "password" in request.form :
        password = request.form['password']
        rst = users.update(id, username, email, password, token)
    else :
        rst = users.update(id, username, email, "", token)

    dico["data"] = rst
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# ----------------------supprimer user by id -------------------------
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    dico = {"error" : None, "data" : None}

    token = request.args.get('token')
    users.delete(id, token)
    dico["data"] = "user deleted"
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# ----------------------lister tous les users -------------------------
@app.route('/users/', methods=['GET'])
def list_users():
    dico = {"error" : None, "data" : None}
    rst = users.list_all() # recupere la liste du controller
    dico["data"] = rst # je met cette liste dans la partie data de ma reponse

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# ROUTES RELATED TO ARTICLES --------------
# CREATE
@app.route('/articles/', methods=['POST'])
def create():
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #ETAPE 3 : RECUPER les champs du formaulaire 
    title = request.form["title"]
    body = request.form["body"]
    #eatpe 4 : appeller la methode create du controller qui retourne 2 parametres
    art, err = articles.create(title, body, token)
    if err == "":
        dico["data"] = art
    else :
        dico["error"] = err
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# READ
# LISTER TOUS LES ARTICLES
@app.route('/articles/', methods=['GET'])
def list_all():
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #eatpe 3 : appeller la methode LIST all du controller qui retourne 2 parametres
    rst, err = articles.list_all(token)
    if err == "":
        dico["data"] = rst
    else :
        dico["error"] = err

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# READ
# RECUPERER LES DETAILS DE UN ARTICLE --------------
@app.route('/articles/<id>', methods=['GET'])
def get_article(id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #eatpe 3 : appeller la methode get_article_by_id du controller qui retourne 2 parametres
    art, err = articles.get_article_by_id(id, token)
    if err == "":
        dico["data"] = art
    else :
        dico["error"] = err
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# UPDATE
# ----------------------met a jour article by id -------------------------
@app.route('/articles/<id>', methods=['PUT'])
def update_articles(id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #ETAPE 3 : RECUPER les champs du formaulaire 
    title = request.form["title"]
    body = request.form["body"]
    #eatpe 4 : appeller la methode update du controller qui retourne 1 parametres
    art, err = articles.update(id, title, body, token)
    if err != "":
        dico["error"] = err
    else :
        dico["data"] = art

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# DELETE
# ----------------------supprimer ARTICLE by id -------------------------
@app.route('/articles/<id>', methods=['DELETE'])
def delete_article(id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #eatpe 4 : appeller la methode delet du controller qui retourne 1 parametres
    art, err = articles.delete(id, token)
    if err != "":
        dico["error"] = err

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)
    
# ROUTES RELATED TO COMMENTS --------------
# CREATE
@app.route('/articles/<article_id>/comments/', methods=['POST'])
def create_comments(article_id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #ETAPE 3 : RECUPER les champs du formaulaire 
    message = request.form["message"]
    #eatpe 4 : appeller la methode create du controller qui retourne 2 parametres
    com, err = comments.create(message, article_id, token)
    if err == "":
        dico["data"] = com
    else :
        dico["error"] = err
    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# READ
# LISTER TOUS LES COOMENTS D un article
@app.route('/articles/<article_id>/comments/', methods=['GET'])
def list_all_comments(article_id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #eatpe 3 : appeller la methode LIST all du controller qui retourne 2 parametres
    rst, err = comments.list_all(article_id, token)
    if err == "":
        dico["data"] = rst
    else :
        dico["error"] = err

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# READ
# LISTER TOUS LES COOMENTS D un article
@app.route('/articles/<article_id>/comments/<id_comment>/', methods=['GET'])
def get_comments(article_id, id_comment):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #eatpe 3 : appeller la methode LIST all du controller qui retourne 2 parametres
    rst, err = comments.get_comment_by_id(id_comment, token)
    if err == "":
        dico["data"] = rst
    else :
        dico["error"] = err

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# UPDATE
# ----------------------met a jour comment by id -------------------------
@app.route('/articles/<article_id>/comments/<id>', methods=['PUT'])
def update_comments(article_id, id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #ETAPE 3 : RECUPER les champs du formaulaire 
    message = request.form["message"]
    #eatpe 4 : appeller la methode update du controller qui retourne 1 parametres
    rst, err = comments.update(id, message, token)
    if err != "":
        dico["error"] = err
    else :
        dico["data"] = rst

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)

# DELETE
# ----------------------supprimer COMMENT by id -------------------------
@app.route('/articles/<article_id>/comments/<id>', methods=['DELETE'])
def delete_comment(article_id, id):
    # etape 1 : preparer la structure de la reponse
    dico = {"error" : None, "data" : None}
    #etape 2 : recuperer le token dans l url
    token = request.args.get('token')
    #eatpe 4 : appeller la methode delete du controller qui retourne 1 parametres
    rst, err = comments.delete(id, token)
    if err != "":
        dico["error"] = err

    return json.dumps(dico,default=h_json.convert_to_dict,indent=4, sort_keys=True)
    