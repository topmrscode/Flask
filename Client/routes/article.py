from app import app
from flask import render_template, request, redirect, flash, session
import json
import requests

# CREATE
@app.route('/articles/', methods=['POST'])
def create():
    # etape 1 : VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    # etape 2 : Recuperer les infos du formulaire
    title = request.form["title"]
    body = request.form["body"]
    # verification des remplissages null
    if title == "" :
        flash("Title can't be empty")
        return redirect('/articles/')
    if body == "" :
        flash("Body can't be empty")
        return redirect('/articles/')
    # etape 3 : recuperer le json et le decoder
    pload = {'title': title, 'body':body}
    r = requests.post('http://localhost:5000/articles/?token=' + token,data = pload)
    rst = json.loads(r.text)
    # etape 4 : verification des erreurs 
    if rst['error'] != None :
        flash(rst["error"])
        return redirect('/articles/')
    else :
        flash("Article created")
        return redirect('/articles/')

# READ
# ----------------------lister tous les ARTICLES -------------------------
@app.route('/articles/', methods=['GET'])
def list_articles():
    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    # etape 2 : recuperer le json et le decoder
    r = requests.get('http://localhost:5000/articles?token=' + token) # je data qui contient recupere les listes 
    rst = json.loads(r.text)
#   #etape 3 : remplir le champs data avec les articles
    res = rst["data"]
    return render_template("articles_list.html", user = user, articles_list = res)

# DELETE
# ----------------------supprimer article by id -------------------------
@app.route('/articles/<id>/delete', methods=['GET'])
def delete_article(id):
    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    requests.delete('http://localhost:5000/articles/' + id + "?token=" + token)
    
    flash("Article has been deleted")
    return redirect('/articles/')

# UPDATE
# ---------------------- (PAGE AFFICHAGE DE FORMULAIRE MODIFY ARTICLE)-------------------------
@app.route('/articles/<id>/modify', methods=['GET'])
def update_article_form(id):
    """Render website's MODYFY page."""
    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    
    # etape 2 : recuperer les details de l article avec l id
    r = requests.get('http://localhost:5000/articles/' + id + "?token=" + token)
    rst = json.loads(r.text)
    if rst["data"]["user_id"] != user["id"]:
        return redirect("/articles/")
    return render_template("article_modify.html", user = user, article_details = rst["data"])

# ----------------------POST-------------------------
@app.route('/articles/<id>/modify', methods=['POST'])
def update_article(id):

    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    # etape 2 : recuperer les infos du formulaire
    title= request.form['title']
    body = request.form['body']
    # verification des remplissages null
    if title == "" :
        flash("Title can't be empty")
        return redirect('/articles/' + id + '/modify')
    if body == "" :
        flash("Body can't be empty")
        return redirect('/articles/' + id + '/modify')
    #---------------------------
    #etape 3 : CREATION DU PLOAd POUR ENVOYER AU BACKEND
    pload = {'title':title, 'body':body}
    #----------------------------
    # etape 4 : recuperer les details de larticle modifie 
    requests.put('http://localhost:5000/articles/' + id + "?token=" + token,data = pload)
        
    flash("Article has been modified")
    return redirect('/articles/' + id)

# READ
# ----------------------detail de larticle  -------------------------
@app.route('/articles/<id>', methods=['GET'])
def article_details(id):
    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    # etape 2 : recuperer le json et le decoder
    r = requests.get('http://localhost:5000/articles/'+ id + '?token=' + token) # je data qui contient recupere les listes 
    rst = json.loads(r.text)
#     {
#     "data": {
#         "body": "Innovation is part of world",
#         "comments": [
#             {
#                 "article_id": 1,
#                 "creation_date": "04/18/20/13/2020 15:13:41",
#                 "id": 1,
#                 "message": "its so cool",
#                 "user_id": 1
#             },
#             {
#                 "article_id": 1,
#                 "creation_date": "04/18/20/13/2020 15:13:53",
#                 "id": 2,
#                 "message": "its bad",
#                 "user_id": 1
#             },
#             {
#                 "article_id": 1,
#                 "creation_date": "04/18/20/14/2020 15:14:03",
#                 "id": 3,
#                 "message": "its reallyyyyyyyyyyyy bad",
#                 "user_id": 1
#             }
#         ],
#         "creation_date": "04/18/20/12/2020 15:12:01",
#         "id": 1,
#         "title": "lol",
#         "user_id": 1
#     },
#     "error": null
# }
#   #etape 3 : remplir le champs data avec les articles
    res = rst["data"]
    return render_template("article_details.html", user = user, article = res)