from flask import Flask, redirect, request, url_for, render_template, session
import pyrebase
from datetime import datetime

fbConfig = {
  "apiKey": "AIzaSyDEWpvhpXcMyzE7Se4zYTj_uaS7rpDB4CA",
  "authDomain": "fitnerd-nexus.firebaseapp.com",
  "projectId": "fitnerd-nexus",
  "storageBucket": "fitnerd-nexus.appspot.com",
  "messagingSenderId": "254774254492",
  "appId": "1:254774254492:web:3bab832d1357c420648659",
  "measurementId": "G-FYHVVTLW4D",
  "databaseURL":"https://fitnerd-nexus-default-rtdb.europe-west1.firebasedatabase.app/"}

app = Flask(__name__, template_folder = "templates", static_folder = "static")
app.config['SECRET_KEY'] = "spicytuna"

firebase = pyrebase.initialize_app(fbConfig)
auth = firebase.auth()
db = firebase.database()

@app.route("/")
def main():
  db.child('verified_users').set(['aReal_Person','veryspecialtestuser'])
  return render_template("main.html")

@app.route("/signup", methods = ["GET","POST"])
def signup():
  if request.method == "POST":
    user = {"username":request.form["username"],"email":request.form["email"]}
    session['user'] = auth.create_user_with_email_and_password(user['email'],request.form["password"])
    session['uid'] = session['user']['localId']
    session['username'] = user['username']
    db.child('Users').child(session['uid']).set(user)
    if session['username'] in db.child('verified_users').get().val():
      session['verified'] = True
    else:
      session['verified'] = False
    return redirect(url_for("feed"))
  else:
    return render_template("signup.html")

@app.route("/signin", methods = ["GET","POST"])
def signin():
  if request.method == "POST":
    session['user'] = auth.sign_in_with_email_and_password(request.form['email'],request.form['password'])
    return redirect(url_for("feed"))
  else:
    return render_template("signin.html")

@app.route("/feed")
def feed():
  posts = db.child("Posts").get().val()
  d = datetime.now().strftime("%d-%m-%Y")
  return render_template("feed.html", posts = posts, d = d)

@app.route("/post", methods = ['GET','POST'])
def post():
  if request.method == "POST":
     post = {"title": request.form['title'],"text":request.form['text'],"author":session['username']}
     db.child("Posts").push(post)
     return redirect(url_for("feed"))
  elif session['verified'] == True:
    return render_template("post_verified.html")
  else:
    return render_template("post.html")

@app.route("/verify")
def verify():
  return render_template("verify?.html")

@app.route("/signout")
def signout():
  session['user'] = None
  auth.current_user = None
  return redirect(url_for("signin"))


if __name__ == '__main__':
	app.run(debug = True)