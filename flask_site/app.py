from flask import Flask, render_template

app = Flask(__name__)

#This will server more or less as my api for this project.

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/create_folder')
def create_folder():
    return render_template("create.html")

@app.route('/audit')
def audit():
    return render_template("audit.html")

@app.route('/direct')
def direct():
    return render_template("direct.html")

@app.route('/indirect')
def indirect():
    return render_template("indirect.html")

if __name__ == '__main__':
    app.run(debug=True)
