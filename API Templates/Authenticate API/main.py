import json
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mtalkz.db'
db = SQLAlchemy(app)

class field_agent(db.Model):
    email = db.Column(db.String(length = 30), nullable = False, unique = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String(length = 30), nullable = False)
    type = db.Column(db.String(length = 30), nullable = False, default = 'field_agent')
    active = db.Column(db.Boolean, nullable = False, default = True)

    def __repr__(self):
        return f'Username : {self.username}'

class customer(db.Model):
    email = db.Column(db.String(length = 30), nullable = False, unique = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True, primary_key = True)
    type = db.Column(db.String(length = 30), nullable = False, default = 'customer')
    active = db.Column(db.Boolean, nullable = False, default = True)

    def __repr__(self):
        return f'Username : {self.username}'

@app.route('/')
def home():
    return 'Hello'

@app.route('/login', methods = ['GET', 'POST'])
def authenticate():
    username = request.args.get('un',None)
    password = request.args.get('pass',None)
    if username is None or password is None:
        return jsonify({'Message': 'Proper Parameters are not given.'})
    agent = field_agent.query.filter_by(username = username, type = 'field_agent').first()
    if agent.password == password:
        return jsonify({'Message': 'Authentication Successful'})
    else:
        return jsonify({'Message': 'Username or Password incorrect. Please try again.'})

@app.route('/register', methods = ['GET', 'POST'])
def register():
    email_id = request.args.get('eid',None)
    username = request.args.get('un',None)
    type = request.args.get('type',None)
    user = None
    if email_id is None or username is None or type is None:
        return jsonify({'Message': 'Proper Parameters are not given'})
        
    if type == 'field_agent':
        password1 = request.args.get('pass1',None)
        password2 = request.args.get('pass2',None)
        if password1 is None or password2 is None:
            return jsonify({'Message': 'Proper Parameters are not given'})
        if password1 != password2:
            return jsonify({'Message': 'Password not matched'})
        user = field_agent(email = email_id,username = username,password = password1)
    else:
        user = customer(email = email_id,username = username)

    db.session.add(user)
    db.session.commit()
    return jsonify({'Message': 'Information added to the database'})

@app.route('/reset_password')
def reset_password():
    username = request.args.get('un',None)
    password = request.args.get('pass',None)
    if username is None or password is None:
        return jsonify({'Message': 'Proper Parameters are not given'})
    agent = field_agent.query.filter_by(username = username).first()
    agent.password = password
    db.session.commit()
    return jsonify({'Message': 'Password has been reset'})

@app.route('/deactivate')
def deactivate():
    username = request.args.get('un',None)
    type = request.args.get('type',None)
    user = None
    if username is None or type is None:
        return jsonify({'Message': 'Proper Parameters not given'})
    if type == 'field_agent':
        user = field_agent.query.filter_by(username = username).first()
    else:
        user = customer.query.filter_by(username = username).first()
    user.active = False
    db.session.commit()
    return jsonify({'Message': 'User deactivated'})

@app.route('/activate')
def activate():
    username = request.args.get('un',None)
    type = request.args.get('type',None)
    user = None
    if username is None or type is None:
        return jsonify({'Message': 'Proper Parameters not given'})
    if type == 'field_agent':
        user = field_agent.query.filter_by(username = username).first()
    else:
        user = customer.query.filter_by(username = username).first()
    user.active = True
    db.session.commit()
    return jsonify({'Message': 'User activated'})

@app.route('/active_users')
def provide_active_users():
    customers = customer.query.filter_by(active = True).limit(100).all()
    names = []
    for x in customers:
        names.append(x.username)
    return jsonify(names)

@app.route('/active_agents')
def provide_active_agents():
    agents = field_agent.query.filter_by(active = True).limit(100).all()
    names = []
    for x in agents:
        names.append(x.username)
    return jsonify(names)

if __name__ == '__main__':
    app.run(debug= True)