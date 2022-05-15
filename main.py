import sqlite3
import requests
from bs4 import BeautifulSoup
from werkzeug.security import generate_password_hash, check_password_hash
from flask import * 
from flask_login import login_user, login_required, logout_user, current_user
import random
import time

now = int( time.time())
print( now )



app = Flask(__name__)
app.secret_key="swift"
conn = sqlite3.connect("testing.db")
c = conn.cursor()


@app.route('/', methods=["POST", "GET"])
def index():
  conn = sqlite3.connect("testing.db")
  c = conn.cursor()
  c.execute("SELECT * FROM user_data")
  users=c.fetchall()
  print(users)  
  return render_template("Home.html")

@app.route('/results', methods=["POST", "GET"])
def results():
  conn = sqlite3.connect("testing.db")
  c = conn.cursor()
  global now4
  now4 = int( time.time())
  fintime=now4-now3
  if request.method=="POST":
    q1=request.form["q1"]
    q2=request.form["q2"]
    q3=request.form["q3"]
    q4=request.form["q4"]
    q5=request.form["q5"]
    q6=request.form["q6"]
    q7=request.form["q7"]
    q8=request.form["q8"]
    q9=request.form["q9"]
    q10=request.form["q10"]
    fin_ans=[q1,q2,q3,q4,q5,q6,q7,q8,q9,q10]
    print(fin_ans)
    b=0
    ans_list=[]
    a=0
    while a<=9:
      print(a)
      ans=randomlist[a]*randomlist2[a]
      ans_list.append(ans)
      a+=1
    ans_list=ans_list
    fin_ans=fin_ans
    print(ans_list)
    print(fin_ans)
    print("q")
    for i in range(len(ans_list)):
      print("r")
      if int(ans_list[i])==int(fin_ans[i]):
        print("s")
        b+=1
    score=(100-fintime)*(b)
    if score<0:
      score=0
    score1=f"Your Score Is {score}"
    c.execute("SELECT * FROM user_data")
    users=c.fetchall()
    print(users)
    score=int(score)
    username=session["user"]
    for u in users:
      print(u[2]<score)
      if int(u[2])<score:
        c.execute("UPDATE user_data SET time = (?) where username= (?)", (score, username))
        conn.commit()
        print("Done")
    
    return render_template("results.html", b=b, fintime=fintime, score=score1)
  else:
    return render_template("Home.html")

@app.route('/add_results', methods=["POST", "GET"])
def add_results():
  
  if request.method=="POST":
    global now2
    now2 = int( time.time())
    fintime=now2-now
    q1=request.form["q1"]
    q2=request.form["q2"]
    q3=request.form["q3"]
    q4=request.form["q4"]
    q5=request.form["q5"]
    q6=request.form["q6"]
    q7=request.form["q7"]
    q8=request.form["q8"]
    q9=request.form["q9"]
    q10=request.form["q10"]
    fin_ans=[q1,q2,q3,q4,q5,q6,q7,q8,q9,q10]
    print(fin_ans)
    b=0
    ans_list=[]
    a=0
    while a<=9:
      print("here")
      ans=int(randomlist[a])+int(randomlist2[a])
      ans_list.append(ans)
      a+=1
    print(ans_list)
    print(fin_ans)
    print("q")
    for i in range(len(ans_list)):
      print("r")
      if int(ans_list[i])==int(fin_ans[i]):
        print("s")
        b+=1

    return render_template("results.html", b=b, fintime=fintime)
  else:
    return render_template("Home.html")


@app.route('/login', methods=["POST", "GET"])
def log():
    if "user" in session:
      return redirect(url_for("game"))

    conn = sqlite3.connect("testing.db")
    c = conn.cursor()
    if request.method == "POST":
        print(request.form)
        username = request.form["username"]
        session["user"] = username
        password = request.form["password"]
        password_hash = generate_password_hash(password)
        c.execute("SELECT * FROM user_data")
        saved_values = c.fetchall()
        #user = User.query.filter_by(email=email).first()
        for value in saved_values:
            if value[0] == username and check_password_hash(
                    value[1], password) == True:
                      # login_user(user, remember=True)
                      return render_template("Game.html")

    else:
        return render_template("Login.html")


@app.route('/sign', methods=["POST", "GET"])
def sign():
    conn = sqlite3.connect("testing.db")
    c = conn.cursor()
    if request.method == "POST":
        username = request.form["regemail"]
        password = request.form["regpassword"]
        password_hash = generate_password_hash(password)
        c.execute("INSERT INTO user_data (username, password, time, most_anwered) VALUES (?,?,?,?)",
            (username, password_hash, 0, 0))
        conn.commit()
        # login_user(username, remember=True)
        return render_template("Game.html")
    else:
        return render_template("Signup.html")

@app.route('/leaderboard')
def leaderboard():
  return render_template('leaderboard.html')

@app.route('/game', methods=["POST", "GET"])
#@login_required
def game():
    conn = sqlite3.connect("testing.db")
    c = conn.cursor()

    return render_template("Game.html")


@app.route('/multiplication', methods=["POST", "GET"])
def multiplication():

  global now3
  
  now3 = int( time.time())

  global randomlist
  
  randomlist =[]
  
  for i in range(0,10):
    n = random.randint(0,9)
    randomlist.append(n)

  global randomlist2
  randomlist2 = []
  
  for i in range(0,10):
    n = random.randint(0,9)
    randomlist2.append(n)


  a=0
  ans_list=[]
  while a<=9:
    ans=randomlist[a]*randomlist2[a]
    ans_list.append(ans)
    a+=1

  imgSrcList = [f"https://latex.codecogs.com/png.image?{randomlist[i]}\cdot{randomlist2[i]}" for i in range(len(randomlist))]
  print(imgSrcList)
  global now
  now = int( time.time())
  return render_template("category.html", len=len(randomlist), randomlist=randomlist, randomlist2=randomlist2, imgSrcList=imgSrcList, ans_list=ans_list)

@app.route('/addition', methods=["POST", "GET"])
def addition():
  
  global randomlist
  randomlist = []
  for i in range(0,10):
    n = random.randint(10,99)
    randomlist.append(n)

  global randomlist2
  randomlist2 = []
  for i in range(0,10):
    n = random.randint(10,99)
    randomlist2.append(n)


  a=0
  ans_list=[]
  while a<=9:
    print(a)
    ans=randomlist[a]+randomlist2[a]
    ans_list.append(ans)
    a+=1

  print(randomlist)
  print(randomlist2)
  print(ans_list)
  imgSrcList = [f"https://latex.codecogs.com/png.image?%7B{randomlist[i]}%7D+%7B{randomlist2[i]}%7D" for i in range(len(randomlist))]
  print(imgSrcList)
  return render_template("addition.html", len=len(randomlist), randomlist=randomlist, randomlist2=randomlist2, imgSrcList=imgSrcList)
  
# c.execute("""CREATE TABLE user_data(
# username TEXT,
# password TEXT,
# time INTEGER,
# most_anwered INTEGER
# )""")
# conn.commit()
# conn.close()



@app.route('/logout')
def logout():
  if "user" in session:
    session.pop("user",None)
    return render_template("Home.html")
  else:
    return render_template("Home.html")

  
app.run(host='0.0.0.0', port=81)