from pymongo import MongoClient
from flask import session

client = MongoClient()
db = client.pcparts


def register(username,password,chkpw,email):
    if(db.users.find({"username":username}).count()) != 0:
        return "There is a account with that username"
    elif(chkpw != password):
        return "Passwords aren't the same"
    elif(db.users.find({"email":email}).count()) != 0:
        return "There is an account with that email"
    else:
        db.users.insert({'username':username, 'password' : password, 'email' : email})
        return 'True'

def login(user,password):
    check=db.users.find_one({'username':user,'password':password}, fields={'_id':False})
    if (db.users.find({"username":user}).count()) == 0:
        return "No account with that username"
    elif check == None:
        return "Username or password is invalid"
    else:
        return 'True'
