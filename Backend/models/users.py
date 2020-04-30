from config.db import query_db

class User :

    def __init__(self, username ="", email= "", password=""):
        self.username = username
        self.email = email
        self.password = password
        self.id = -1

# CREATE
# ------------- sauvergarder L'user en DB------------------
    def save(self):
        usr, id = query_db("INSERT INTO users (username, email, password) VALUES(?, ?, ?)", (self.username, self.email, self.password))
        return id

# READ
# ------------- recuperer l user par son id ------------------
    def get_by_id(self):
        user, id = query_db("SELECT * FROM users WHERE id = ?", (self.id,), True) # True == je veux qu un element
        if user != None :
            self.username = user["username"]
            self.email = user["email"]
            self.password = user["password"]
            self.id = user["id"]
            return self
        return None

# ------------- recuperer l user par son email ------------------
    def get_by_email(self):
        user, id = query_db("SELECT * FROM users WHERE email = ?", (self.email,), True) 
        if user != None :
            self.username = user["username"]
            self.email = user["email"]
            self.password = user["password"]
            self.id = user["id"]
            return self
        return None

# UPDATE
# ------------- Mettre a jour l user ------------------
    def update(self, passwd = False):  # boolen pour gerer la modif du password
        if passwd == False :
            query_db("UPDATE users SET username = ?, email = ? WHERE id = ?", (self.username, self.email, self.id))
        else :
            query_db("UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?", (self.username, self.email, self.password, self.id))
# DELETE
# -------------- supprimer un user ------------------------
    def delete(self):
        query_db("DELETE FROM users WHERE id = ?", (self.id,), True)


class Users :

    def __init__(self):
        self.users = []

# READ
# ------------- lister tous les users ------------------
    def all(self):
        users, ids = query_db("SELECT * FROM users")
        for usr in users :
            tmp = User(usr['username'], usr['email'], usr['password'])
            tmp.id = usr["id"]
            self.users.append(tmp)