from flask import  Flask, render_template, url_for, redirect, request
import dating
import csv
from geopy.distance import great_circle

''' create instance of Flask web app '''
app = Flask(__name__)

helloworld = "world"

''' The decoration is to give a route to Flask to access this method '''
''' in the route parameter is to give a path to the method (web query) '''
''' / mean current page (default domain) '''
@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for("matching"))

# ''' add <var> (take query str) and pass it to func parameter as a variable  '''
# @app.route("/<name>")
# def user(name):
#     return f"hello {name}"


# def upload():
#     #email_1 = request.form['email_1']
#     return render_template("upload.html")

@app.route("/matching", methods=['GET', 'POST'])
def matching():
    if request.method == "POST":
        email_1 = request.form['email_1']
        email_2 = request.form['email_2']
        return render_template("displayMatching.html", text="Matching Mode", email_1 = email_1, email_2 = email_2)
    else:
        return render_template("upload.html", text="Matching Mode")

@app.route("/ranking", methods=['GET', 'POST'])
def ranking():
    x = dating.hello()
    if request.method == "POST":
        email_1 = request.form['email_1']
        return render_template("displayRanking.html", text="Ranking Mode", email_1 = email_1)
    else:
        return render_template("upload2.html", text="Ranking Mode",  hello = x)

if __name__ == "__main__":
    app.run(debug=True)