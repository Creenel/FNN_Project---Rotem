from flask import Flask, redirect, request, url_for, render_template, session
import pyrebase

fbConfig = {
  "apiKey": "AIzaSyDEWpvhpXcMyzE7Se4zYTj_uaS7rpDB4CA",
  "authDomain": "fitnerd-nexus.firebaseapp.com",
  "projectId": "fitnerd-nexus",
  "storageBucket": "fitnerd-nexus.appspot.com",
  "messagingSenderId": "254774254492",
  "appId": "1:254774254492:web:3bab832d1357c420648659",
  "measurementId": "G-FYHVVTLW4D",
  "databaseURL":"https://fitnerd-nexus-default-rtdb.europe-west1.firebasedatabase.app/"
}

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.config['SECRET_KEY'] = "spicytuna"

firebase = pyrebase.initialize_app(fbConfig)
auth = firebase.auth()
db = firebase.database()

@app.route("/")
def main():
	return render_template("hub.html")

if __name__ == '__main__':
	app.run(debug = True)