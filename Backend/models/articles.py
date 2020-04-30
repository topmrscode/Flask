from config.db import query_db

class Article :

    def __init__(self):
        self.id = -1
        self.title = ''
        self.body = ""
        self.creation_date = ""
        self.user_id= -1
        self.comments = []

# CREATE
# ------------- sauvergarder L'article en DB------------------
    def save(self):
        # le query db renvoit art vide (car INSERT) et un id (remplie)
        art, id = query_db("INSERT INTO articles (title, body, creation_date, user_id) VALUES(?, ?, ?, ?)", (self.title, self.body, self.creation_date, self.user_id))
        return id

# READ
# ------------- recuperer l article par son id ------------------
    def get_by_id(self):
        article, id = query_db("SELECT * FROM articles WHERE id = ?", (self.id,), True) # True == je veux qu un element
        if article != None :
            self.title = article["title"]
            self.body = article["body"]
            self.creation_date= article["creation_date"]
            self.id = article["id"]
            self.user_id = article["user_id"]
            return self
        return None

# UPDATE
# ------------- Mettre a jour l article ------------------
    def update(self): 
        query_db("UPDATE articles SET title = ?, body = ? WHERE id = ?", (self.title, self.body, self.id))
        
# DELETE
# -------------- supprimer un article ------------------------
    def delete(self):
        query_db("DELETE FROM articles WHERE id = ?", (self.id,), True)


class Articles :

    def __init__(self):
        self.articles = []

# READ
# ------------- lister tous les articles ------------------
    def all(self):
        articles, ids = query_db("SELECT * FROM articles")
        for art in articles :
            tmp = Article() 
            tmp.title = art["title"]
            tmp.body = art["body"]
            tmp.creation_date = art["creation_date"]
            tmp.user_id = art["user_id"]
            tmp.id = art["id"]
            self.articles.append(tmp)