from models import sessions, users
from passlib.hash import sha256_crypt
import jwt

# CREATE
# Creer une session ------------------------------------
 
def create(email, password):
    # etape 1 : verifier que l utilisateur existe
    usr = users.User()
    usr.email = email
    usr = usr.get_by_email()
    if usr == None:
        return None, None, 'User not found' # on renvoit juste l EEREUR
    # etape 2 : verifier le mot de passe correspond
    if sha256_crypt.verify(password, usr.password) == False :
        return None, None, 'Bad password' # on renvoit juste l EEREUR
    # etape 3 : creer un token(str) (si etape 1 et 2 validees)
    encoded = str(jwt.encode({'username': usr.username, 'email' : usr.email}, 'l4ur45k', algorithm='HS256'))
    # etape 4 : appeler la db (create)
    sess = sessions.Session(encoded)
    sess.user_id = usr.id
    sess.create()
    # etape 5 : retourner un token(str) et un user(objet json)(username, email, id, password)
    # None => pas d'erreur 
    return encoded, usr, None


# DELETE
# supprimer une session ------------------------------------
def delete(encoded):
    # etape 1 : chercher si la session existe pour ce token
    sess = sessions.Session(encoded)
    sess = sess.get_by_token()
    # etape 2 : si lr token dans la session est le meme que celui donne, on supprime la session
    if sess != None:
        sess.delete()
    return True 


