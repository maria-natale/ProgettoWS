from flask import Flask, render_template

app = Flask(__name__,static_folder="templates/static")
@app.route("/")
def hello():
    return render_template('index.html')