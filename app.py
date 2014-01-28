from flask import Flask, render_template, url_for, redirect, request, session
from pymongo import MongoClient
import utils,auth,gimages

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
            return render_template('home.html', username = session['username'])
        if auth.login(username, password) == 'No account with that username':
            error1 = auth.login(username, password)
            return render_template('login.html', error1 = error1)
        if auth.login(username, password) == "Username or password is invalid":
            error2 = auth.login(username, password)
            return render_template('login.html', error2 = error2)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username'].encode('ascii', 'ignore')
        password = request.form['password'].encode('ascii', 'ignore')
        checkpas = request.form['checkpas'].encode('ascii', 'ignore')
        email = request.form['email'].encode('ascii', 'ignore')
        if auth.register(username,password,checkpas,email) == 'True':
            return render_template('home.html')
        if auth.register(username,password,checkpas,email) == 'There is a account with that username':
            error1 = auth.register(username, password,checkpas,email)
            return render_template('register.html', error1 = error1)
        if auth.register(username,password,checkpas,email) == "Passwords aren't the same":
            error2 = auth.register(username, password,checkpas,email)
            return render_template('register.html', error2 = error2)
        if auth.register(username,password,checkpas,email) == "There is an account with that email":
            error3 = auth.register(username, password,checkpas,email)
            return render_template('register.html', error3 = error3)

@app.route('/parts/<itemnum>')
def parts(itemnum):
    results = db.parts.find_one({'itemnumber':itemnum})
    name = results["stuff"]["Title"]
    url = gimages.gimages(name)
    if 'username' in session:
        return render_template('parts.html', username = session['username'], results=results, url = url)
    else:
        return render_template('parts.html', results=results, url = url)

@app.route('/add/<itemnum>')
def add(itemnum):
    results = dict()
    if (db.cpus.find_one({'itemnumber':itemnum})):
        session['cpu'] = itemnum
        results['cpu'] = db.cpus.find_one({'itemnum':itemnum})
    if (db.cases.find_one({'itemnumber':itemnum})):
        session['case'] = itemnum
        results['case'] = db.cases.find_one({'itemnum':itemnum})
    if (db.hdds.find_one({'itemnumber':itemnum})):
        session['hdd'] = itemnum
        results['hdd'] = db.hdds.find_one({'itemnum':itemnum})
    if (db.ssds.find_one({'itemnumber':itemnum})):
        session['ssd'] = itemnum
        results['ssd'] = db.ssds.find_one({'itemnum':itemnum})
    if (db.ram.find_one({'itemnumber':itemnum})):
        session['ram'] = itemnum
        results['ram'] = db.ram.find_one({'itemnum':itemnum})
    if (db.mobos.find_one({'itemnumber':itemnum})):
        session['mobo'] = itemnum
        results['mobo'] = db.mobos.find_one({'itemnum':itemnum})
    if (db.psus.find_one({'itemnumber':itemnum})):
        session['psu'] = itemnum
        results['psu'] = db.psus.find_one({'itemnum':itemnum})
    if (db.gpus.find_one({'itemnumber':itemnum})):
        session['gpu'] = itemnum
        results['gpu'] = db.gpus.find_one({'itemnum':itemnum})
    if 'username' in session:
        return render_template('redir.html', username= session['username'])
    else:
        return render_template('redir.html')


@app.route('/build')
def build():
    results = dict()
    sum = cpu = case = gpu = psu = hdd = ssd = ram = mobo = 0
    for x in session:
        if x == 'cpu':
            results['cpu'] = db.cpus.find_one({'itemnumber':session[x]})
        if x == 'case':
            results['case'] = db.cases.find_one({'itemnumber':session[x]})
        if x =='gpu':
            results['gpu'] = db.gpus.find_one({'itemnumber':session[x]})
        if x == 'psu':
            results['psu'] = db.psus.find_one({'itemnumber':session[x]})
        if x =='hdd':
            results['hdd'] = db.hdds.find_one({'itemnumber':session[x]})
        if x == 'ssd':
            results['ssd'] = db.ssds.find_one({'itemnumber':session[x]})
        if x =='ram':
            results['ram'] = db.ram.find_one({'itemnumber':session[x]})
        if x == 'mobo':
            results['mobo'] = db.mobos.find_one({'itemnumber':session[x]})
	if db.cpus.find_one({'itemnumber':session[x]}):
	    cpu = float(results['cpu']['stuff']['fPrice'].replace("$",""))
	if db.cases.find_one({'itemnumber':session[x]}):
	    case = float(results['case']['stuff']['fPrice'].replace("$",""))
	if db.gpus.find_one({'itemnumber':session[x]}):
	    gpu = float(results['gpu']['stuff']['fPrice'].replace("$",""))
	if db.psus.find_one({'itemnumber':session[x]}):
	    psu = float(results['psu']['stuff']['fPrice'].replace("$",""))
	if db.hdds.find_one({'itemnumber':session[x]}):
	    hdd = float(results['hdd']['stuff']['fPrice'].replace("$",""))
	if db.ssds.find_one({'itemnumber':session[x]}):
	    ssd = float(results['ssd']['stuff']['fPrice'].replace("$",""))
	if db.ram.find_one({'itemnumber':session[x]}):
	    ram = float(results['ram']['stuff']['fPrice'].replace("$",""))
	if db.mobos.find_one({'itemnumber':session[x]}):
	    mobo = float(results['mobo']['stuff']['fPrice'].replace("$",""))
	sum = cpu+case+gpu+psu+hdd+ssd+ram+mobo
    if 'username' in session:
        return render_template('build.html', username = session['username'], results=results, add=sum)
    else:
        return render_template('build.html', results=results, add=sum)

@app.route('/remove/<part>')
def remove(part):
    session.pop(part, None)
    if 'username' in session:
        return render_template('rem.html', username=session['username'])
    else:
        return render_template('rem.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('home.html')

@app.route('/cpu')
def cpu():
    results = list(db.cpus.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('cpu.html', username = session['username'], results=results)
    else:
        return render_template('cpu.html', results=results)

@app.route('/mobo')
def mobo():
    results = list(db.mobos.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('mobo.html', username = session['username'], results=results)
    else:
        return render_template('mobo.html', results=results)

@app.route('/ram')
def ram():
    results = list(db.ram.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('ram.html', username = session['username'], results=results)
    else:
        return render_template('ram.html', results=results)

@app.route('/hdd')
def hdd():
    results = list(db.hdds.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('hdd.html', username = session['username'], results=results)
    else:
        return render_template('hdd.html', results=results)

@app.route('/ssd')
def ssd():
    results = list(db.ssds.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('ssd.html', username = session['username'], results=results)
    else:
        return render_template('ssd.html', results=results)

@app.route('/gpu')
def gpu():
    results = list(db.gpus.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('gpu.html', username = session['username'], results=results)
    else:
        return render_template('gpu.html', results=results)

@app.route('/psu')
def psu():
    results = list(db.psus.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('psu.html', username = session['username'], results=results)
    else:
        return render_template('psu.html', results=results)

@app.route('/case')
def case():
    results = list(db.cases.find({}, fields={'_id':False}))
    if 'username' in session:
        return render_template('case.html', username = session['username'], results=results)
    else:
        return render_template('case.html', results=results)

@app.route('/gen')
def gen():
    return render_template('gen.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=6002)

#use this to learn about the structure of the db
#result = list(db.cpus.find({}, fields = {'_id':False}))
#print result[0]['specs']
#result = db.cpus.find_one({"itemnumber":"11-233-116"})

