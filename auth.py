def register(username,password,chkpw):
    if(users.find({"username":user}).count()) != 0:
        return False
    elif(chkpw != password):
        return False
    else:
        db.users.insert({'username':username, 'password' : password})
        return True

def login(user,password):
