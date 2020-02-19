import flask
from flask import *
import flask_bootstrap
import flask_pymongo
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from flask_moment import Moment
from datetime import datetime

app = Flask("My-Digital-Diary")
app.config["MONGO_URI"] = " cluster0-shard-00-00-y36ty.mongodb.net:27017"
app.config['SECRET_KEY'] = 'abc'
moment = Moment(app)


Bootstrap(app)
mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            doc[item] = request.form[item]
        mongo.db.users.insert_one(doc)
        flash('Account created successfully!')
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def loginn():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == 'POST':
        docc = {'Email': request.form['login-email'], 'Password': request.form['login-password']}
        found = mongo.db.users.find_one(docc)
        if found is None:
            flash("The email/password doesn't work. Try again")
            return redirect("/login")
        else:
            print("CORRECT")
            print(found)
            session['user-info'] = {'firstName': found['First Name'], 'lastName': found['Last Name'],'email': found['Email'], 'loginTime': datetime.utcnow()}
            return redirect("/home")

@app.route('/home',  methods=['GET', 'POST'])
def home():
    if 'user-info' in session:
        if request.method == "GET":
            savedEntries = mongo.db.entries.find({'user': session['user-info']['email']}).sort('time', -1)
            # print("samesame")
            bob = savedEntries
            lst = [x for x in savedEntries]
            for entry in savedEntries:
                print(entry)
            print(savedEntries)
            return render_template('home.html', entries=lst)
        elif request.method == "POST":
            entry = {'user': session['user-info']['email'], 'content': request.form['content'], 'time': datetime.utcnow()}
            mongo.db.entries.insert_one(entry)
            print("samesamesame")
            return redirect('/home')
    else:
        flash("You need to login first!")
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user-info')
    return redirect('/login')

app.run(debug=True)

