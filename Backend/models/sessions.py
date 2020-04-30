from config.db import query_db

class Session :

    def __init__(self, token):
        self.token = token
        self.user_id = -1
        self.id = -1

# CREATE
# ------------- Sauvergarder le token ---------------
    def create(self):
        art, id = query_db("INSERT INTO sessions (token, user_id) VALUES(?, ?)", (self.token, self.user_id))
        return id

# READ
# -------- recuperer les token d apres l id de l user  -----
    def get_by_user_id(self):
        session, id = query_db("SELECT * FROM sessions WHERE user_id = ?", (self.user_id,), True)
        if session != None:
            self.id = session["id"]
            self.token = session["token"]
            self.user_id = session["user_id"]
            return self
        return None

# READ
# -------------- get by token  ------------------------
    def get_by_token(self):
        session, id = query_db("SELECT * FROM sessions WHERE token = ?", (self.token,), True)
        if session != None:
            self.id = session["id"]
            self.token = session["token"]
            self.user_id = session["user_id"]
            return self
        return None

# DELETE
# -------------- DELETE ------------------------------
    def delete(self):
        query_db("DELETE FROM sessions WHERE id = ?", (self.id,),True)
