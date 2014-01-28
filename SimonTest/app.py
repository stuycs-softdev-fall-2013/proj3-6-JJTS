from flask import Flask, render_template, url_for, redirect, request, session



app = Flask(__name__)
app.secret_key = 'asdf'

@app.route("/home")
def home():
    return render_template('cpu.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
