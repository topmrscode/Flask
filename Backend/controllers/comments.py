from models import sessions, comments
from datetime import datetime

# CREATE
# Creer un comment -------------------------------
def create(message, article_id,token) :
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    # etape 2 : creer le modele comment et remplir les champs
    com = comments.Comment()
    com.message = message
    # current date and hours
    now = datetime.now()
    com.creation_date = now.strftime("%D/%M/%Y %H:%M:%S")
    # --------
    com.article_id = article_id
    com.user_id = sess.user_id
    # etape 3 : sauvegarder et recuperer l id  
    id = com.save()
    com.id = id
    return com, "" 

# READ
# Recuperer un comment depuis son id -------------------------------
def get_comment_by_id(_id, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    # etape 2 : creer le modele comment et recuperer son contenu en fonction de son id
    com = comments.Comment()
    com.id = _id
    com = com.get_by_id()
    if com == None:
        return None, "comment not found" 
    return com, ""

# DELETE
# Supprimer un comment  -----------------------------------
def delete(_id, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return "your are not logined"
    # etape 2 : creer le modele comment et recuperer son id
    com = comments.Comment()
    com.id = _id
    # etape 3 : recuperer le commentaire en fonction de son id
    com.get_by_id()
    # etape 3 : verifier que l user id dans la session et le meme 
    if sess.user_id == com.user_id :
        com.delete()
        return ""
    else :
        return None, "you can't do it"

# READ
# Afficher tous les comments by article -----------------------------------
def list_all(article_id, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    coms = comments.Comments() # on creer une nouvelle instance de la class comments
    coms.article_id = article_id # definit larticle_id
    coms.all() # remplit la liste dans notre class comments avec tous les commentaires
    return coms.comments, ""  # renvoit la liste complete

# UPDATE
# mettre a jour le comment ------------------------------
def update(_id, message, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    # etape 2 : creer le modele comment et changer le champs
    com = comments.Comment()
     #recuperer le comment en fonction de son id
    com.id = _id
    com.get_by_id()
    com.message = message
    # etape 3 : verifier que l user id dans la session et le meme 
    if sess.user_id == com.user_id :
        com.update()
        return com, ""
    else :
        return None, "you can't do it"

    
    
