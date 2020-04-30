from models import articles, sessions, comments
from datetime import datetime

# CREATE
# Creer un article-------------------------------
def create(title, body, token) :
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    # etape 2 : creer le modele article et remplir les champs
    art = articles.Article()
    art.title = title
    art.body = body
    # current date and hours
    now = datetime.now()
    art.creation_date = now.strftime("%D/%M/%Y %H:%M:%S")
    # --------
    art.user_id = sess.user_id
    # etape 3 : sauvegarder et recuperer l id  
    id = art.save()
    art.id = id
    return art, "" 

# READ
# Recuperer un article depuis son id -------------------------------
def get_article_by_id(_id, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    art = articles.Article()
    art.id = _id
    
    art = art.get_by_id()
    if art == None:
        return None, "article not found" 
    # creer le modeles pour PLUSIEURS commentaires
    comms = comments.Comments()
    # definir l'id de l'article associe
    comms.article_id = _id
    # recup tous les comms en db pour l'article id donne
    comms.all()
    art.comments = comms.comments
    return art, ""

# DELETE
# Supprimer un article  -----------------------------------
def delete(_id, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return "your are not logined"
    # etape 2 : creer le modele darticles et recuperer son id
    art = articles.Article()
    art.id = _id
    # etape 3 : recuperer l article en fonction de son id
    art.get_by_id()
    # etape 3 : verifier que l user id dans la session et le meme 
    if sess.user_id == art.user_id :
        art.delete()
        return ""
    else :
        return None, "you can't do it"

# READ
# Afficher tous les articles  -----------------------------------
def list_all(token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    arts = articles.Articles() # on creer une nouvelle instance de la class articles
    arts.all() # remplit la liste dans notre class articles avec tous les articles
    return arts.articles, ""  # renvoit la liste complete

# UPDATE
# mettre a jour l article ------------------------------
def update(_id, title, body, token):
    # etape 1 : recuperer la session
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return None, "your are not logined"
    # etape 2 : creer le modele darticles et changer le champs
    art = articles.Article()
     #recuperer l article en fonction de son id
    art.id = _id
    art.get_by_id()
    art.title = title
    art.body = body
    # etape 3 : verifier que l user id dans la session et le meme 
    if sess.user_id == art.user_id :
        art.update()
        return art, ""
    else :
        return None, "you can't do it"
    

    
    

