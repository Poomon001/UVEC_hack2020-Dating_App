from flask import  Flask, render_template, url_for, redirect, request, send_file
import dating
import csv
from geopy.distance import great_circle

''' create instance of Flask web app '''
app = Flask(__name__)

''' The decoration is to give a route to Flask to access this method '''
''' in the route parameter is to give a path to the method (web query) '''
@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for("matching"))

''' matching two user email and display score '''
@app.route("/matching", methods=['GET', 'POST'])
def matching():
    if request.method == "POST":
        email_1 = request.form['email_1']
        email_2 = request.form['email_2']
        score = dating.sc(email_1, email_2, 0)
        return render_template("displayMatching.html", text="Matching Mode", score = score)
    else:
        return render_template("upload.html", text="Matching Mode")

''' ranking the top 10 users you may interest '''
@app.route("/ranking", methods=['GET', 'POST'])
def ranking():
    if request.method == "POST":
        email_1 = request.form['email_1']
        persons = dating.sc(email_1, '', 1)
        return render_template("displayRanking.html", text="Ranking Mode", person = persons)
    else:
        return render_template("upload2.html", text="Ranking Mode")

@app.route("/testCases")
def testCases():
    return send_file('UVEC-Fall-2020-Seed.csv', as_attachment=True, attachment_filename='UVEC-Fall-2020-testCases.csv')

if __name__ == "__main__":
    app.run(debug=True)