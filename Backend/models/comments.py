from config.db import query_db

class Comment :

    def __init__(self):
        self.id = -1
        self.creation_date = ""
        self.article_id = -1
        self.user_id= -1

# CREATE
# ------------- sauvergarder Le comment en DB------------------
    def save(self):
        # le query db renvoit comment vide (car INSERT) et un id (remplie)
        comment, id = query_db("INSERT INTO comments (message, creation_date, article_id, user_id) VALUES(?, ?, ?, ?)", (self.message, self.creation_date, self.article_id, self.user_id))
        return id

# READ
# ------------- recuperer le comment par son id ------------------
    def get_by_id(self):
        comment, id = query_db("SELECT * FROM comments WHERE id = ?", (self.id,), True) # True == je veux qu un element
        if comment != None :
            self.message = comment["message"]
            self.creation_date= comment["creation_date"]
            self.id = comment["id"]
            self.article_id = comment["article_id"]
            self.user_id = comment["user_id"]
            return self
        return None

# UPDATE
# ------------- Mettre a jour le comment ------------------
    def update(self): 
        query_db("UPDATE comments SET message = ? WHERE id = ?", (self.message, self.id))
        
# DELETE
# -------------- supprimer un comment ------------------------
    def delete(self):
        query_db("DELETE FROM comments WHERE id = ?", (self.id,), True)


class Comments :

    def __init__(self):
        self.comments = []
        self.article_id = -1

# READ
# ------------- lister tous les comments by article id ------------------
    def all(self):
        comments, ids = query_db("SELECT * FROM comments WHERE article_id = ?", (self.article_id,))
        if comments is None :
            return
        for com in comments :
            tmp = Comment() 
            tmp.message = com["message"]
            tmp.creation_date = com["creation_date"]
            tmp.article_id = com["article_id"]
            tmp.user_id = com["user_id"]
            tmp.id = com["id"]
            self.comments.append(tmp)