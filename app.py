from flask import Flask, render_template, url_for, redirect, request, session
from pymongo import MongoClient
import utils

client = MongoClient()
db = client.pcparts

app = Flask(__name__)
app.secret_key = 'asdf'

@app.route("/")
@app.route("/home")
def home():
    if 'username' in session:
        return render_template('home.html', username = session['username'])
    else:
        return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    else:
        username = request.form['username'].encode('ascii', 'ignore')
        password = request.form['password'].encode('ascii', 'ignore')
        if auth.login(username, password) == "True":
            session['username'] = username
            return render_template('build.html', username = session['username'])
        else:
            error = auth.login(username, password)
            return render_template('login.html', error = error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if auth.register(username,password) == 'True':
            return render_template('login.html', username = session['username'])
        else:
            error = auth.register(username, password)
            return render_template('register.html"', error = error)

@app.route('/parts/<itemnum>')
def parts(itemnum):
    result = db.parts.find_one({'itemnumber':itemnum})
    if 'username' in session:
        return render_template('parts.html', username = session['username'], result=result)
    else:
        return render_template('parts.html', result=result)

@app.route('/add/<itemnum>')
def addpart(itemnum):
    if (db.cpus.find_one({'itemnumber':itemnum})):
        session['cpu'] = itemnum
    if (db.cases.find_one({'itemnumber':itemnum})):
        session['case'] = itemnum
    if (db.hdds.find_one({'itemnumber':itemnum})):
        session['hdd'] = itemnum
    if (db.ssds.find_one({'itemnumber':itemnum})):
        session['ssd'] = itemnum
    if (db.ram.find_one({'itemnumber':itemnum})):
        session['ram'] = itemnum
    if (db.mobos.find_one({'itemnumber':itemnum})):
        session['mobo'] = itemnum
    if (db.psus.find_one({'itemnumber':itemnum})):
        session['psu'] = itemnum
    if (db.gpus.find_one({'itemnumber':itemnum})):
        session['gpu'] = itemnum
    if 'username' in session:
        return redirect_template('build.html', username= session['username'], session=session)
    else:
        return redirect_template('build.html', session = session)


@app.route('/build')
def build():
    results = dict()
    for x in session:
        if x == 'cpu':
            results['cpu'] = db.cpus.find_one({'itemnumber':session[x]})
        if x == 'case':
            results['case'] = db.cpus.find_one({'itemnumber':session[x]})
        if x =='gpu':
            results['gpu'] = db.cpus.find_one({'itemnumber':session[x]})
        if x == 'psu':
            results['psu'] = db.cpus.find_one({'itemnumber':session[x]})
        if x =='hdd':
            results['hdd'] = db.cpus.find_one({'itemnumber':session[x]})
        if x == 'ssd':
            results['ssd'] = db.cpus.find_one({'itemnumber':session[x]})
        if x =='ram':
            results['ram'] = db.cpus.find_one({'itemnumber':session[x]})
        if x == 'mobo':
            results['mobo'] = db.cpus.find_one({'itemnumber':session[x]})
    if 'username' in session:
        return redirect_template('build.html', username = session['username'], results=results)
    else:
        return redirect_template('build.html', results=results)

@app.route('/remove/<part>')
def remove(part):
    session.pop(part, None)
    if 'username' in session:
        return redirect_template('build.html', username= session['username'], session=session)
    else:
        return redirect_template('build.html', session = session)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect_template('home.html')

@app.route('/cpu')
def cpu():
    result = list(db.cpus.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('cpu.html', username = session['username'], result=result)
    else:
        return render_template('cpu.html', result=result)

@app.route('/mobo')
def mobo():
    result = list(db.mobos.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('mobo.html', username = session['username'], result=result)
    else:
        return render_template('mobo.html', result=result)

@app.route('/ram')
def ram():
    result = list(db.ram.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('ram.html', username = session['username'], result=result)
    else:
        return render_template('ram.html', result=result)

@app.route('/hdd')
def hdd():
    result = list(db.hdds.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('hdd.html', username = session['username'], result=result)
    else:
        return render_template('hdd.html', result=result)

@app.route('/ssd')
def ssd():
    result = list(db.ssds.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('ssd.html', username = session['username'], result=result)
    else:
        return render_template('ssd.html', result=result)

@app.route('/gpu')
def gpu():
    result = list(db.gpus.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('gpu.html', username = session['username'], result=result)
    else:
        return render_template('gpu.html', result=result)

@app.route('/psu')
def psu():
    result = list(db.psus.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('psu.html', username = session['username'], result=result)
    else:
        return render_template('psu.html', result=result)

@app.route('/case')
def case():
    result = list(db.cases.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('case.html', username = session['username'], result=result)
    else:
        return render_template('case.html', result=result)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=6002)

#use this to learn about the structure of the db
#result = list(db.cpus.find({}, fields = {'_id':False}))
#print result[0]['specs']
#result = db.cpus.find_one({"itemnumber":"11-233-116"})

