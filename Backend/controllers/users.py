from models import users, sessions
from passlib.hash import sha256_crypt

# Creer un user -------------------------------
def create(username, email, password) :
    usr = users.User("", email, "") # on creer notre modele utilisateur
    usr = usr.get_by_email() # on appel la db avec l email quon a remplit
    if usr != None : # si l utilisateur avec cet email n existe pas 
        return None, "user already exist"
    hashed_pw = sha256_crypt.encrypt(password)
    usr = users.User(username, email, hashed_pw)
    usr.save()
    usr.get_by_email() # recupere l utilisateur d apres son email (gestion des id = -1)
    return usr, None 

# Recuperer un user depuis son id -------------------------------
def get_user_by_id(_id):
    usr = users.User()
    usr.id = _id
    
    usr = usr.get_by_id()
    if usr == None:
        return None, "user not found" 
    return usr, None

# Recuperer un user depuis son email  -------------------------------
def get_user_by_email(email):
    usr = users.User()
    usr.email = email

    usr = usr.get_by_email()
    if usr == None:
        return None, "user not found" 
    return usr, None


# Supprimer un user  -----------------------------------
def delete(_id, token):
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return "your are not logined"
    # if sess.user_id != id :
    #     return "You don't have the right to do it"

    usr = users.User()
    usr.id = _id
    usr.delete()
    return True

# Afficher tous les users  -----------------------------------
def list_all():
    usrs = users.Users() # on creer une nouvelle instance de la class users
    usrs.all() # remplit la liste dans notre class users avec tous les utilisateurs
    return usrs.users # renvoit la liste complete

# mettre a jour l utilisateur  ------------------------------
def update(_id, username, email, password, token):
    sess = sessions.Session(token)
    sess = sess.get_by_token()
    if sess == None:
        return "your are not logined"
  

    if password != "":
        hashed_pw = sha256_crypt.encrypt(password)
    else :
        hashed_pw = password
    usr = users.User(username, email, hashed_pw)
    usr.id = _id
    if hashed_pw != "" :
        usr.update(True)
    else :
        usr.update(False)
    return usr

