from flask import Flask
from flask_jwt import JWT,jwt_required, current_identity
from werkzeug.security import safe_str_cmp


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

class Admin(object):
	def __init__(self,id,username,password):
		self.id = id
		self.user_name = username
		self.password = password
	def __str__():
		return "Admin(id='%s')" % self.id


users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

admin = [
	Admin(1,"a1",'123456'),
	Admin(2,'a2','123456')
]

adminname_table ={u.user_name: u for u in admin}
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
adminid_table ={u.id: u for u in admin}

def authenticate_admin(username, password):
    user = adminname_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity_admin(payload):
    user_id = payload['identity']
    return adminid_table.get(user_id, None)

def authenticate_user(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity_user(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt_user = JWT(app, authenticate_user, identity_user)
jwt_admin = JWT(app,authenticate_admin,identity_admin)
@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()