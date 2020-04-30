from app import app
from flask import render_template, request, redirect, flash, session
import json
import requests

# CREATE
@app.route('/articles/<id>/comments/', methods=['POST'])
def create_comment(id):
    # etape 1 : VERFICATION LA CONNEXION DE l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    # etape 2 : Recuperer les infos du formulaire
    message = request.form["message"]
    # verification des remplissages null
    if message == "" :
        flash("Comment can't be empty")
        return redirect('/articles/'+id)
    # etape 3 : recuperer le json et le decoder
    pload = {'message': message}
    r = requests.post('http://localhost:5000/articles/'+ id + '/comments/?token=' + token,data = pload)
    rst = json.loads(r.text)
    # etape 4 : verification des erreurs 
    if rst['error'] != None :
        flash(rst["error"])
        return redirect('/articles/'+id)
    else :
        flash("Comment added")
        return redirect('/articles/'+id)

# DELETE
# ----------------------supprimer un comment -------------------------
@app.route('/articles/<id>/comments/<id_comment>/delete', methods=['GET'])
def delete_comment(id, id_comment):
    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    requests.delete('http://localhost:5000/articles/' + id + '/comments/' + id_comment + "?token=" + token)
    
    flash("Comment has been deleted")
    return redirect('/articles/'+ id)

# UPDATE
# ---------------------- (PAGE AFFICHAGE DE FORMULAIRE MODIFY comment)-------------------------
@app.route('/articles/<id>/comments/<id_comment>/modify', methods=['GET'])
def update_comment_form(id, id_comment):
    """Render website's MODYFY page."""
    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    
    # etape 2 : recuperer les details du comment avec l id
    r = requests.get('http://localhost:5000/articles/' + id + '/comments/' + id_comment +"/?token=" + token)
    rst = json.loads(r.text)
    if rst["data"]["user_id"] != user["id"]:
        return redirect("/articles/"+id)
    return render_template("comment_modify.html", user = user, comment = rst["data"])

# ----------------------POST-------------------------
@app.route('/articles/<id>/comments/<id_comment>/modify', methods=['POST'])
def update_comment(id, id_comment):

    # etape 1 : verifier la connexion de l user 
    token = session.get("token")
    if token is None :
        return redirect("/login/")
    user = session.get("user")
    # ------------------------------------
    # etape 2 : recuperer les infos du formulaire
    message= request.form['message']
    # verification des remplissages null
    if message == "" :
        flash("Comment can't be empty")
        return redirect('/articles/' + id + '/comments/' + id_comment + '/modify')
    #---------------------------
    #etape 3 : CREATION DU PLOAd POUR ENVOYER AU BACKEND
    pload = {'message':message}
    #----------------------------
    # etape 4 : recuperer les details du comment modifie 
    requests.put('http://localhost:5000/articles/' + id + '/comments/' + id_comment + "?token=" + token,data = pload)
        
    flash("Comment has been modified")
    return redirect('/articles/' + id)
